# -*- coding: utf-8 -*-
from django import forms


class LoginForm(forms.Form):
    """
    Formulario de login
    """
    user_username = forms.CharField(label="Nombre de usuario")
    user_password = forms.CharField(label="Contraseña", widget=forms.PasswordInput() )