from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.base_user import BaseUserManager
from django.core.validators import MinLengthValidator



# Create your models here.
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_("The Email field must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        
        return self.create_user(email, password, **extra_fields)
    
    

class User(AbstractUser):
    email=models.EmailField(max_length=225, unique=True)
    username=None
    password=models.CharField(max_length=225, validators=[MinLengthValidator(8)], null=False)
    first_name=models.CharField(max_length=225, null=False)
    last_name=models.CharField(max_length=225, null=False)
    image=models.URLField(max_length=500, null=False)
    
    objects=CustomUserManager()
    
    USERNAME_FIELD="email"
    REQUIRED_FIELDS=[]