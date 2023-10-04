from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import *
from Users.models import *
from .utils import clean_name, check_file_version, file_type, file_is_valid, check_prev_version
from django.db.models import Q
from django.contrib import messages

# Create your views here.

@login_required(login_url='login')
def index(request):
    user = UserInfo.objects.get(user=request.user)
    files = Files.objects.filter(uploaded_by=request.user, new_version=False)
    new_ver = Version_control.objects.filter(uploaded_by=request.user)
    if new_ver.count() > 0:
        for new in new_ver:
            if new.new_version == True:
                print("New Version for the file uploaded by another user")
                new_ver = Version_control.objects.filter(org_name=new.org_name, new_version=False)
        data = new_ver
    else:
        data = files 

    context = {'data': data, 'index':'index', 'user':user}
    return render(request, 'dms/index.html', context)

@login_required(login_url='login')
def for_me(request):
    profile = UserInfo.objects.get(user=request.user)
    files = Files.objects.filter(Q(group=profile.group) | Q(group="all") & Q(new_version=False))
    new_ver = Version_control.objects.filter(Q(group=profile.group) | Q(group="all") & Q(new_version=False))
 
    if files.count() == 0:
        data = new_ver
        context = {'data': data, 'shared':'shared','user':profile}
    elif new_ver.count() == 0:
        data = files
        context = {'data': data, 'shared':'shared','user':profile}
    else:
        data = files
        data1 = new_ver
        context = {'data': data, 'data1': data1, 'shared':'shared', 'user':profile}
    
    return render(request, 'dms/with_me.html', context)

@login_required(login_url='login')
def upload_files(request):

    if request.method == 'POST':

        try:
            file = request.FILES['file']
            name, type = file_type(request)
            org_name = clean_name(name)
        except:
            messages.error(request, 'Please choose a file to upload!')
            return redirect('upload')


        if file_is_valid(type):
            if check_file_version(org_name, type):
                if check_prev_version(org_name, type):
                    messages.success(request, 'Previous version control exist')
                    file1 = file1 = Files.objects.get(name=name, extension=type)
                    version_ctrl = Version_control.objects.get(org_name=org_name, prev_version=file1, new_version=False)
                    print(version_ctrl)
                else:
                    try:
                        file1 = Files.objects.get(name=name, extension=type)
                        name = name + '_' + str(file1.version + 1)
                        version = file1.version + 1
                        
                        # vc = Version_control.objects.create(name=name, prev_version=file1, file=file, org_name=org_name, uploaded_by = request.user, version=version)
                        # vc.save()
                        # file1.new_version=True
                        # file1.save()

                        # vc1 = Version_control.objects.get(org_name=org_name, prev_version=file1, version=version)
                        # vc1.pre_ver_control = vc1
                        # vc1.save()

                        messages.success(request, 'File already exist, Saving as new version')
                            
                        return redirect('upload')
                    except Exception as e:
                        print(e)
                        messages.error(request, 'File could not be uploaded, Please try again')
                        return redirect('upload')
                
            else:
                messages.error(request, 'Saving New File')
                # try:
                #     file = Files.objects.create(file=file,
                #                                 name=name,
                #                                 org_name=org_name
                #                                 extension=type,
                #                                 uploaded_by=request.user)
                #     file.save()
                #     messages.success(request, 'File uploaded successfully')
                #     return redirect('index')
                # except:
                #     messages.error(request, 'File could not be uploaded, Please try again')
                #     return redirect('index')
                    
        else:
            messages.success(request, 'File extension is not allowed, Please a different file')   
    
        return redirect('upload')
    
    profile = UserInfo.objects.get(user=request.user)
    context = { 'upload':'upload', 'user':profile}
    
    return render(request, 'dms/upload.html', context)


    