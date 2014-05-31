# -*- coding: utf-8 -*-
from django.shortcuts import render
from models import Photo

def home(request):
    all_photos = Photo.objects.all() # recupera todas las fotos de la DB
    context = {
        'photo_list' : all_photos
    }
    return render(request, 'photos/home.html', context)