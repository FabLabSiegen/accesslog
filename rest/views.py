from django.contrib.auth.models import User, Group
from django.core.files.storage import default_storage
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import permissions
from rest.serializers import *
from print.models import *

class ThreeDimensionalModelViewSet(viewsets.ViewSet):
    serializer_class = ThreeDimensionalModelSerializer
    queryset = ThreeDimensionalModel.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        return Response("GET API")

    def create(self, request):
        file = request.FILES.get('File')
        content_type = file.content_type
        serializer = ThreeDimensionalModelSerializer(data=request.data)
        if serializer.is_valid():
            if file.name.endswith('.stl') or file.name.endswith('.obj'):
                serializer.save()
                print(serializer.data)
                print(request.user.id)
                default_storage.save('models/'+file.name, file)
                #### print(ThreeDimensionalModelSerializer.is_valid(self))
                response = "POST API and you have uploaded a {} file".format(content_type)
                return Response(response, status=200)
            else:
                print(file.name)
                response = "POST API does not accept {} files".format(content_type)
                return Response(response, status=415)
        else:
            return Response(serializer.errors, status=400)

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]