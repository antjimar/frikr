# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from models import Photo
from django.http import HttpResponseNotFound
from django.contrib.auth import authenticate, login, logout
from forms import LoginForm, PhotoForm
from django.contrib.auth.decorators import login_required
from django.views.generic import View, ListView
from django.utils.decorators import method_decorator


class HomeView(View):

    def get(self, request):
        """
        Recibe las peticiones GET
        """
        all_photos = Photo.objects.filter(visibility=Photo.VISIBILITY_PUBLIC).order_by('-created_at')
        context = {
            'photo_list' : all_photos[:10]
        }
        return render(request, 'photos/home.html', context)


class PhotoDetail(View):

    def get(self, request, pk):
        possible_photos = Photo.objects.filter(pk=pk) # buscamos la foto
        if len(possible_photos) == 0: # si no encuentra la foto
            return HttpResponseNotFound("No existe la foto indicada")
        else:
            selected_photo = possible_photos[0]
            context = {
                'photo' : selected_photo
            }
            return render(request, 'photos/photo_detail.html', context)


class LoginView(View):


    def get(self, request):
        login_form = LoginForm() # formulario vacio cuando la petición es GET
        context = {
            'form' : login_form
        }
        return render(request, 'photos/login.html', context)


    def post(self, request) :

        error_messages = []
        login_form = LoginForm(request.POST)

        if login_form.is_valid() :
            username = login_form.cleaned_data.get('user_username')
            password = login_form.cleaned_data.get('user_password')
            # buscamos el usuario con ese username y password
            user = authenticate(username=username, password=password)
            if user is None :  # si es null
                error_messages.append("Nombre de usuario o contraseña incorrectos")
            else :
                if user.is_active :  # si esta activo hacemos el login
                    login(request, user)
                    next_url = request.GET.get('next', '/')
                    return redirect(next_url)  # le enviamos al home
                else :
                    error_messages.append("El usuario no está activo")
        context = {
            'form' : login_form,
            'errors' : error_messages
        }

        return render(request, 'photos/login.html', context)


def user_logout(request):
    if request.user.is_authenticated():
        logout(request)
    return redirect('/')


class UserProfileView(View):

    @method_decorator(login_required())
    def get(self, request):
        # photos = Photo.objects.filter(owner=request.user)
        photos = request.user.photo_set.all()
        context = {
            'photos' : photos
        }
        return render(request, 'photos/profile.html', context)


@login_required()
def new_photo(request):
    messages = []
    if request.POST: # lo mismo que hacer request.method == 'POST'

        photo_with_user = Photo(owner=request.user)
        photo_form = PhotoForm(request.POST, files=request.FILES, instance=photo_with_user)

        if photo_form.is_valid():
            #new_photo = Photo()
            #new_photo.url = photo_form.cleaned_data.get('url')
            #...
            #new_photo.save()
            new_photo = photo_form.save() # guarda la foto
            messages.append('Foto guardada! <a href="/photos/' + str(new_photo.pk) + '">Ver foto</a>')
            photo_form = PhotoForm()
    else:
        photo_form = PhotoForm()

    context = {
        'form' : photo_form,
        'message_list' : messages
    }
    return render(request, 'photos/new_photo.html', context)



class PhotoList(ListView):
    """
    Lista las fotos del sistema
    """
    model = Photo
    template_name = 'photos/list.html' # en photos/templates/photos/list.html


