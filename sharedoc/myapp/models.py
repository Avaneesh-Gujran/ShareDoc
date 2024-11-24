from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
# Create your models here.

import uuid
from uuid import uuid4



class Document(models.Model):
    title = models.CharField(max_length=255, default="Untitled Document")
    content = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    version = models.PositiveIntegerField(default=0)
    #owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='owned_documents',null=True)
    #shared_with = models.ManyToManyField(CustomUser, related_name='shared_documents', blank=True) 

class Cursor(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='cursors')
    user_id = models.CharField(max_length=255)  # Unique user identifier
    cursor_position = models.IntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)


from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, email, name, phone_number, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        user = self.model(
            email=self.normalize_email(email),
            name=name,
            phone_number=phone_number,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15, unique=True)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'phone_number']

    objects = UserManager()

    def __str__(self):
        return self.email
