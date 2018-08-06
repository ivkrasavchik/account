# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render, render_to_response, redirect
from django.contrib import auth, messages
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.template import RequestContext
from django.template.context_processors import csrf
from .forms import UserProfileForm, UserPassForm, EmailRegisterForm
from django.contrib.auth import update_session_auth_hash


def home(request):
    user = auth.get_user(request)
    return render_to_response('home.html', {'user': auth.get_user(request)})


# @csrf_protect
def login(request):
    args = {}
    args.update(csrf(request))
    if request.POST:
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            print("вьюха -> login: ", username, password)
            auth.login(request, user)
            return redirect('/')

        else:
            args['login_error'] = "Пользователь не найден"
            print("вьюха -> login: ", username, password)
            return render_to_response('login.html', args)

    else:
        return render_to_response('login.html', args)


def logout(request):
    auth.logout(request)
    return redirect("/")


def register(request):
    args = {}
    args.update(csrf(request))
    args['form'] = UserCreationForm()
    if request.POST:
        newuser_form = UserCreationForm(request.POST)
        if newuser_form.is_valid():
            newuser_form.save()
            newuser = auth.authenticate(username=newuser_form.cleaned_data['username'],
                                        password=newuser_form.cleaned_data['password2'])
            auth.login(request, newuser)
            return redirect('/')
        else:
            args['form'] = newuser_form
            return render_to_response('login.html', args)
    return render_to_response('changepass.html', args)


def eregister(request):
    args = {}
    args.update(csrf(request))
    args['form'] = EmailRegisterForm()
    if request.POST:
        newuser_form = EmailRegisterForm(request.POST)
        if newuser_form.is_valid():
            newuser_form.save()
            newuser = auth.authenticate(username=newuser_form.cleaned_data['username'],
                                        password=newuser_form.cleaned_data['password2'])
            auth.login(request, newuser)
            return redirect('/')
        else:
            args['form'] = newuser_form
            return render_to_response('changepass.html', args)
    return render_to_response('changepass.html', args)


def change_user_setting(request):
    args = {}
    args.update(csrf(request))

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ваши данные UPS изменены!')
            # args['msg'] = "Change success"
            return redirect('/')
            # return HttpResponse("Change success")
    else:
        form = UserProfileForm(instance=request.user)
    args['form'] = form
    return render_to_response('changepass.html', args)


def change_user_pass(request):
    args = {}
    args.update(csrf(request))

    if request.method == 'POST':
        form = UserPassForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            return redirect('/')
            # return HttpResponse("Change success")
    else:
        form = UserPassForm(request.user)
    args['form'] = form
    return render_to_response('changepass.html', args)
