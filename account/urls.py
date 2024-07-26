from django.urls import path
from account.views import UserView,LoginUser

urlpatterns=[
    path('api/user/',UserView.as_view(),name='user'),
    path('api/user/<int:id>/',UserView.as_view(),name='userid'),
    path('login/',LoginUser.as_view(),name='login'),
    
]