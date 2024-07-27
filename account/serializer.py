from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    class Meta:
        model =User
        fields = '__all__'
