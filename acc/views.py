# -*- coding: utf-8 -*-

from django.shortcuts import render, render_to_response, redirect
from django.contrib import auth
from django.template.context_processors import csrf


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
            auth.login(request, user)
            return redirect('/')

        else:
            args['login_error'] = "Пользователь не найден"
            print(username, password)
            return render_to_response('login.html', args)

    else:
        return render_to_response('login.html', args)



def logout(request):
    auth.logout(request)
    return redirect("/")
