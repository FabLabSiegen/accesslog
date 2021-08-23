from django.db import models
from django.contrib.auth.models import User

class SafetyBriefing(models.Model):
    kind = models.TextField(max_length=500)
    validity_period = models.IntegerField()
    document = models.BinaryField()

class FabLabUser(models.Model):
    name = models.TextField(max_length=100)
    email = models.TextField(max_length=200)
    registered = models.DateTimeField()
    rfid_uuid = models.IntegerField()
    safety_briefings = models.ManyToManyField(SafetyBriefing)
