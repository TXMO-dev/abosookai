from django.db import models
from django.contrib.auth.models import AbstractBaseUser, \
                                       BaseUserManager, \
                                       PermissionsMixin
from django.conf import settings


# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """Creates and saves a new user..."""
        if not email:
            raise ValueError("User must have an email")
        elif not password:
            raise ValueError("User must have a password")
        user = self.model(email=self.normalize_email(email[0]), **extra_fields)   
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """ Custom user model that supports emails instead of my username"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255,default="foobar")
    user_type = models.CharField(max_length=255,default="foobar")
    address = models.CharField(max_length=255,default="foobar")
    city = models.CharField(max_length=255,default="foobar2")
    state = models.CharField(max_length=255,default="foobar3")
    zip = models.CharField(max_length=255,default="foobar")   
    description = models.TextField(max_length=255,default="foobar")
    following = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="follow")
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)             
    objects = UserManager()
    USERNAME_FIELD = 'email' 

    def get_following(self):
        return ",".join([str(follow) for follow in self.following.all()])       

    def __str__(self):  
       return self.name                  