# -*- coding: utf-8 -*-
from django.db import models

class Photo(models.Model):

    COPYRIGHT = 'RIG'
    COPYLEFT = 'LEF'
    CREATIVE_COMMONS = 'CC'

    LICENSES = (
        (COPYRIGHT, 'Copyright'),
        (COPYLEFT, 'Copyleft'),
        (CREATIVE_COMMONS, 'Creative Commons')
    )

    name = models.CharField(max_length=150)
    url = models.URLField()
    description = models.TextField(blank=True) # permite estar vacío
    created_at = models.DateTimeField(auto_now_add=True) # cuando se crea, se pone a NOW()
    modified_at = models.DateTimeField(auto_now_add=True, auto_now=True) # cuando se crea o modifica, se pone a NOW()
    license = models.CharField(max_length=3, choices=LICENSES)

    def __unicode__(self):
        return self.name