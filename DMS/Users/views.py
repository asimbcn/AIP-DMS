from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
# from .forms import CreateUserForm
from django.contrib.auth import password_validation

# Create your views here.
def user_login(request):
    if request.user.is_authenticated:
        return redirect('redir')

    if request.method == 'POST':
        user = authenticate(username=request.POST['username'],
                            password=request.POST['password'])
        if user is not None:
            check = UserInfo.objects.get(user=user)
            if check.active == True:    
                login(request, user)
                return redirect('redir')
            else:
                messages.error(request, 'Your account has been deactivated, Please Contact Admininstrator')
                return redirect('login')
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'users/login.html')

def user_register(request):
    if request.user.is_authenticated:
        return redirect('redir')
    
    if request.method == 'POST':
        name = request.POST['name']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']

        if request.POST['name'] == " " or request.POST['username'] == " " or request.POST['password1'] == " " or request.POST['password2'] == " " or request.POST['email'] == " ":
            messages.error(request, 'Please fill in all fields')
            return redirect('register')
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('register')
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return redirect('login')
        if len(username) <= 6:
            messages.error(request, 'Username must be more than 6 characters')
            return redirect('register')
        if password1!= password2:
            messages.error(request, 'Passwords do not match')
            return redirect('register')
        
        try:
            password_validation.validate_password(password1, None)
        except Exception as e:
            messages.error(request, ', '.join(e))  
            return redirect('register')    
    
        try:
            user = User.objects.create_user(first_name=name, username=username, email=email, password=password1) 
            user.save()
        except Exception as e:
            messages.error(e, 'Something went wrong, Please Try Again Later')
            return redirect('register')

        return redirect('login')

    return render(request, 'users/register.html')

@login_required(login_url='login')
def redir(request):
    if request.method == 'POST':
        return redirect('index')
    return render(request, 'users/redirect.html')

@login_required(login_url='login')
def user_logout(request):
    logout(request)
    return redirect('login')