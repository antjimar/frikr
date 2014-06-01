# -*- coding: utf-8 -*-
from rest_framework.views import APIView
from django.contrib.auth.models import User
from serializers import UserSerializer, PhotoSerializer
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from models import Photo
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView



class UserListAPI(APIView):

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
        user = get_object_or_404(User, pk=pk) # recuperamos el User por pk si no encuentra lanza un 404
        serializer = UserSerializer(user)
        return Response(serializer.data)


    def put(self, request, pk):
        """
        Actualiza un usuario
        """
        user = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(user, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED) # 202 ACCEPTED
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) # 400 BAD REQUEST


    def delete(self, request, pk):
        """
        Elimina un usuario
        """
        user = get_object_or_404(User, pk=pk)
        user.delete()
        return Response({}, status=status.HTTP_204_NO_CONTENT) # 204 NO CONTENT




class PhotoListAPI(ListCreateAPIView):
    """
    API con endpoints de listado y creación de fotos
    """
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer


class PhotoDetailAPI(RetrieveUpdateDestroyAPIView):
    """
    API con endpoints de detalle, actualización y borrado
    """
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer




