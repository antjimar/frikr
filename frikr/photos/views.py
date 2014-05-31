# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from models import Photo
from django.http import HttpResponseNotFound
from django.contrib.auth import authenticate, login, logout
from forms import LoginForm


def home(request):
    all_photos = Photo.objects.filter(visibility=Photo.VISIBILITY_PUBLIC).order_by('-created_at')
    context = {
        'photo_list' : all_photos[:10]
    }
    return render(request, 'photos/home.html', context)


def photo_detail(request, pk):
    possible_photos = Photo.objects.filter(pk=pk) # buscamos la foto
    if len(possible_photos) == 0: # si no encuentra la foto
        return HttpResponseNotFound("No existe la foto indicada")
    else:
        selected_photo = possible_photos[0]
        context = {
            'photo' : selected_photo
        }
        return render(request, 'photos/photo_detail.html', context)


def user_login(request):

    error_messages = []
    if request.method == 'POST': # si me envían datos
        login_form = LoginForm(request.POST)

        if login_form.is_valid():
            username = login_form.cleaned_data.get('user_username')
            password = login_form.cleaned_data.get('user_password')
            # buscamos el usuario con ese username y password
            user = authenticate(username=username, password=password)
            if user is None: # si es null
                error_messages.append("Nombre de usuario o contraseña incorrectos")
            else:
                if user.is_active: # si esta activo hacemos el login
                    login(request, user)
                    return redirect('/') # le enviamos al home
                else:
                    error_messages.append("El usuario no está activo")
    else:
        login_form = LoginForm() # formulario vacio cuando la petición es GET

    context = {
        'form' : login_form,
        'errors' : error_messages
    }

    return render(request, 'photos/login.html', context)


def user_logout(request):
    if request.user.is_authenticated():
        logout(request)
    return redirect('/')


def user_profile(request):
    # photos = Photo.objects.filter(owner=request.user)
    photos = request.user.photo_set.all()
    context = {
        'photos' : photos
    }
    return render(request, 'photos/profile.html', context)










