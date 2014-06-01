from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from models import Photo



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



class PhotoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Photo













