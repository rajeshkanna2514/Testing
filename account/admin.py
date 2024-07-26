from django.contrib import admin
from account.models import UserManager,User

class Useradmin(admin.ModelAdmin):
    list_display=('username','email','created_date','modefied_date','is_admin','is_staff','is_active','is_superadmin',)
admin.site.register(User,Useradmin)    

