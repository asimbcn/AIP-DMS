from .views import *
from .models import *
import re

def file_type(request):
    file = request.FILES['file']
    file_type = file.name.split('.')[-1]
    file_name = file.name.split('.')[0]
    return  file_name, file_type

def file_is_valid(file_ext):
    valid_file_ext = ['doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'pdf', 'txt', 'jpg', 'jpeg', 'png', 'bmp']
    if file_ext.lower() in valid_file_ext:
        return True
    else:
        return False
    

def check_file_version(org_name, type):
    file1 = Files.objects.filter(org_name=org_name, extension=type)
    if len(file1) != 0:
        return True
    else:
        return False
    
def check_prev_version(org_name,type):
    file = Files.objects.get(org_name=org_name, extension=type)
    file1 = Version_control.objects.filter(org_name=org_name, prev_version = file,new_version=False)
    print(file1)
    if len(file1) != 0:
        return True
    else:
        return False    

def clean_name(name):
    name = re.sub("[()_-]"," ",name)
    return name