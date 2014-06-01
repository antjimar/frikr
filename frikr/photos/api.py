# -*- coding: utf-8 -*-
from rest_framework.views import APIView
from django.contrib.auth.models import User
from serializers import UserSerializer, PhotoSerializer, PhotoListSerializer
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from models import Photo
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, GenericAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from permissions import UserPermission
from django.db.models import Q



class UserListAPI(APIView):

    permission_classes = (UserPermission,)

    def get(self, request):
        """
        Lista los usuarios del sistema
        """
        users = User.objects.all()
        serializer = UserSerializer(users, many=True) # many = True porque pasamos un listado y no un solo modelo
        return Response(serializer.data)

    def post(self, request):
        """
        Crea un usuario
        """
        serializer = UserSerializer(data=request.DATA) # use DATA instead of POST
        if serializer.is_valid():
            new_user = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED) # 201 CREATED
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) # 400 BAD REQUEST



class UserDetailAPI(APIView):


    def get(self, request, pk):
        """
        Devuelve el detalle de un usuario
        """
        user = get_object_or_404(User, pk=pk)  # recuperamos el User por pk si no encuentra lanza un 404
        if request.user.is_superuser or request.user == user:
            serializer = UserSerializer(user)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
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

    def delete(self, request, pk):
        """
        Elimina un usuario
        """
        user = get_object_or_404(User, pk=pk)
        if request.user.is_superuser or request.user == user:
            user.delete()
            return Response({}, status=status.HTTP_204_NO_CONTENT) # 204 NO CONTENT
        else :
            return Response(status=status.HTTP_404_NOT_FOUND)


class PhotoAPIQueryset:

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



class PhotoListAPI(PhotoAPIQueryset, ListCreateAPIView):
    """
    API con endpoints de listado y creación de fotos
    """
    queryset = Photo.objects.all()
    serializer_class = PhotoListSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


    def get_serializer_class(self):
        return PhotoSerializer if self.request.method == "POST" else PhotoListSerializer


    def pre_save(self, obj):
        """
        Asigna el autor de la foto antes de ser creada
        """
        obj.owner = self.request.user


class PhotoDetailAPI(PhotoAPIQueryset, RetrieveUpdateDestroyAPIView):
    """
    API con endpoints de detalle, actualización y borrado
    """
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)




