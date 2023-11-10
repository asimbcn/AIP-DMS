from .views import *
from .models import *
import re
import io
import pytesseract
from pdf2image import convert_from_path
from PIL import Image
import docx2txt as dt

def file_type(request):
    file = request.FILES['file']
    file_type = file.name.split('.')[-1]
    file_name = file.name.split('.')[0]
    return  file_name, file_type

def file_is_valid(file_ext):
    valid_file_ext = ['doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'pdf', 'txt', 'jpg', 'jpeg', 'png']
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

def extract_text_from_pdf(pdf_path, type):
    pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe' 
    try:
        if type == "pdf":
            pages = convert_from_path(pdf_path, 500, poppler_path=r'C:/Proppler/Library/bin')
            text_data = ''
            for page in pages:
                text = pytesseract.image_to_string(page)
                text_data += text + '\n'
            return text_data.split()
        if type == "jpg" or type == "jpeg" or type == "png":
            img = Image.open(pdf_path)
            # Perform OCR using PyTesseract
            text = pytesseract.image_to_string(img)  
            return text.split() 
        if type == "doc" or type == "docx":
            text = dt.process(pdf_path)
            return text
    except Exception as e:
        print(e)
        return ''
    

def check_user_status(request):
    user = UserInfo.objects.get(user=request.user)
    if user.active == True:
        return True
    else:
        return False
