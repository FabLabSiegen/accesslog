
from django.contrib.auth.models import User, Group
from rest_framework import serializers
from print.models import *

class ThreeDimensionalModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThreeDimensionalModel
        fields = ['File', 'Owner', 'Uploaded', 'Previous', 'SharedWithUser']


class UserSerializer(serializers.HyperlinkedModelSerializer):
    tdm = serializers.PrimaryKeyRelatedField(many=True, queryset=ThreeDimensionalModel.objects.all())
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups', 'tdm']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']