# -*- coding: utf-8 -*-
from django.shortcuts import render
from models import Photo

def home(request):
    all_photos = Photo.objects.all().order_by('-created_at')
    context = {
        'photo_list' : all_photos[:10]
    }
    return render(request, 'photos/home.html', context)