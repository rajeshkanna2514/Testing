from django.contrib import admin
from .models import Register,Userdetail,Officedetail


class UserAdmin(admin.ModelAdmin):

    list_display=('email','password')

admin.site.register(Register,UserAdmin)    

class UserdetailAdmin(admin.ModelAdmin):

    list_display=('name','age','address','user')

admin.site.register(Userdetail,UserdetailAdmin)

class OfficedetailAdmin(admin.ModelAdmin):

    list_display=('companyname','city','office')

admin.site.register(Officedetail,OfficedetailAdmin)
    


