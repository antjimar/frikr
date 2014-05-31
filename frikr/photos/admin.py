# -*- coding: utf-8 -*-
from django.contrib import admin
from models import Photo


class PhotoAdmin(admin.ModelAdmin):

    # list customization
    list_display = ('name', 'owner_name', 'license', 'visibility')
    list_filter = ('license', 'visibility')
    search_fields = ('name', 'description')

    def owner_name(self, obj):
        return obj.owner.first_name + ' ' + obj.owner.last_name

    owner_name.short_description = 'Propietario'
    owner_name.admin_order_field = 'owner'


    # detail customization
    fieldsets = (
        (None, {
            'fields' : ('name', 'url', 'owner'),
            'classes' : ('wide',)
        }),
        ('Descripción', {
            'fields' : ('description',),
            'classes': ('wide',)
        }),
        ('Licencia y visibilidad', {
            'fields' : ('license', 'visibility'),
            'classes': ('wide', 'collapse')
        })
    )

admin.site.register(Photo, PhotoAdmin) # Add Photo to admin web interface