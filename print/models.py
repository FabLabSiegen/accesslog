from django.db import models
from django.contrib.auth.models import User

class SafetyBriefing(models.Model):
    kind = models.TextField(max_length=500)
    validity_period = models.IntegerField()
    document = models.BinaryField()