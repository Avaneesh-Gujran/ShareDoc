from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
# Create your models here.

import uuid
from uuid import uuid4

class CustomUser(AbstractUser):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    

    REQUIRED_FIELDS = ['email', 'phone_number', 'name']  # Fields required in addition to username

    def __str__(self):
        return self.username

class Document(models.Model):
    title = models.CharField(max_length=255, default="Untitled Document")
    content = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    #owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='owned_documents',null=True)
    #shared_with = models.ManyToManyField(CustomUser, related_name='shared_documents', blank=True) 

class Cursor(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='cursors')
    user_id = models.CharField(max_length=255)  # Unique user identifier
    cursor_position = models.IntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)




