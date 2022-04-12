from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.utils import timezone
from django.utils.decorators import method_decorator
from extra_views import InlineFormSetView, ModelFormSetView

from print.models import Machine, MachineCategory

# views
from utilities.forms import MachineForm


def index(response):
    return render(response, "main/base.html", {})


def home(response):
    return render(response, "main/home.html", {})


@method_decorator(staff_member_required, name="dispatch")
class MachineListView(ModelFormSetView):
    model = Machine
    form_class = MachineForm
    paginate_by = 100
    template_name = "main/manage.html"
    fields = ["id", "Name", "Status", "DomainName", "ApiKey", "Location", "Description"]


def register(response):
    if response.method == "POST":
        form = UserCreationForm(response.POST)
        if form.is_valid():
            form.save()
    else:
        form = UserCreationForm()

    return render(response, "registration/register.html", {"form": form})
