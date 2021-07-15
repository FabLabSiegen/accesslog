from django.db import models
from django.contrib.auth.models import User

class Print(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    datetime = models.DateField()

class Printer(models.Model):
    print = models.ForeignKey(Print, on_delete=models.CASCADE)
    printing = models.BooleanField()

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    print = models.ForeignKey(Print, on_delete=models.CASCADE)
    comment = models.TextField(max_length=500)
    rating = models.IntegerField()