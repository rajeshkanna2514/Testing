from django.db import models




# Create your models here.
class Register(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=20)

    def __str__(self):
        return self.email

class Userdetail(models.Model):
    
    user = models.ForeignKey(Register,on_delete=models.CASCADE,related_name='details')
    name = models.CharField(max_length=50,null=True)
    age = models.IntegerField()
    address = models.CharField(max_length=100,null=True)


    def __str__(self):
        return self.name    
    
class Officedetail(models.Model):

    office = models.ForeignKey(Userdetail,on_delete=models.CASCADE,related_name='offices')
    companyname = models.CharField(max_length=50,null=True)
    city = models.CharField(max_length=100,null=True)

    def __str__(self):
        return self.companyname
        