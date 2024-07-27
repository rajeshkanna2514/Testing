from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import Register,Userdetail,Officedetail
from django.contrib.auth.models import User


class OfficeSerializer(serializers.ModelSerializer):
  
    class Meta:
        model = Officedetail
        fields =('companyname','city','office')

class UserdetailSerializer(serializers.ModelSerializer):
    offices = OfficeSerializer(many=True,read_only = True)

    class Meta:
        model = Userdetail
        fields =('name','age','address','user','offices')        

class UserSerializer(serializers.ModelSerializer):
    details = UserdetailSerializer(many=True,read_only = True)
  
    class Meta:
        model = Register
        fields = ('id','email','password','details')

class LoginSerializer(serializers.Serializer):
    
    email = serializers.EmailField(max_length=50)
    password = serializers.CharField(write_only=True)

    def validate(self,data):
        email=data.get('email')
        password = data.get('password')
        user = authenticate(email=email,password=password)
        return user
    
class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username','password')    
    
    
     


    