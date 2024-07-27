from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated,AllowAny


from .models import User
from .serializer import UserSerializer


class UserView(APIView):
    permission_classes = []
    def post(self,request):
        email = request.data.get('email')
        username =request.data.get('username')
        password = request.data.get('password')
        if email is None:
            return Response({"error":"Enter requierd email"},status=status.HTTP_400_BAD_REQUEST)
        if email and username and password:
            try:
                user = User.objects.create(email=email,username=username,password=password)
                user.is_admin = False
                user.is_active=False
                user.is_staff=False
                user.is_superadmin=False
                user.save(using = self.request._db)

                return Response({"user_createdseccessfully"},status=status.HTTP_201_CREATED)
            except :
                return Response({"user_createdseccessfully"},status=status.HTTP_204_NO_CONTENT)
        else :
            return Response({"user Does not exist"},status=status.HTTP_400_BAD_REQUEST)
        
    def get(self,request,id=None,format=None):
        if id is None:
            users = User.objects.all()
            serializer = UserSerializer(users,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        else :
            users = User.objects.get(id=id)
            serializer = UserSerializer(users)
            return Response(serializer.data,status=status.HTTP_200_OK)
        
    def put(self,request,id =id):
        data= request.data
        username = data['username']
        email = data['email']
        password = data['password']
        is_staff = data['is_staff']
        userdata = User.objects.filter(id=id).update(
            email=email,
            username = username,
            password=password,
            is_staff = is_staff
        )
        return Response({"Details Updated"},status=status.HTTP_200_OK)

    def delete(self,request,id,format=None):
        user = User.objects.get(id=id)
        user.delete()
        return Response ({"Deleted Successfully"},status=status.HTTP_205_RESET_CONTENT)      

class LoginUser(APIView):
    permission_classes=[AllowAny]
    def post(self,request,format=None):
        try:
            data = request.data
            email = data['email']
            password = data['password']
           
            user = User.objects.get(email=email,password=password)
            if user is not None:
                request.data['email']=user.email
                refresh = RefreshToken.for_user(user)
                token = {
                    'refresh':str(refresh),
                    'access':str(refresh.access_token)
                }
                return Response({"msg":"Login success","token":token},status=status.HTTP_200_OK)
        except User.DoesNotExist:    
            return Response({"msg":"Invalid Email or Password"},status=status.HTTP_400_BAD_REQUEST)
        

    

    


