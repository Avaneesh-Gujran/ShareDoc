# forms.py
from django import forms

from .models import Document
from .models import User

class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Password")

    class Meta:
        model = User
        fields = ['name', 'email', 'phone_number', 'password']

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['title', 'content']