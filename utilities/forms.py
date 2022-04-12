from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from extra_views import ModelFormSetView

from print.models import Machine


class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class MachineForm(ModelForm):
    fields = ["id", "Status", "Name", "HostName", "Location", "Description"]
