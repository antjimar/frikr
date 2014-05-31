# -*- coding: utf-8 -*-
from django.shortcuts import render
from models import Photo
from django.http import HttpResponseNotFound

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