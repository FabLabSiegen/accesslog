
from django.shortcuts import render
from django.utils import timezone
from extra_views import ModelFormSetView, InlineFormSetView
from print.models import Machine, MachineCategory
from django.contrib.auth.forms import UserCreationForm

#views
from utilities.forms import MachineForm


def index(response):
    return render(response, "main/base.html", {});

def home(response):
    return render(response, "main/home.html", {});


class MachineListView(ModelFormSetView):
    model = Machine
    form_class = MachineForm
    paginate_by = 100
    template_name = 'main/manage.html'
    fields = ['id', 'Status', 'Name', 'HostName', 'Location', 'Description']
    data = {
        'form-TOTAL_FORMS': '1',
        'form-INITIAL_FORMS': '0',
        'form-MAX_NUM_FORMS': '',
        'form-0-title': '',
        'form-0-pub_date': '',
    }

def register(response):
    if response.method == "POST":
        form = UserCreationForm(response.POST)
        if form.is_valid():
            form.save()
    else:
        form = UserCreationForm()

    return render(response, "registration/register.html", {"form":form})