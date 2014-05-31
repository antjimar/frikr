# -*- coding: utf-8 -*-
from django import forms
from models import Photo

class LoginForm(forms.Form):
    """
    Formulario de login
    """
    user_username = forms.CharField(label="Nombre de usuario")
    user_password = forms.CharField(label="Contraseña", widget=forms.PasswordInput() )


class PhotoForm(forms.ModelForm):

    class Meta:
        model = Photo
        fields = ('name', 'url', 'description', 'license', 'visibility')


    # from http://goo.gl/G2nCu7
    BADWORDS = (u'diseñata', u'limpiatubos', u'abollao', u'abrazafarolas')

    def clean(self):
        cleaned_data = super(PhotoForm, self).clean() # llamada a super
        description = cleaned_data.get('description', '')
        for badword in self.BADWORDS:
            if badword in description:
                raise forms.ValidationError(unicode(badword) + u' no está permitido')

        return cleaned_data # aquí siempre tenemos que devolver







