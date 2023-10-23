from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import *
from Users.models import *
from .utils import clean_name, check_file_version, file_type, file_is_valid, check_prev_version
from django.db.models import Q
from django.contrib import messages
from Users.utils import *
from django.contrib.auth import password_validation
from django.db.models.functions import Extract
# Create your views here.

@login_required(login_url='login')
def index(request):
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
    profile = UserInfo.objects.get(user=request.user)
    files = Files.objects.filter(Q(group=profile.group) | Q(group="all") & Q(new_version=False))
    new_ver = Version_control.objects.filter(Q(group=profile.group) | Q(group="all") & Q(new_version=False))
 
    if files.count() == 0:
        context = {'data1': new_ver, 'shared':'shared','user':profile}
    if new_ver.count() == 0:
        context = {'data': files, 'shared':'shared','user':profile}
    if new_ver.count() > 0 and files.count() > 0:
        context = {'data': files, 'data1': new_ver, 'shared':'shared', 'user':profile}

    return render(request, 'dms/with_me.html', context)

@login_required(login_url='login')
def upload_files(request):

    if request.method == 'POST':
        try:
            file = request.FILES['file']
            name, type = file_type(request)
            org_name = clean_name(name)
            group = request.POST['group']
        except:
            messages.error(request, 'Please choose a file to upload!')
            return redirect('upload')


        if file_is_valid(type):
            if check_file_version(org_name, type):
                if check_prev_version(org_name, type):
                    file1 = file1 = Files.objects.get(name=name, extension=type)
                    version_ctrl = Version_control.objects.get(org_name=org_name, prev_version=file1, new_version=False)
                    
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
                    vc1.save()

                    return redirect('index')
                else:
                    try:
                        file1 = Files.objects.get(name=name, extension=type)
                        name = name + '_' + str(file1.version + 1)
                        version = file1.version + 1
                        
                        vc = Version_control.objects.create(name=name, prev_version=file1, file=file, org_name=org_name, uploaded_by = request.user, version=version, group=group, extension=type)
                        vc.save()
                        file1.new_version=True
                        file1.save()

                        vc1 = Version_control.objects.get(org_name=org_name, prev_version=file1, version=version)
                        vc1.pre_ver_control = vc1
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
                    return redirect('index')
                except:
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

        # filestime = Files.objects.all().values('created_at').annotate(date_only=Extract('created_at', 'month'))
        # vctime = Version_control.objects.all().values('created_at').annotate(date_only=Extract('created_at', 'month'))
            
        
        context = {'active_users':active_users,'inactive_users':inactive_users,'total':files+vc,'files':files,'vc':vc,
                   'total_dept':all+manage+account+sales+tech,'all':all,'manage':manage,
                   'account':account,'sales':sales,'tech':tech}
        return render(request, 'dms/statistics/statistics.html', context)
    else:
        return HttpResponse('Not permitted')
    
@login_required(login_url='login')
def search(request):
    profile = UserInfo.objects.get(user=request.user)
    context= {'search':'search','user':profile}
    
    if request.method == 'POST':
        search = request.POST['search']
        print(search)
        files = Files.objects.filter(Q(org_name__icontains=search) | Q(extension__icontains=search)).filter(Q(group=profile.group) | Q(group="all") | Q(uploaded_by=request.user ))
        new_ver = Version_control.objects.filter(Q(org_name__icontains=search) | Q(extension__icontains=search)).filter(Q(group=profile.group) | Q(group="all")| Q(uploaded_by=request.user ))

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
    logs = Security_logs.objects.all()
    context = {'data':logs}
    return render(request, 'dms/statistics/security.html', context)