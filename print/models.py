from django.db import models
from django.contrib.auth.models import User

class SafetyBriefing(models.Model):
    kind = models.TextField(max_length=500)
    validity_period = models.IntegerField()
    document = models.BinaryField()

class FabLabUser(models.Model):
    name = models.TextField(max_length=100)
    email = models.TextField(max_length=200)
    rfid_uuid = models.IntegerField()
    can_brief = models.BooleanField()
    safety_briefings = models.ManyToManyField(SafetyBriefing, through='UserIsBriefed',)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class UserIsBriefed(models.Model):
    recipient = models.ForeignKey(FabLabUser, on_delete=models.CASCADE)
    safety_briefings = models.ForeignKey(SafetyBriefing, on_delete=models.CASCADE)
    date = models.DateTimeField()
    instructor_id = models.IntegerField()


