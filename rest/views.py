from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import permissions
from rest.serializers import *
from print.models import *
from django.db.models import Q
from rest_framework import viewsets

class ThreeDimensionalModelViewSet(viewsets.ModelViewSet):
    serializer_class = ThreeDimensionalModelSerializer
    queryset = ThreeDimensionalModel.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    # Router class variables
    lookup_field = 'id'

    @staticmethod
    def list(request):
        id = request.query_params.get('id')
        name = request.query_params.get('name')
        if id is not None:
            try:
                queryset = ThreeDimensionalModel.objects.get(id=id)
                serializer = ThreeDimensionalModelSerializer(queryset)
                return Response(serializer.data,200)
            except:
                return Response(status=404)
        elif name is not None:
            try:
                queryset = ThreeDimensionalModel.objects.filter(Name=name)
                serializer = ThreeDimensionalModelSerializer(queryset, many=True)
                return Response(serializer.data, 200)
            except:
                return Response(status=404)
        else:
            # Filter out if models are shared or owned by requesting user
            queryset = ThreeDimensionalModel.objects.filter(Q(Owner=request.user.id) | Q(SharedWithUser=request.user.id))
            serializer = ThreeDimensionalModelSerializer(queryset, many=True)
            return Response(serializer.data)

    def create(self, request):
        file = request.FILES.get('File')
        content_type = file.content_type
        serializer = ThreeDimensionalModelSerializer(data=request.data)
        if serializer.is_valid():
            if file.name.endswith('.stl') or file.name.endswith('.obj'):
                obj = serializer.save(Owner=self.request.user, Size=file.size, Name=file.name)
                response = {'message:':'POST API and you have uploaded a {} file'.format(content_type), 'id':obj.id}
                return Response(response, status=200)
            else:
                response = {'message:':'POST API does not accept {} files'.format(content_type)}
                return Response(response, status=415)
        else:
            response = {'message:':'Following serializer errors came up: ' + serializer.errors}
            return Response(response, status=400)


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