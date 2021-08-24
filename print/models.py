from django.db import models
from django.contrib.auth.models import User

class SafetyBriefing(models.Model):
    kind = models.TextField(max_length=500)
    validity_period = models.IntegerField()
    document = models.FileField()

class FabLabUser(models.Model):
    name = models.TextField(max_length=100)
    email = models.EmailField(max_length=200)
    rfid_uuid = models.IntegerField()
    can_brief = models.BooleanField()
    safety_briefings = models.ManyToManyField(SafetyBriefing, through='UserIsBriefed', through_fields=('recipient','safety_briefing'))
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class UserIsBriefed(models.Model):
    recipient = models.ForeignKey(FabLabUser, related_name='recipient', on_delete=models.CASCADE)
    safety_briefing = models.ForeignKey(SafetyBriefing, on_delete=models.CASCADE)
    date = models.DateTimeField()
    instructor = models.ForeignKey(FabLabUser, related_name='instructor', on_delete=models.CASCADE, default=None)

class MachineCategory(models.Model):
    name = models.TextField()

class Machine(models.Model):
    category = models.ForeignKey(MachineCategory, on_delete=models.SET_NULL, null=True)
    status = models.TextField()
    name = models.TextField()
    host_name = models.TextField()
    location = models.TextField()
    description = models.TextField()

class Model(models.Model):
    file = models.FilePathField()
    owner = models.ForeignKey(FabLabUser, on_delete=models.SET_NULL, null=True)
    uploaded = models.DateTimeField()
    previous = models.ForeignKey("self", on_delete=models.SET_NULL, default=None, null=True)

class GCode(models.Model):
    model = models.ForeignKey(Model, on_delete=models.CASCADE)
    file_location = models.FilePathField()
    estimated_printing_time = models.TimeField()
    used_filament_in_g = models.FloatField()
    used_filament_in_mm = models.FloatField()
    uploaded = models.DateTimeField()

class PrintJob(models.Model):
    user = models.ForeignKey(FabLabUser, on_delete=models.SET_NULL, null=True)
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    g_code = models.ForeignKey(GCode, on_delete=models.SET_NULL, null=True)
    start = models.DateTimeField()
    end = models.DateTimeField()
    state = models.IntegerField()

class PrintTemperatureHistory(models.Model):
    print_job = models.ForeignKey(PrintJob, on_delete=models.CASCADE)
    tool_target = models.FloatField()
    tool_actual = models.FloatField()
    bed_target = models.FloatField()
    bed_actual = models.FloatField()
    timestamp = models.DateTimeField()

