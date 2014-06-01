# -*- coding: utf-8 -*-
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from models import Photo
from django.db.models import Q



class UserSerializer(serializers.Serializer):

    id = serializers.Field() # read only
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    username = serializers.CharField()
    email = serializers.CharField()
    password = serializers.CharField()


    def restore_object(self, attrs, instance=None):
        """
        Crea o actualiza una instancia de User a partir de
        los datos de attrs que contiene valores deserializados
        """
        if instance is None:
            instance = User()

        instance.first_name = attrs.get('first_name')
        instance.last_name = attrs.get('last_name')
        instance.username = attrs.get('username')
        instance.email = attrs.get('email')
        instance.password = make_password(attrs.get('password')) # encriptamos la password

        return instance


    def validate(self, attrs):
        """
        Valida si ya existe el usuario en el sistema
        """
        username = attrs.get('username')
        email = attrs.get('email')
        # SELECT * FROM users WHERE username = 'username' OR email = 'email'
        existent_users = User.objects.filter(Q(username=username) | Q(email=email))
        if len(existent_users) > 0:
            raise serializers.ValidationError(u"Ya existe un usuario con ese nombre de usuario y/o e-mail registrado")

        return attrs


class PhotoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Photo


    # from http://goo.gl/G2nCu7
    BADWORDS = (u'diseñata', u'limpiatubos', u'abollao', u'abrazafarolas')

    def validate_description(self, attrs, source):
        """
        Valida que la descripción no tiene tacos
        :param attrs: diccionario con todos los atributos
        :param source: nombre del atributo a validar
        :return: diccionario con atributos
        """
        description = attrs.get(source)
        for badword in self.BADWORDS:
            if badword in description:
                raise serializers.ValidationError(badword + u" no es una palabra permitida")
        return attrs


class PhotoListSerializer(PhotoSerializer):

    class Meta(PhotoSerializer.Meta):
        fields = ('id', 'owner', 'name', 'url')










