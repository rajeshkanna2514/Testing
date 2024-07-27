from django.urls import path
from logic_app.views import UserView,LoginView,UserLogin
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [

    path('register/',UserView.as_view(),name='register'),
    path('register/<int:id>/',UserView.as_view(),name='register'),
    path('login/',LoginView.as_view(),name='login'),
    
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
   
]