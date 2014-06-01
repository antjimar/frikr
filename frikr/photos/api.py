# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from serializers import UserSerializer, PhotoSerializer, PhotoListSerializer, PhotoFileSerializer
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from models import Photo, PhotoFile
from rest_framework.generics import CreateAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django.db.models import Q
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework import filters
from django.core.mail import send_mail
from settings import SENDER_EMAIL
from django.conf import settings


class UserViewSet(ViewSet):


    def list(self, request): # GET del listado
        """
        Lista los usuarios del sistema
        """
        if request.user.is_superuser:
            users = User.objects.all()
            serializer = UserSerializer(users, many=True) # many = True porque pasamos un listado y no un solo modelo
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


    def create(self, request): # POST
        """
        Crea un usuario
        """
        serializer = UserSerializer(data=request.DATA) # use DATA instead of POST
        if serializer.is_valid():
            new_user = serializer.save()

            message = u"Tu usuario es: " + new_user.username + u" tú sabrás cual es tu password."
            send_mail(u"Bienvenido a Frikr!", message, SENDER_EMAIL, [new_user.email], fail_silently=(not settings.DEBUG))

            return Response(serializer.data, status=status.HTTP_201_CREATED) # 201 CREATED
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) # 400 BAD REQUEST



    def retrieve(self, request, pk): # GET del detalle
        """
        Devuelve el detalle de un usuario
        """
        user = get_object_or_404(User, pk=pk)  # recuperamos el User por pk si no encuentra lanza un 404
        if request.user.is_superuser or request.user == user:
            serializer = UserSerializer(user)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


    def update(self, request, pk): # PUT
        """
        Actualiza un usuario
        """
        user = get_object_or_404(User, pk=pk)
        if request.user.is_superuser or request.user == user:
            serializer = UserSerializer(user, data=request.DATA)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_202_ACCEPTED) # 202 ACCEPTED
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) # 400 BAD REQUEST
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


    def destroy(self, request, pk): # DELETE
        """
        Elimina un usuario
        """
        user = get_object_or_404(User, pk=pk)
        if request.user.is_superuser or request.user == user:
            user.delete()
            return Response({}, status=status.HTTP_204_NO_CONTENT) # 204 NO CONTENT
        else :
            return Response(status=status.HTTP_404_NOT_FOUND)



class PhotoViewSet(ModelViewSet):

    queryset = Photo.objects.all()
    serializer_class = PhotoListSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_backends = (filters.DjangoFilterBackend, filters.OrderingFilter,)
    filter_fields = ('name', 'license', 'visibility')
    ordering_fields = ('id', 'name', 'owner')

    def get_queryset(self) :
        """
        Si es superusuario, accede a todo
        Si no es superusuario y está autentciado, accede a lo suyo y a lo público del resto
        Si no está autenticado, sólo ve lo público
        """
        if self.request.user.is_superuser :
            return Photo.objects.all()
        elif self.request.user.is_authenticated() :
            return Photo.objects.filter(Q(owner=self.request.user) | Q(visibility=Photo.VISIBILITY_PUBLIC))
        else :
            return Photo.objects.filter(visibility=Photo.VISIBILITY_PUBLIC)


    def get_serializer_class(self) :
        return PhotoSerializer if self.action == "create" else PhotoListSerializer


    def pre_save(self, obj) :
        """
        Asigna el autor de la foto antes de ser creada
        """
        obj.owner = self.request.user



class UploadPhotoAPI(ListCreateAPIView):

    queryset = PhotoFile.objects.all()
    serializer_class = PhotoFileSerializer
    permission_classes = (IsAuthenticated,)