from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]

class SafetyBriefing(models.Model):
    Kind = models.TextField(max_length=500)
    ValidityPeriod = models.IntegerField()
    Document = models.FileField(upload_to='safetybriefings')

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
    Status = models.CharField(max_length=100)
    Name = models.CharField(max_length=100)
    DomainName = models.CharField(max_length=100)
    Location = models.CharField(max_length=100)
    ApiKey = models.CharField(max_length=100)
    Description = models.TextField()
    User = models.ManyToManyField(User, through='AssignedUsers')

class AssignedUsers(models.Model):
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    Machine = models.ForeignKey(Machine, on_delete=models.CASCADE)

class ThreeDimensionalModel(models.Model):
    Name = models.TextField()
    FileName = models.TextField()
    Size = models.TextField()
    File = models.FileField(upload_to='models')
    Owner = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, related_name='ModelOwner')
    Uploaded = models.DateTimeField(auto_now_add=True)
    Previous = models.ForeignKey("self", on_delete=models.SET_NULL, default=None, null=True)
    SharedWithUser = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='SharedWithUser')

class GCode(models.Model):
    Name = models.TextField()
    FileName = models.TextField()
    Size = models.TextField()
    ThreeDimensionalModel = models.ForeignKey(ThreeDimensionalModel, on_delete=models.SET_NULL, null=True, default=None)
    File = models.FileField(upload_to='gcode')
    EstimatedPrintingTime = models.TimeField()
    UsedFilamentInG = models.FloatField()
    UsedFilamentInMm = models.FloatField()
    Owner = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, related_name='GcodeOwner')
    Uploaded = models.DateTimeField(auto_now_add=True)
    SharedWithUser = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)



class PrintJob(models.Model):
    User = models.ForeignKey(User, on_delete=models.SET(get_sentinel_user))
    Machine = models.ForeignKey(Machine, on_delete=models.SET_NULL, null=True)
    GCode = models.ForeignKey(GCode, on_delete=models.SET_NULL, null=True)
    Start = models.DateTimeField()
    End = models.DateTimeField(null=True)
    State = models.CharField(max_length=100)

class BedTemperatureHistory(models.Model):
    PrintJob = models.ForeignKey(PrintJob, on_delete=models.CASCADE)
    Target = models.FloatField()
    Actual = models.FloatField()
    TimeStamp = models.DateTimeField()

class ToolTemperatureHistory(models.Model):
    PrintJob = models.ForeignKey(PrintJob, on_delete=models.CASCADE)
    Target = models.FloatField()
    Actual = models.FloatField()
    TimeStamp = models.DateTimeField()

class PrintMediaFile(models.Model):
    PrintJob = models.ForeignKey(PrintJob, on_delete=models.CASCADE)
    File = models.FileField(upload_to='printmedia')
    Description = models.TextField()
    Owner = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, related_name='PrintMediaOwner')

class SlicingConfig(models.Model):
    GCode = models.ForeignKey(GCode,on_delete=models.CASCADE)
    Config = models.JSONField(null=False)

class Rating(models.Model):
    User = models.ForeignKey(User, on_delete=models.SET(get_sentinel_user))
    PrintJob = models.ForeignKey(PrintJob, on_delete=models.CASCADE)
    Comment = models.TextField(max_length=500)
    Rating = models.IntegerField()

class StartGCode(models.Model):
    Machine = models.ForeignKey(Machine, on_delete=models.SET_NULL, null=True)
    GCode = models.ForeignKey(GCode, on_delete=models.SET_NULL, null=True)
    Owner = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, related_name='StartGcodeOwner')

class StopGCode(models.Model):
    PrintJob = models.ForeignKey(PrintJob, on_delete=models.CASCADE)
    Owner = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, related_name='StopGcodeOwner')