# -*- coding: utf-8 -*-
from rest_framework.permissions import BasePermission


class UserPermission(BasePermission):

    def has_permission(self, request, view):
        """
        Queremos que:
            - Sólo los administradores puedan ver el listado o detalle de cualquier usuario (GET)
            - Cualquiera pueda crear un usuario (para que se registren) (POST)
            - Sólo pueden ver el detalle de los usuarios si accedes a tu mismo usuario (ver mi perfil)
            - Si eres un administrador, puedes ver el detalle de cualquier usuario
        Define si tiene permiso para ejecutar esta acción
        :param request: petición recibida
        :param view: vista que se está ejecutando
        :return: boolean
        """

        if request.method == "POST":
            return True
        elif request.user.is_superuser:
            return True
        else:
            return False