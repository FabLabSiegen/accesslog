
from django.contrib.auth.models import User, Group
from rest_framework import serializers
from print.models import *

class ThreeDimensionalModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThreeDimensionalModel
        fields = ['id', 'Name' , 'FileName','Size','File', 'Uploaded', 'Owner', 'Previous', 'SharedWithUser']
        read_only_fields = ['Owner', 'Size', 'Name', 'FileName']

class GCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = GCode
        fields = ['id', 'Name' , 'FileName','Size','File', 'Uploaded', 'UsedFilamentInG','Owner', 'UsedFilamentInMm', 'SharedWithUser', 'EstimatedPrintingTime', 'ThreeDimensionalModel']
        read_only_fields = ['Size', 'Name', 'FileName', 'Owner']

class SlicingConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = SlicingConfig
        fields = ['ConfigLocation', 'GCode']


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']