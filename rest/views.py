import json
import os

import requests
from django.db.models import Q
from django.utils import timezone
from rest_framework import permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from print.models import *
from rest.serializers import *


class ThreeDimensionalModelViewSet(viewsets.ModelViewSet):
    serializer_class = ThreeDimensionalModelSerializer
    queryset = ThreeDimensionalModel.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    # Router class variables
    lookup_field = "id"

    @staticmethod
    def list(request):
        id = request.query_params.get("id")
        name = request.query_params.get("name")

        # Filter out if models are shared or owned by requesting user
        queryset = ThreeDimensionalModel.objects.filter(
            Q(Owner=request.user.id) | Q(SharedWithUser=request.user.id)
        )
        if id is not None:
            try:
                queryset = queryset.get(id=id)
                serializer = ThreeDimensionalModelSerializer(queryset)
                return Response(serializer.data, 200)
            except:
                return Response(status=404)
        elif name is not None:
            try:
                queryset = queryset.filter(Name=name)
                serializer = ThreeDimensionalModelSerializer(queryset, many=True)
                return Response(serializer.data, 200)
            except:
                return Response(status=404)
        else:
            serializer = ThreeDimensionalModelSerializer(queryset, many=True)
            return Response(serializer.data)

    def create(self, request):
        file = request.FILES.get("File")
        serializer = ThreeDimensionalModelSerializer(data=request.data)
        if serializer.is_valid():
            content_type = file.content_type
            if file.name.endswith(".stl") or file.name.endswith(".obj"):
                serializer.save(
                    Owner=self.request.user,
                    Size=file.size,
                    FileName=file.name,
                    Name=os.path.splitext(file.name)[0],
                )
                headers = self.get_success_headers(serializer.data)
                return Response(
                    serializer.data, status=status.HTTP_201_CREATED, headers=headers
                )
            else:
                response = {
                    "message:": "POST API does not accept {} files".format(content_type)
                }
                return Response(response, status=415)
        else:
            response = serializer.errors
            return Response(response, status=400)


class GCodeViewSet(viewsets.ModelViewSet):
    serializer_class = GCodeSerializer
    queryset = GCode.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    # Router class variables
    lookup_field = "id"

    @staticmethod
    def list(request):
        id = request.query_params.get("id")
        name = request.query_params.get("name")

        # Filter out if models are shared or owned by requesting user
        queryset = GCode.objects.filter(
            Q(Owner=request.user.id) | Q(SharedWithUser=request.user.id)
        )
        if id is not None:
            try:
                queryset = queryset.get(id=id)
                serializer = GCodeSerializer(queryset)
                return Response(serializer.data, 200)
            except:
                return Response(status=404)
        elif name is not None:
            try:
                queryset = queryset.filter(Name=name)
                serializer = GCodeSerializer(queryset, many=True)
                return Response(serializer.data, 200)
            except:
                return Response(status=404)
        else:
            serializer = GCodeSerializer(queryset, many=True)
            return Response(serializer.data)

    def create(self, request):
        file = request.FILES.get("File")
        serializer = GCodeSerializer(data=request.data)
        if serializer.is_valid():
            content_type = file.content_type
            if file.name.endswith(".gcode"):
                serializer.save(
                    Owner=self.request.user,
                    Size=file.size,
                    FileName=file.name,
                    Name=os.path.splitext(file.name)[0],
                )
                headers = self.get_success_headers(serializer.data)
                return Response(
                    serializer.data, status=status.HTTP_201_CREATED, headers=headers
                )
            else:
                response = {
                    "message:": "POST API does not accept {} files".format(content_type)
                }
                return Response(response, status=415)
        else:
            response = serializer.errors
            return Response(response, status=400)


class SlicingConfigViewSet(viewsets.ModelViewSet):
    serializer_class = SlicingConfigSerializer
    queryset = SlicingConfig.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    lookup_field = "GCode"

    def retrieve(self, request, *args, **kwargs):
        # get contents of config json
        instance = self.get_object()
        return Response(instance.Config)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        print(request.data["GCode"])
        try:
            SlicingConfig.objects.get(GCode_id=request.data["GCode"])
            exists = True
            print(True)
        except:
            exists = False

        if exists:
            response = {"error": "SlicingConfig of GCode already exists"}
            return Response(response, status=409)
        elif serializer.is_valid() and str(request.data["Config"]) != "null":
            self.perform_create(serializer)

            headers = self.get_success_headers(serializer.data)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED, headers=headers
            )
        else:
            return Response(serializer.errors, status=400)


class PrintJobViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows PrintJobs to be viewed or edited.
    """

    serializer_class = PrintJobSerializer
    queryset = PrintJob.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    lookup_field = "id"

    def perform_create(self, serializer):
        serializer.save(User=self.request.user)

    def list(self, request, *args, **kwargs):
        # Filter out if models are owned by requesting user
        queryset = PrintJob.objects.filter(Q(User=request.user.id))
        serializer = PrintJobSerializer(queryset, many=True)
        return Response(serializer.data)


class PrintMediaFileViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows PrintMediaFiles to be viewed or edited.
    """

    serializer_class = PrintMediaFileSerializer
    queryset = PrintMediaFile.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    lookup_field = "id"

    def create(self, request, *args, **kwargs):
        # Lookup the printjob id
        job_id = self.request.data.__getitem__("PrintJob")
        # Lookup the id of the user that owns that print job
        job_user = PrintJob.objects.get(id=job_id).User.id
        # See if logged in user owns the print job that will be related to the media files
        if job_user == request.user.id:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=201, headers=headers)
        else:
            response = {
                "message": "You are not allowed to add media files to that Print Job because you do not own it"
            }
            return Response(response, status=403)

    def perform_create(self, serializer):
        serializer.save(Owner=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        if request.user.id == instance.Owner.id:
            return Response(serializer.data)
        else:
            response = {
                "message": "You are not allowed to retrieve this entry because you are not the Owner"
            }
            return Response(response, status=403)


class PrintMediaFileByPrintJob(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        pk = self.kwargs["pk"]
        queryset = PrintMediaFile.objects.filter(Q(PrintJob=pk))
        if queryset:
            serializer = PrintMediaFileSerializer(queryset, many=True)
            return Response(serializer.data)
        else:
            response = {"message": "There are no Media Files related to that Print Job"}
            return Response(response, status=404)


def post_file(api_key, file, host):
    hed = {"Authorization": "Bearer " + api_key}
    data = {"print": "true", "file": file}

    url = "http://" + host + "/api/files/local"
    try:
        response = requests.post(url, files=data, headers=hed)

        return Response(json.loads(response.text), status=response.status_code)
    except requests.exceptions.RequestException as e:
        response = {"error": str(e)}
        return Response(response, status=421)
    except Exception as e:
        response = {"error": str(e)}
        print(e)
        return Response(response, status=500)


class StartPrintJob(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = StartPrintJobSerializer

    def post(self, request, *args, **kwargs):
        p_exists = None
        owner = self.request.user.id

        try:
            file = GCode.objects.get(id=request.data["GCode"]).File
            api_key = Machine.objects.get(id=request.data["Machine"]).ApiKey
            host = Machine.objects.get(id=request.data["Machine"]).DomainName
        except Exception as e:
            return Response(str(e), status=500)

        response = post_file(api_key, file, host)
        print(response.status_code)
        if response.status_code == 201:
            try:
                PrintJob.objects.get(
                    Machine_id=request.data["Machine"], State="PRINTING"
                )
                p_exists = True
            except PrintJob.DoesNotExist:
                p_exists = False
            except Exception as e:
                print(e)

            try:
                if not p_exists:
                    PrintJob.objects.create(
                        Start=timezone.now(),
                        End=None,
                        GCode_id=request.data["GCode"],
                        State="PRINTING",
                        Machine_id=request.data["Machine"],
                        User_id=owner,
                    )
                    print("PrintJob created")
            except Exception as e:
                print(e)
        return response


def stop_job(api_key, host):
    hed = {"Authorization": "Bearer " + api_key, "content-type": "application/json"}
    data = {"command": "cancel"}

    url = "http://" + host + "/api/job"
    try:
        response = requests.post(url, data=json.dumps(data), headers=hed)
        try:
            r = json.loads(response.text)
            return Response(r, status=response.status_code)
        except:
            return Response(status=response.status_code)

    except requests.exceptions.RequestException as e:
        response = {"error": str(e)}
        return Response(response, status=421)


class StopPrintJob(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = StopPrintJobSerializer

    def post(self, request, *args, **kwargs):

        print(request.data)

        try:
            machine_id = PrintJob.objects.get(id=request.data["PrintJob"]).Machine.id
            owner = PrintJob.objects.get(id=request.data["PrintJob"]).User.id
        except Exception as e:
            return Response(str(e), status=500)

        if owner == self.request.user.id:
            try:
                api_key = Machine.objects.get(id=machine_id).ApiKey
                host = Machine.objects.get(id=machine_id).DomainName
            except Exception as e:
                return Response(str(e), status=500)

            try:
                response = stop_job(api_key, host)
                return response
            except requests.exceptions.RequestException as e:
                response = {"error": str(e)}
                return Response(response, status=421)
        else:
            response = {
                "message": "You are not allowed to stop this PrintJob because you do not own it"
            }
            return Response(response, status=403)


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]
