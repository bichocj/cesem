from rest_framework import viewsets
from django.contrib.auth.models import User
from .utils import BasePathSerializer

class UserPathSerializer(BasePathSerializer):

    @staticmethod
    def get_path():
        return 'users'
    
    class Meta:
        model = User
        fields = ['username', 'url']

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserPathSerializer