from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]

class SafetyBriefing(models.Model):
    Kind = models.TextField(max_length=500)
    ValidityPeriod = models.IntegerField()
    Document = models.FileField()

class FabLabUser(models.Model):
    Name = models.TextField(max_length=100)
    Email = models.EmailField(max_length=200)
    RfidUuid = models.IntegerField()
    CanBrief = models.BooleanField()
    SafetyBriefings = models.ManyToManyField(SafetyBriefing, through='UserIsBriefed', through_fields=('Recipient','SafetyBriefing'))
    User = models.OneToOneField(User, on_delete=models.CASCADE)

class UserIsBriefed(models.Model):
    Recipient = models.ForeignKey(FabLabUser, related_name='Recipient', on_delete=models.CASCADE)
    SafetyBriefing = models.ForeignKey(SafetyBriefing, on_delete=models.CASCADE)
    Date = models.DateTimeField()
    Instructor = models.ForeignKey(User, related_name='Instructor', on_delete=models.SET(get_sentinel_user), default=None)

class MachineCategory(models.Model):
    Name = models.TextField()

class Machine(models.Model):
    Category = models.ForeignKey(MachineCategory, on_delete=models.SET_NULL, null=True)
    Status = models.TextField()
    Name = models.TextField()
    HostName = models.TextField()
    Location = models.TextField()
    Description = models.TextField()
    User = models.ManyToManyField(User, through='AssignedUsers')

class AssignedUsers(models.Model):
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    Machine = models.ForeignKey(Machine, on_delete=models.CASCADE)

class ThreeDimensionalModel(models.Model):
    File = models.FileField(upload_to='models')
    Owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='Owner')
    Uploaded = models.DateTimeField()
    Previous = models.ForeignKey("self", on_delete=models.SET_NULL, default=None, null=True)
    SharedWithUser = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='SharedWithUser')

class GCode(models.Model):
    ThreeDimensionalModel = models.ForeignKey(ThreeDimensionalModel, on_delete=models.SET_NULL, null=True, default=None)
    FileLocation = models.FilePathField()
    EstimatedPrintingTime = models.TimeField()
    UsedFilamentInG = models.FloatField()
    UsedFilamentInMm = models.FloatField()
    Uploaded = models.DateTimeField()
    SharedWithUser = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

class PrintJob(models.Model):
    User = models.ForeignKey(User, on_delete=models.SET(get_sentinel_user))
    Machine = models.ForeignKey(Machine, on_delete=models.SET_NULL, null=True)
    GCode = models.ForeignKey(GCode, on_delete=models.SET_NULL, null=True)
    Start = models.DateTimeField()
    End = models.DateTimeField()
    State = models.IntegerField()

class PrintTemperatureHistory(models.Model):
    PrintJob = models.ForeignKey(PrintJob, on_delete=models.CASCADE)
    ToolTarget = models.FloatField()
    ToolActual = models.FloatField()
    BedTarget = models.FloatField()
    BedActual = models.FloatField()
    TimeStamp = models.DateTimeField()

class PrintMediaFile(models.Model):
    PrintJob = models.ForeignKey(PrintJob, on_delete=models.CASCADE)
    FileLocation = models.FilePathField()
    Description = models.TextField()

class SlicingConfig(models.Model):
    GCode = models.ForeignKey(GCode,on_delete=models.CASCADE)
    ConfigLocation = models.FilePathField()

class Rating(models.Model):
    User = models.ForeignKey(User, on_delete=models.SET(get_sentinel_user))
    PrintJob = models.ForeignKey(PrintJob, on_delete=models.CASCADE)
    Comment = models.TextField(max_length=500)
    Rating = models.IntegerField()