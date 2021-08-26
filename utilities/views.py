from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm

#views
def index(response):
    return render(response, "main/base.html", {});

def home(response):
    return render(response, "main/home.html", {});

def register(response):
    if response.method == "POST":
        form = UserCreationForm(response.POST)
        if form.is_valid():
            form.save()
    else:
        form = UserCreationForm()

    return render(response, "registration/register.html", {"form":form})