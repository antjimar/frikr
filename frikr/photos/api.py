from django.views.generic import View
from django.contrib.auth.models import User
from serializers import UserSerializer
from rest_framework.renderers import JSONRenderer


class UserListAPI(View):

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True) # many = True porque pasamos un listado y no un solo modelo
        renderer = JSONRenderer()
        data = renderer.render(serializer.data) # renderizamos en JSON
        return HttpResponse(data)