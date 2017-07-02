from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, RegisterForm, UserEditForm, ProfileEditForm, ChangePassworForm
from .models import Profile
from django.contrib import messages
# Create your views here.
def index(request):
    return render(request, 'index.html')
def authenticate(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = auth.authenticate(username = cd['username'],
                                    password = cd['password'])
            if user is not None:
                if user.is_active:
                    auth.login(request, user)
                    return render(request, 'index.html')
                else:
                    form = LoginErrorForm()
                    return render(request, 'account/login.html',
                                            {'form': form, 'errors':"user has been banned"})
        return render(request, 'account/login.html',
                                            {'form': form, 'errors':"wrong username or wrong password"})
    else:
        form = LoginForm()
        return render(request, 'account/login.html',{'form': form})

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if cd['password'] != cd['password2']:
                return render(request, 'account/register.html',
                                        {'form': form, 'errors':"two password are not same"})
            username_exists=User.objects.filter(username=cd['username']).exists()
            if username_exists:
                return render(request, 'account/register.html',
                                        {'form': form, 'errors':"username has existed"})
            new_user = User()
            new_user.username = cd['username']
            new_user.set_password(cd['password'])
            new_user.email =cd['email']
            new_user.save()
            new_profile = Profile.objects.create(user=new_user)
            #new_profile.save()
            return render(request, 'account/register_done.html', {'new_user': new_user})
    else:
        form = RegisterForm()
        return render(request, 'account/register.html', {'form': form})

@login_required
def logout(request):
    auth.logout(request)
    return render(request, 'index.html')

@login_required
def user_edit(request):
    if request.method == 'POST':
        new_user_form = UserEditForm(instance=request.user, data=request.POST)
        new_profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if new_user_form.is_valid() and new_profile_form.is_valid():
            new_user_form.save()
            new_profile_form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        new_user_form = UserEditForm(instance=request.user)
        new_profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'account/user_edit.html', {'user_form': new_user_form, 'profile_form': new_profile_form})

@login_required
def change_password(request):
    if request.method == 'POST':
        form = ChangePassworForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            now_user = request.user
            if auth.authenticate(username = now_user.username, password = cd['old_password']):
                if cd['new_password1'] != cd['new_password2']:
                    messages.error(request, 'two password are not same')
                else:
                    now_user.set_password(cd['new_password1'])
                    now_user.save()
                    auth.login(request, now_user)
                    messages.success(request, 'change successfully')
            else:
                messages.error(request, 'old password wrong')
    else:
        form = ChangePassworForm()
    return render(request, 'account/change_password.html', {'form':form})
