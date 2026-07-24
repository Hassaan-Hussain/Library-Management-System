from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, UserLoginForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required


# Create your views here.

# User Registration View
def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            print(name, password)
            form.save()
            return redirect('books_view')
    else:
        form = UserRegistrationForm()

    return render(request, 'User/register.html', {'form': form})

# User Login View
def login_view(request):
    if request.method == 'POST':
        login_form = UserLoginForm(request.POST)

        if login_form.is_valid():
            user = login_form.cleaned_data.get('user')
            password = login_form.cleaned_data.get('password')
            User = authenticate(username=user, password=password)

            if User:
                print("user is authenticated")
                login(request, User)
                return redirect('books_view')
            else:
                messages.info(request, 'Login Failed.Try again.')
                
    else:
        login_form = UserLoginForm()

    return render(request, 'User/login.html', {'login_form': login_form})

# User Logout View
def logout_view(request):
    logout(request)
    return redirect('login')