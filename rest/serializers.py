
from django.contrib.auth.models import User, Group
from rest_framework import serializers
from print.models import *

class ThreeDimensionalModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThreeDimensionalModel
        fields = ['File', 'Uploaded', 'Owner', 'Previous', 'SharedWithUser']
        read_only_fields = ['Owner']


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']