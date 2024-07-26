import traceback
from django.shortcuts import get_object_or_404, render
from django.contrib.auth import authenticate,login
from django.core.exceptions import ValidationError

from rest_framework.views import APIView 

from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
# from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User

from logic_app.models import Officedetail, Register, Userdetail
from logic_app.serializer import UserSerializer,LoginSerializer,UserLoginSerializer

# Create your views here.
class UserLogin(APIView):
    def post(self,request):
        data = request.data
        username = data['username']
        password = data['password']
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(username=username,password=password)
        if user is not None:
            request.data['username']=user.username
            refresh = RefreshToken.for_user(user)
            token = {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    }
            return Response({"msg":"Login successfully","tokens": token},status=status.HTTP_200_OK)






class UserView(APIView):
    def post(self, request):
        try:
            data = request.data
            email = data.get('email')
            password = data.get('password')
            if Register.objects.filter(email=email).exists():
                return Response("Email is already exist",status=status.HTTP_207_MULTI_STATUS)
            user = Register.objects.create(email=email, password=password)
            user_details = data.get('details',[])
            for details in user_details:
                name = details.get('name')
                age = details.get('age')
                address = details.get('address')
                userdata=Userdetail.objects.create(user=user, name=name, age=age, address=address)
            office_detail = data.get("office",[])
            for office_details in office_detail:
                companyname = office_details.get('companyname')
                city = office_details.get('city')
                office = Userdetail.objects.get(name=office_details['office'])
                officedata = Officedetail.objects.create(office=office,companyname=companyname,city=city)  
            return Response({"message": "User created successfully"}, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def get(self,request,format=None,id=None):  
        if id is None:
            users = Register.objects.all()
            serializer = UserSerializer(users,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            users = Register.objects.get(id=id)
            serializer = UserSerializer(users)
            return Response(serializer.data,status=status.HTTP_200_OK)
        
    def put(self,request,id):
        try:
            # breakpoint()
            data = request.data
            user = Register.objects.filter(id=id).update(
            email = data['email'],
            password = data["password"]
            )
            # breakpoint()
            user_data = Register.objects.get(id=id)

            for details in data['details']:  
                userdata=Userdetail.objects.filter(id=details['id']).update(
                user =user_data,
                name = details['name'],
                age = details['age'],
                address = details['address']
                )
            
            for offices in data['offices']:
                officedata = Officedetail.objects.filter(id=offices['id']).update(
                office = Userdetail.objects.get(name=offices['name']),
                companyname = offices['companyname'],
                city = offices['city']
                )
            return Response({"message":"Details Updated"},status=status.HTTP_200_OK)   
        except Exception:
            return Response(traceback.format_exc(),status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,id=None,format=None):
        user = Register.objects.get(id=id)
        user.delete()
        return Response({"Message":"User Deleted Successfully"},status=status.HTTP_205_RESET_CONTENT)

  
        
class LoginView(APIView):
    permission_classes = []
    def post(self, request):    
        data=request.data
        email = data['email']   
        password = data['password']
        user = Register.objects.get(email=email,password=password)
        if user is not None:
            request.data['email']=user.email
            refresh = RefreshToken.for_user(user)
            token = {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    }
            return Response({"msg":"Login successfully","tokens": token},status=status.HTTP_200_OK)
        
        else:
            return Response({"msg":"Invalid Email or Password"},status=status.HTTP_400_BAD_REQUEST)










        # except:
        # data=request.data
        # email = data['email']   
        # password = data['password']
        # user = authenticate(email=email, password=password)
        # breakpoint()
        # if user is not None:
            
        #     serializer = LoginSerializer(data=request.data)
        #     if serializer.is_valid(raise_exception=True):
        #         refresh = RefreshToken.for_user(user)
        #         token = {
        #             'refresh': str(refresh),
        #             'access': str(refresh.access_token),
        #             }
        #     return Response({"message": "Login Successful", "tokens": token}, status=status.HTTP_202_ACCEPTED)
        # else:
        #     return Response({"error" : "something wrong"}, status=status.HTTP_400_BAD_REQUEST)

            
            
    # def post(self, request): 
    #     try:   
    #         data = request.data
    #         email = data.get('email')
    #         password = data('password')    
    #         user = Register.objects.get(email=email,password=password)
    #         if user is not None:
    #             request.data['email'] = user.email
    #             return Response({"Message":"Login Successfully"},status=status.HTTP_202_ACCEPTED)
    #     except Register.DoesNotExist:
    #         return Response("User Does Not Exist",status=status.HTTP_404_NOT_FOUND)    

#    serializer = LoginSerializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             user = serializer.validated_data['user'] 
#             refresh =RefreshToken.for_user(user)
#             token = {
#                 'refresh':str(refresh),
#                 'access':str(refresh.access_token)
#             }
   
        
# class UserView(APIView):
#     def post(self, request):
#         try:
#             data = request.data
#             print("data=",data)

#             email = data.get('email')
#             print("email=",email)
#             password = data.get('password')
#             print("password =",password )
        
#             if Users.objects.filter(email=email).exists():
#                 return Response("Email is already exist",status=status.HTTP_207_MULTI_STATUS)

#             user = Users.objects.create(email=email, password=password)
#             print("data=",data)

#             user_details = data.get('userdetail',[])
#             print("user=",user)

#             detail=[]
#             print("detail=",detail)

#             for details in user_details:
#                 name = details.get('name')
#                 age = details.get('age')
#                 address = details.get('address')
    
#                 userdata=Userdetail.objects.create(user=user, name=name, age=age, address=address)
#                 print("userdata=",userdata)

#                 detail.append
#                 (
#                     {
#                         "id":userdata.id,
#                         "name":userdata.name,
#                         "age":userdata.age,
#                         "address":userdata.address
#                     }
#                 )

              
#             office_detail = data.get("officedetail",[])
#             print("office_detail=",office_detail)

#             office_data = []  
#             print("office_data=",office_data)

#             for office_detail in office_detail:
#                 companyname = office_detail.get('companyname')
#                 city = office_detail.get('city')

#                 officedata = Officedetail.objects.create(office=userdata,companyname=companyname,city=city)  
#                 print("officedata =",officedata )
                
#                 office_data.append
#                 (
#                     {
#                         "id":officedata.id,
#                         "companyname":officedata.companyname,
#                         "city":officedata.city
#                     }
#                 )  
                
#             return Response({"message": "User created successfully"}, status=status.HTTP_200_OK)
#         except ValidationError as e:
#             return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


# def put(self, request, id=None, format=None):
    #     data = request.data
        
    #     try:
    #         user = Users.objects.get(id=id)
    #     except Users.DoesNotExist:
    #         return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    #     user.email = data.get("email", user.email)
    #     user.password = data.get("password", user.password)
    #     user.save()

    #     user_detail = data.get("userdetail", [])
    #     for details in user_detail:
    #         if 'id' in details:
    #             try:
    #                 userdetail = Userdetail.objects.get(id=details['id'], user=user)
    #             except Userdetail.DoesNotExist:
    #                 return Response({"error": "Userdetail with id {} not found".format(details['id'])}, status=status.HTTP_404_NOT_FOUND)
    #         else:
    #             userdetail = Userdetail(user=user)

    #         userdetail.name = details.get("name", userdetail.name)
    #         userdetail.age = details.get("age", userdetail.age)
    #         userdetail.address = details.get("address", userdetail.address)
    #         userdetail.save()

    #     office_detail = data.get("officedetail", [])
    #     for office_details in office_detail:
    #         if 'id' in office_details:
    #             try:
    #                 officedetail = Officedetail.objects.get(id=office_details['id'], user=user)
    #             except Officedetail.DoesNotExist:
    #                 return Response({"error": "Officedetail with id {} not found".format(office_details['id'])}, status=status.HTTP_404_NOT_FOUND)
    #         else:
    #             officedetail = Officedetail(user=user)
    #         officedetail.user = user  
    #         officedetail.companyname = office_details.get("companyname", officedetail.companyname)
    #         officedetail.city = office_details.get("city", officedetail.city)
    #         officedetail.save()

    #     return Response({"message": "Details Updated"}, status=status.HTTP_200_OK)    






