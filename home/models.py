from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin , BaseUserManager
from django.utils.translation import gettext_lazy as _
from datetime import date

# Create your models here.
#manually 



class UserManager(BaseUserManager):

    def create_superuser(self, email, user_name, first_name, password, **extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault('is_active',True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('superuser must be assigned to is_staff=True'))

        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('superuser must be assigned to is_staff=True'))

        if extra_fields.get('is_active') is not True:
            raise ValueError(_('superuser must be assigned to is_active=True'))

        return self.create_user(email, user_name, first_name, password, **extra_fields)

    def create_user(self, email, user_name, first_name, password, **extra_fields):

        if not email:
            raise ValueError(_('You must provide an email address'))

        extra_fields.setdefault('is_active',True)
        email = self.normalize_email(email)
        user = self.model(email=email, user_name=user_name, first_name=first_name, **extra_fields)
        user.set_password(password)
        user.save()
        return user

class User(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(_('email address'), unique = True)
    user_name = models.CharField(max_length = 30, blank = True, null = True, unique = True)
    first_name = models.CharField(max_length = 30,blank=True)
    last_name = models.CharField(max_length = 30,blank=True,default="")
    occupation = models.CharField(max_length = 30,blank=True,default='',null=True)
    facebook = models.CharField(max_length = 300,blank=True,default="")
     
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = 'user_name'
    REQUIRED_FIELDS = ['email', 'first_name']
    objects=UserManager()

    def __str__(self):
        return self.email

class Feedback(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    text = models.TextField()
    date = models.DateField()

    def __str__(self):
        return self.name


class Task(models.Model):
    priority_choices = (
        ("0","none"),
        ("1","low"),
        ("2","medium"),
        ("3","high")
    )
    status_choices=(
        (False,"pending"),
        (True,"completed")
    )
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=100,blank=False)
    due_date = models.DateField(default=date.today)
    desc = models.TextField(blank=True)
    priority = models.CharField(max_length=1,choices=priority_choices,default="0")
    status = models.BooleanField(choices=status_choices,default=False)

    def __str__(self):
        return self.title




