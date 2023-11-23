from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import *
from Users.models import *
from .utils import clean_name, check_file_version, file_type, file_is_valid, check_prev_version, extract_text_from_pdf,check_user_status
from django.db.models import Q
from django.contrib import messages
from Users.utils import *
from django.contrib.auth import password_validation
from django.db.models.functions import Extract
# from pypdf import PdfReader
import re
# Create your views here.


@login_required(login_url='login')
def index(request):
    if not check_user_status(request):
        messages.error(request, 'Your account is not active. Please contact admin to activate your account.')
        return redirect('logout')

    user = UserInfo.objects.get(user=request.user)
    files = Files.objects.filter(uploaded_by=request.user, new_version=False)
    new_ver = Version_control.objects.filter(uploaded_by=request.user, new_version=False)
    context = {'index':'index','user':user}

    #show all prev version in front end

    if new_ver.count() > 0:
        context = {'data1': new_ver, 'index':'index', 'user':user}
    if files.count() > 0:
        context = {'data': files, 'index':'index', 'user':user}    
    if new_ver.count() > 0 and files.count() > 0:
         context = {'data': files, 'data1':new_ver, 'index':'index', 'user':user}

    return render(request, 'dms/index.html', context)

@login_required(login_url='login')
def for_me(request):
    if not check_user_status(request):
        messages.error(request, 'Your account is not active. Please contact admin to activate your account.')
        return redirect('logout')

    profile = UserInfo.objects.get(user=request.user)
    files = Files.objects.filter((Q(group=profile.group) | Q(group="all")) & Q(new_version=False))
    new_ver = Version_control.objects.filter((Q(group=profile.group) | Q(group="all")) & Q(new_version=False))

    print(files,new_ver)
    if files.count() == 0:
        context = {'data1': new_ver, 'shared':'shared','user':profile}
    if new_ver.count() == 0:
        context = {'data': files, 'shared':'shared','user':profile}
    if new_ver.count() > 0 and files.count() > 0:
        context = {'data': files, 'data1': new_ver, 'shared':'shared', 'user':profile}

    return render(request, 'dms/with_me.html', context) 

@login_required(login_url='login')
def upload_files(request):

    if not check_user_status(request):
        messages.error(request, 'Your account is not active. Please contact admin to activate your account.')
        return redirect('logout')

    if request.method == 'POST':
        try:
            file = request.FILES['file']
            name, type = file_type(request)
            org_name = clean_name(name)
            group = request.POST['group']
            print(name, org_name)
        except:
            messages.error(request, 'Please choose a file to upload!')
            return redirect('upload')


        if file_is_valid(type):
            if check_file_version(org_name, type):
                pass
                if check_prev_version(org_name, type):
                    file1 = file1 = Files.objects.get(name=name, extension=type)
                    version_ctrl = Version_control.objects.get(org_name=org_name, prev_version=file1, new_version=False)

                    if version_ctrl.locked == True:
                            messages.error(request, 'File is locked for further updated. Contact the file owner for new changes.')
                            return redirect('upload')
                    
                    name = name + '_' + str(version_ctrl.version + 1)
                    version = version_ctrl.version + 1
                    print(name, version, org_name)

                    # new_version update on previos version
                    vc = Version_control.objects.create(name=name, prev_version=file1, file=file, org_name=org_name, uploaded_by = request.user, version=version, group=group,extension=type)
                    vc.save()
                    version_ctrl.new_version=True
                    version_ctrl.save()

                    vc1 = Version_control.objects.get(org_name=org_name, prev_version=file1, version=version)
                    vc1.pre_ver_control = version_ctrl
    
                    text = extract_text_from_pdf(vc1.file.path, type)
                    vc1.file_content = text
                    vc1.save()

                    return redirect('index')
                
                else:
                    try:
                        file1 = Files.objects.get(name=name, extension=type)
                        name = name + '_' + str(file1.version + 1)
                        version = file1.version + 1
                        if file1.locked == True:
                            messages.error(request, 'File is locked for further updated. Contact the file owner for new changes.')
                            return redirect('upload')
                        
                        vc = Version_control.objects.create(name=name, prev_version=file1, file=file, org_name=org_name, uploaded_by = request.user, version=version, group=group, extension=type)
                        vc.save()
                        file1.new_version=True
                        file1.save()

                        vc1 = Version_control.objects.get(org_name=org_name, prev_version=file1, version=version)
                        vc1.pre_ver_control = vc1
                        text = extract_text_from_pdf(vc1.file.path, type)
                        vc1.file_content = text
                        vc1.save()

                        return redirect('index')

                    except Exception as e:
                        print(e)
                        messages.error(request, 'File could not be uploaded, Please try again')
                        return redirect('upload')
                
            else:
                messages.error(request, 'Saving New File')
                try:
                    file = Files.objects.create(file=file,
                                                name=name,
                                                org_name=org_name,
                                                extension=type,
                                                uploaded_by=request.user,
                                                group=group)
                    file.save()
                    text = extract_text_from_pdf(file.file.path, type)
                    file.file_content = text
                    file.save()
                    return redirect('index')
                except Exception as e:
                    print(e)
                    messages.error(request, 'File could not be uploaded, Please try again')
                    return redirect('upload')
                    
        else:
            messages.success(request, 'File extension is not allowed, Please a different file')   
    
        return redirect('upload')
    
    profile = UserInfo.objects.get(user=request.user)
    context = { 'upload':'upload', 'user':profile}
    
    return render(request, 'dms/upload.html', context)

@login_required(login_url='login')
def edit_profile(request):

    if not check_user_status(request):
        messages.error(request, 'Your account is not active. Please contact admin to activate your account.')
        return redirect('logout')
    
    profile = UserInfo.objects.get(user=request.user)
    info_save = False

    if request.method == 'POST':
        if request.user.check_password(request.POST['curr_pass']) == True:
            if 'file' in request.FILES:
                files = request.FILES['file']
                profile.image = files
                info_save = True
            else:
                pass

            if request.POST['pass'] != "" and request.POST['pass1'] != "":
                try:
                    password_validation.validate_password(request.POST['pass'], None)
                    
                    if request.POST['pass'] == request.POST['pass1']:
                        request.user.set_password(request.POST['pass'])
                        request.user.save()
                    else:
                        messages.error(request,'Passwords do not match!') 

                except Exception as e:
                    messages.error(request, ', '.join(e))  
                    return redirect('edit')      

            if info_save == True:
                profile.save()
        else:
            messages.error(request,'Current password is incorrect!')

        return redirect('edit')        
    
    context = {'edit_user':'edit_user', 'data':profile}
    return render(request, 'dms/edit_profile.html', context)

@login_required(login_url='login')
def stats(request):
    if not check_user_status(request):
        messages.error(request, 'Your account is not active. Please contact admin to activate your account.')
        return redirect('logout')

    profile = UserInfo.objects.get(user=request.user)
    if request.user.is_staff == True or profile.group =='management':
        active_users = UserInfo.objects.filter(active=True).count()
        inactive_users = UserInfo.objects.filter(active=False).count()

        files = Files.objects.all().count()
        vc = Version_control.objects.all().count()

        all = Files.objects.filter(group = 'all').count() + Version_control.objects.filter(group = 'all').count()
        manage = Files.objects.filter(group = 'management').count() + Version_control.objects.filter(group = 'management').count()
        account = Files.objects.filter(group = 'accounting').count() + Version_control.objects.filter(group = 'accounting').count()
        sales = Files.objects.filter(group = 'sales').count() + Version_control.objects.filter(group = 'sales').count()
        tech = Files.objects.filter(group = 'tech').count() + Version_control.objects.filter(group = 'tech').count()

        incident = Security_logs.objects.filter(level='0').count()
        warning = Security_logs.objects.filter(level='1').count()
        info = Security_logs.objects.filter(level='2').count()

        # filestime = Files.objects.all().values('created_at').annotate(date_only=Extract('created_at', 'month'))
        # vctime = Version_control.objects.all().values('created_at').annotate(date_only=Extract('created_at', 'month'))
            
        
        context = {'active_users':active_users,'inactive_users':inactive_users,'total':files+vc,'files':files,'vc':vc,
                   'total_dept':all+manage+account+sales+tech,'all':all,'manage':manage,
                   'account':account,'sales':sales,'tech':tech,'incident':incident, 'warning':warning, 'info':info}
        return render(request, 'dms/statistics/statistics.html', context)
    else:
        return HttpResponse('Not permitted')
    
@login_required(login_url='login')
def search(request):
    if not check_user_status(request):
        messages.error(request, 'Your account is not active. Please contact admin to activate your account.')
        return redirect('logout')

    profile = UserInfo.objects.get(user=request.user)
    context= {'search':'search','user':profile}
    
    if request.method == 'POST':
        search = request.POST['search']
        files = Files.objects.filter(Q(org_name__icontains=search) | Q(extension__icontains=search) | Q(file_content__icontains=search)).filter(Q(group=profile.group) | Q(group="all") | Q(uploaded_by=request.user ))
        new_ver = Version_control.objects.filter(Q(org_name__icontains=search) | Q(extension__icontains=search) | Q(file_content__icontains=search)).filter(Q(group=profile.group) | Q(group="all")| Q(uploaded_by=request.user ))

        # all in one compact file
        
        if files.count() == 0:
            data = new_ver
            context={'search':'search','user':profile,'data':data}
        elif new_ver.count() == 0:
            data = files
            context={'search':'search','user':profile,'data':data}
        else: 
            data = files
            data1 = new_ver
            context={'search':'search','user':profile,'data':data,'data1':data1}
        
    
    return render(request, 'dms/search.html',context) 


@login_required(login_url='login')
def view_file(request, pk, type):
    if not check_user_status(request):
        messages.error(request, 'Your account is not active. Please contact admin to activate your account.')
        return redirect('logout')
    
    profile = UserInfo.objects.get(user=request.user)
    if type == "version":
        get_data = Version_control.objects.get(pk=pk)
        org_file = get_data.org_name
        data1 = Version_control.objects.filter(org_name=org_file)
        data = Files.objects.filter(org_name=org_file)
    if type == "file":
        data = Files.objects.filter(pk=pk)
        org_file = data[0].org_name
        data1 = False

    context = {'user':profile,'file_name':org_file,'data':data,'data1':data1}
    return render(request, 'dms/file_list.html', context)

@login_required(login_url='login')
def sec_log(request):
    if not check_user_status(request):
        messages.error(request, 'Your account is not active. Please contact admin to activate your account.')
        return redirect('logout')
    
    logs = Security_logs.objects.all()
    context = {'data':logs}
    return render(request, 'dms/statistics/security.html', context)

@login_required(login_url='login')
def user_info(request):
    if not check_user_status(request):
        messages.error(request, 'Your account is not active. Please contact admin to activate your account.')
        return redirect('logout')
    
    info = UserInfo.objects.all()
    context = {'data':info}
    return render(request, 'dms/statistics/user_info.html', context)

@login_required(login_url='login')
def add_logs(request):
    if not check_user_status(request):
        messages.error(request, 'Your account is not active. Please contact admin to activate your account.')
        return redirect('logout')
    
    if request.method == 'POST':
        user = User.objects.get(username='root')
        try:
            logs = Security_logs.objects.create(User=user, Action=request.POST['action'], level=request.POST['level'],  message=request.POST['message'])
            logs.save()
            return redirect('logs')
        except Exception as e:
            print(e)
            messages.error(request, 'Please try again later')
            return redirect('add_logs')
           
    return render(request, 'dms/statistics/add_logs.html')

@login_required(login_url='login')
def change_status(request,pk, reason=None):
    if not check_user_status(request):
        messages.error(request, 'Your account is not active. Please contact admin to activate your account.')
        return redirect('logout')
    
    user = UserInfo.objects.get(pk=pk)
    if user.active == True:
        if reason != None or reason != 'test':
            user.remarks = reason
        user.active = False
    else:
        user.remarks = "Active"
        user.active = True

    try:
        user.save()
    except Exception as e:
        print(e)
        messages.error(request, 'Changes cannot be made, Please try again later')
        
    return redirect('user_info')

@login_required(login_url='login')
def download(request,pk,type):
    if not check_user_status(request):
        messages.error(request, 'Your account is not active. Please contact admin to activate your account.')
        return redirect('logout')
    
    if type == "version":
        data = Version_control.objects.get(pk=pk)
        name = data.prev_version.name
    if type == "file":
        data = Files.objects.get(pk=pk)
        name = data.name

    response = HttpResponse(data, content_type=f"text/{data.extension}")
    response['Content-Disposition'] = f"attachment; filename={name}.{data.extension}"
    return response 

@login_required(login_url='login')
def restrict(request,pk):
    if not check_user_status(request):
        messages.error(request, 'Your account is not active. Please contact admin to activate your account.')
        return redirect('logout')
    
    if request.method == "POST":
        user = UserInfo.objects.get(pk=pk)
        option = request.POST['myselect']
        user.group = option
        try:
            user.save()
        except Exception as e:
            messages.error(request, 'Changes cannot be made, Please try again later')  

    return redirect('user_info')

@login_required(login_url='login')
def active_change(request,pk):
    if not check_user_status(request):
        messages.error(request, 'Your account is not active. Please contact admin to activate your account.')
        return redirect('logout')
    
    return redirect('change_status', pk=pk, reason=request.POST['reason'])


@login_required(login_url='login')
def edit_file(request,pk,type):
    if not check_user_status(request):
        messages.error(request, 'Your account is not active. Please contact admin to activate your account.')
        return redirect('logout')
    
    if type == "version":
        data = Version_control.objects.get(pk=pk)
        select = data.group
        if data.new_version == False:
            version_info = "Latest Version"
            new_ver = False
        else:
            version_info = f'{data.version}'
            new_ver = Version_control.objects.filter(org_name=data.org_name).order_by('-id')[0]  
           
        type = "version"

    if type == "file":
        data = Files.objects.get(pk=pk)
        select = data.group
        if data.new_version == False:
            version_info = "Latest Version"
            new_ver = False
        else:
            version_info = f'{data.version}'
            new_ver = Version_control.objects.filter(org_name=data.org_name).order_by('-id')[0]   

        type = "file"

    context = {'data':data,'type':type,'version_info':version_info,'new_ver':new_ver,'select':select}
    return render(request,'dms/edit_file.html',context)

@login_required(login_url='login')
def change_group(request, pk, type):
    if not check_user_status(request):
        messages.error(request, 'Your account is not active. Please contact admin to activate your account.')
        return redirect('logout')
    
    if request.method == "POST":
    
        if type == "version":
            data = Version_control.objects.get(pk=pk)
        if type == "file":
            data = Files.objects.get(pk=pk)

        data.group = request.POST['myselect']
        try:
            data.save()
        except Exception as e:  
            messages.error(request, 'Changes cannot be made, Please try again later')
        
        return redirect('edit_file', pk=pk, type=type)
    

@login_required(login_url='login')
def change_locked(request, pk, type):
    if not check_user_status(request):
        messages.error(request, 'Your account is not active. Please contact admin to activate your account.')
        return redirect('logout')
    
    if request.method == "POST":
    
        if type == "version":
            data = Version_control.objects.get(pk=pk)
        if type == "file":
            data = Files.objects.get(pk=pk)

        if data.locked == True:
            data.locked = False
        else:
            data.locked = True
        try:
            data.save()
        except Exception as e:  
            messages.error(request, 'Changes cannot be made, Please try again later')
        
        return redirect('edit_file', pk=pk, type=type)
    

@login_required(login_url='login')
def extract_text(request):
    if not check_user_status(request):
        messages.error(request, 'Your account is not active. Please contact admin to activate your account.')
        return redirect('logout')
    
    context = {}
    
    if request.method == "POST":
        try:
            file = request.FILES['file'] 
            name, type = file_type(request)
            new = Temp_OCR.objects.filter(name=name).first()
            if new is None:
                new = Temp_OCR.objects.create(name=name, file=file)
                new.save()
                text = extract_text_from_pdf(new.file.path, type)
                new.file_content = text
                new.save()
            else:
                text = extract_text_from_pdf(new.file.path, type)

            text = ' '.join(text)
            print(text)               
            context = {'data':text}
        except Exception as e:
            print(e)
            messages.error(request, e)
            return redirect('extract')
    
    return render(request,'dms/extract_text.html',context)
