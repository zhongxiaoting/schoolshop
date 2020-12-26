
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from userprofile.forms import UserLoginForm, UserRegisterForm, ProfileForm, ChangeForm

# 用户登录
from userprofile.models import Profile


def user_login(request):
    if request.method == 'POST':
        user_login_form = UserLoginForm(data=request.POST)
        if user_login_form.is_valid():
            data = user_login_form.clean()
            user = authenticate(username=data['username'], password=data['password'])
            if user:
                login(request, user)
                return redirect("publisher:publisher_list")
            else:
                return HttpResponse("账号或者密码不正确，请重新输入")
        else:
            return HttpResponse("账号或者密码输入不合法")

    elif request.method == 'GET':
        user_login_form = UserLoginForm()
        context = {'form': user_login_form}
        return render(request, 'userprofile/login.html', context)
    else:
        return HttpResponse("请使用GET或者POST登录")


# 退出登录
def user_logout(request):
    logout(request)
    return redirect('publisher:publisher_list')


# 用户注册
def user_register(request):
    if request.method == 'POST':
        user_register_form = UserRegisterForm(data=request.POST)
        if user_register_form.is_valid():
            new_user = user_register_form.save(commit=False)
            # 设置密码
            new_user.set_password(user_register_form.cleaned_data['password'])
            new_user.save()
            # 保存好数据后立即登录并返回博客列表页面
            login(request, new_user)
            return redirect("publisher:publisher_list")
        else:
            return HttpResponse("注册表单输入有误。请重新输入~")
    elif request.method == 'GET':
        user_register_form = UserRegisterForm()
        context = {'form': user_register_form}
        return render(request, 'userprofile/register.html', context)
    else:
        return HttpResponse("请使用GET或POST请求数据")


# 用户删除
@login_required(login_url='/userprofile/login/')
def user_delete(request, id):
    if request.method == 'POST':
        user = User.objects.get(id=id)
        if request.user == user:
            logout(request)
            user.delete()
            return redirect('publisher:publisher_list')
        else:
            return HttpResponse("你没有删除操作的权限")
    else:
        return HttpResponse("仅接受POST请求")


# 编辑用户的信息
@login_required(login_url='/userprofile/login/')
def profile_edit(request, id):
    user = User.objects.get(id=id)
    profile = Profile.objects.get(user_id=id)
    if request.method == 'POST':
        if request.user != user:
            return HttpResponse("你没有权限修改此用户信息")
        profile_form = ProfileForm(request.POST, request.FILES)
        if profile_form.is_valid():
            profile_cd = profile_form.cleaned_data
            profile.phone = profile_cd['phone']
            profile.bio = profile_cd['bio']
            if 'avatar' in request.FILES:
                profile.avatar = profile_cd["avatar"]
            profile.save()
            return redirect('userprofile:edit', id=id)
        else:
            return HttpResponse("表单注册有误，请重新输入~")

    elif request.method == 'GET':
        profile_form = ProfileForm()
        context = {'profile_form': profile_form, 'profile': profile, 'user': user}
        return render(request, 'userprofile/edit.html', context)
    else:
        return HttpResponse("请使用GET或POST请求数据")


# 修改密码
@login_required(login_url='/userprofile/login/')
def change_pass(request):
    if request.method == 'POST':
        form = ChangeForm(request.POST)
        if form.is_valid():
            username = request.user.username
            old_password = request.POST.get('old_password', '')
            # 验证用户密码是否正确
            user = authenticate(username=username, password=old_password)
            if user:
                # 获取新密码
                new_password = request.POST.get('new_password', '')
                # 设置密码
                user.set_password(new_password)
                user.save()
                return HttpResponse("修改成功!")
            else:
                return HttpResponse("用户名获取密码不正确")
        else:
            return HttpResponse("用户名或者密码不合法")
    else:
        form = ChangeForm()
        context = {'form': form}
        return render(request, 'userprofile/change.html', context)

