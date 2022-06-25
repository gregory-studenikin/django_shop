from django.contrib.auth import logout
from django.shortcuts import render, redirect


def login_user(request):
    return render(request, template_name='auth/login.html')


def register(request):
    return render(request, template_name='auth/register.html')


def logout_user(request):
    logout(request)
    return redirect('index')
