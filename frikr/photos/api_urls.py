from django.conf.urls import patterns, url, include
import api
from rest_framework.routers import DefaultRouter


# Creamos un router y registramos el viewset de Photos
photo_router = DefaultRouter()
photo_router.register(r'photos', api.PhotoViewSet)

# Router de viewset de usuario
user_router = DefaultRouter()
user_router.register(r'users', api.UserViewSet, base_name='user')

urlpatterns = patterns('',

    # Users API
    url(r'', include(user_router.urls)),

    # Photos API
    url(r'', include(photo_router.urls)),

    # Upload photo URL
    url(r'^upload$', api.UploadPhotoAPI.as_view())
)