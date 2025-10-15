from django.db import models
from django.core.validators import validate_integer
from django.contrib.auth.models import AbstractBaseUser , PermissionsMixin
from django.core.exceptions import ValidationError
import re
from .managers import UserManager


def valid_phone_ir(value):
    pattern = r'^09\d{9}$'
    if not re.match(pattern , value) or len(value) != 11:
        raise ValidationError("شماره تلفن نامعتبر است")
    return value

class User(PermissionsMixin , AbstractBaseUser):
    phone = models.CharField(max_length=11 , unique=True , validators=[validate_integer,valid_phone_ir])
    is_support = models.BooleanField(default=False)
    is_user = models.BooleanField(default=True)

    USERNAME_FIELD = "phone"

    objects = UserManager()

    def __str__(self):
        return self.phone
        
    @property
    def is_staff(self):
        return self.is_support
    

class Provinces(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
class Cities(models.Model):
    name = models.CharField(max_length=50)
    province = models.ForeignKey(Provinces,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE , related_name='profile_user')
    email = models.EmailField(max_length=100 , null=True , blank=True ,db_index=True , unique=True)
    username = models.CharField(max_length=100 , null=True , blank=True)
    image = models.ImageField(upload_to='media/profiles/', null=True , blank=True)
    city = models.ForeignKey(Cities , on_delete=models.CASCADE , null=True , blank=True)
    province = models.ForeignKey(Provinces , on_delete=models.CASCADE , null=True , blank=True)

    def __str__(self):
        return self.user.phone

    