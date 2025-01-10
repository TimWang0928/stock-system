# from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect
from .form import UserRegistrationForm
from django.contrib.auth import login

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/admin/')  # 注册后跳转到主页
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

# 判断用户是否是管理员
# def is_admin(user):
#     return user.role == 'admin'
#
# @user_passes_test(is_admin)
# def admin_dashboard(request):
#     return render(request, 'admin_dashboard.html')
