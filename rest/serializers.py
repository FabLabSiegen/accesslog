
from django.contrib.auth.models import User, Group
from rest_framework import serializers
from print.models import *

class ThreeDimensionalModelSerializer(serializers.ModelSerializer):
    File = serializers.FileField()
    class Meta:
        model = ThreeDimensionalModel
        fields = ['File', 'Owner', 'Uploaded', 'Previous', 'SharedWithUser']

    def create(self, validated_data):
        model = ThreeDimensionalModel(
            File=validated_data['File'],
            Owner=validated_data['Owner'],
            Uploaded=validated_data['Uploaded'],
            Previous=validated_data['Previous'],
            SharedWithUser=validated_data['SharedWithUser'],
        )
        model.save()
        return model

    def update(self, instance, validated_data):
        instance.File = validated_data.get('File', instance.File)
        instance.save()

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']