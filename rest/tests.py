import tempfile
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient, RequestsClient
from print.models import *
import json


def login():
    client = APIClient()
    user = User.objects.get(username='testuser')
    client.force_authenticate(user=user)
    return client


class ThreeDimensionalModelCreateTestCase(APITestCase):

    def setUp(self):
        """
        Create Test User to authenticate and add and request test objects to database
        """
        User.objects.create_user('testuser')

    def test_login(self):
        """
        Ensure that logged in client can make requests
        """
        client = login()
        request = client.request()
        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_create_model(self):
        """
        Ensure we can upload a ThreeDimensionalModel.
        """
        client = login()
        # Test correct input response
        file = SimpleUploadedFile("file.obj", b"file_content", content_type="application/octet-stream")
        request = client.post(reverse('ThreeDimensionalModel-list'), {'File': file})
        self.assertEqual(request.status_code, status.HTTP_201_CREATED)
        # Test if there is actually one file uploaded
        self.assertEqual(ThreeDimensionalModel.objects.count(), 1)
        # Test if uploading user was associated as owner of model
        self.assertEqual(request.data['Owner'], 1)

    def test_create_model_wrong_type(self):
        """
        Ensure that a wrong file type leads to a 415 Error
        """
        client = login()
        # Test incorrect file type input response
        file = SimpleUploadedFile("file.jpg", b"file_content", content_type="image/jpeg")
        request = client.post(reverse('ThreeDimensionalModel-list'), {'File': file})
        self.assertEqual(request.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    def test_create_model_bad_request(self):
        """
        Ensure that a bad request leads to a 400 Error
        """
        client = login()
        # Test null input (bad request)
        request = client.post(reverse('ThreeDimensionalModel-list'), None)
        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)

class ThreeDimensionalModelListTestCase(APITestCase):

    def setUp(self):
        """
        Create Test User to authenticate and add and request test objects to database
        """
        User.objects.create_user(username='testuser', id=1)

    def test_list_model_owner(self):
        """
        Ensure that Owners can request their models
        """
        client = login()
        ThreeDimensionalModel.objects.create(Owner_id=1)
        request = client.get(reverse('ThreeDimensionalModel-list'))
        entry_count = json.dumps(request.data).count('id')
        self.assertEqual(entry_count, 1)
        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_list_model_shared(self):
        """
        Ensure that shared users can request models shared with them
        """
        client = login()
        ThreeDimensionalModel.objects.create(SharedWithUser_id=1)
        request = client.get(reverse('ThreeDimensionalModel-list'))
        entry_count = json.dumps(request.data).count('id')
        self.assertEqual(entry_count, 1)
        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_list_model_id(self):
        """
        Ensure that shared users can request models shared with them by id
        """
        client = login()
        ThreeDimensionalModel.objects.create(id=1, Owner_id=1)
        request = client.get(reverse('ThreeDimensionalModel-list')+'?id=1')
        entry_count = json.dumps(request.data).count('id')
        self.assertEqual(entry_count, 1)
        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_list_model_name(self):
        """
        Ensure that shared users can request models shared with them by name
        """
        client = login()
        ThreeDimensionalModel.objects.create(Name='testmodel', Owner_id=1)
        request = client.get(reverse('ThreeDimensionalModel-list')+'?name=testmodel')
        entry_count = json.dumps(request.data).count('id')
        self.assertEqual(entry_count, 1)
        self.assertEqual(request.status_code, status.HTTP_200_OK)

class GCodeCreateTestCase(APITestCase):

    def setUp(self):
        """
        Create Test User to authenticate and add and request test objects to database
        """
        User.objects.create_user(username='testuser', id=1)

    def test_create_gcode(self):
        """
        Ensure we can upload a GCode.
        """
        client = login()
        # Test correct input response
        file = SimpleUploadedFile("file.gcode", b"file_content", content_type="application/octet-stream")
        request = client.post(reverse('GCode-list'), {
            'File': file,
            'UsedFilamentInG': 1233.23,
            'UsedFilamentInMm': 12.324,
            'EstimatedPrintingTime': '20:12:20'
        })
        self.assertEqual(request.status_code, status.HTTP_201_CREATED)
        # Test if there is actually one file uploaded
        self.assertEqual(GCode.objects.count(), 1)
        # Test if uploading user was associated as owner of gcode
        self.assertEqual(request.data['Owner'], 1)

    def test_create_gcode_wrong_type(self):
        """
        Ensure that a wrong file type leads to a 415 Error
        """
        client = login()
        # Test incorrect file type input response
        file = SimpleUploadedFile("file.jpg", b"file_content", content_type="image/jpeg")
        request = client.post(reverse('GCode-list'), {
            'File': file,
            'UsedFilamentInG': 1233.23,
            'UsedFilamentInMm': 12.324,
            'EstimatedPrintingTime': '20:12:20'}
        )
        self.assertEqual(request.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    def test_create_gcode_bad_request(self):
        """
        Ensure that a bad request leads to a 400 Error
        """
        client = login()
        # Test null input (bad request)
        request = client.post(reverse('GCode-list'), None)
        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)

class GCodeListTestCase(APITestCase):

    def setUp(self):
        """
        Create Test User to authenticate and add and request test objects to database
        """
        User.objects.create_user(username='testuser', id=1)

    def test_list_gcode_owner(self):
        """
        Ensure that Owners can request their GCode
        """
        client = login()
        GCode.objects.create(
            id=1,
            Owner_id=1,
            UsedFilamentInG=123.123,
            UsedFilamentInMm=123.123,
            EstimatedPrintingTime='12:03:00'
        )
        request = client.get(reverse('GCode-list'))
        entry_count = json.dumps(request.data).count('id')
        self.assertEqual(entry_count, 1)
        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_list_gcode_shared(self):
        """
        Ensure that shared users can request GCode shared with them
        """
        client = login()
        GCode.objects.create(
            id=1,
            SharedWithUser_id=1,
            UsedFilamentInG=123.123,
            UsedFilamentInMm=123.123,
            EstimatedPrintingTime='12:03:00'
        )
        request = client.get(reverse('GCode-list'))
        entry_count = json.dumps(request.data).count('id')
        self.assertEqual(entry_count, 1)
        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_list_gcode_id(self):
        """
        Ensure that shared users can request GCode shared with them by id
        """
        client = login()
        GCode.objects.create(
            id=1,
            Owner_id=1,
            UsedFilamentInG=123.123,
            UsedFilamentInMm=123.123,
            EstimatedPrintingTime='12:03:00'
        )
        request = client.get(reverse('GCode-list')+'?id=1')
        entry_count = json.dumps(request.data).count('id')
        self.assertEqual(entry_count, 1)
        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_list_gcode_name(self):
        """
        Ensure that shared users can request GCode shared with them by name
        """
        client = login()
        GCode.objects.create(
            id=1,
            Owner_id=1,
            UsedFilamentInG=123.123,
            UsedFilamentInMm=123.123,
            EstimatedPrintingTime='12:03:00',
            Name='testgcode'
        )
        request = client.get(reverse('GCode-list')+'?name=testgcode')
        entry_count = json.dumps(request.data).count('id')
        self.assertEqual(entry_count, 1)
        self.assertEqual(request.status_code, status.HTTP_200_OK)

class SlicingConfigRetrieveTestCase(APITestCase):

    def setUp(self):
        """
        Create Test User to authenticate and add and request test objects to database
        """
        User.objects.create_user(username='testuser', id=1)

    def test_slicing_config_retrieve(self):
        """
        Ensure that users can request SlicingConfig by providing GCode ID
        """
        client = login()
        # Create test JSON to be used in SlicingConfig creation
        test_json = {
            'testjson': {
                'test1': {
                    'data': 'Testdata'
                },
                'test2': {
                    'data': 'Testdata'
                },
            }
        }
        # Create test GCode to be able to create Slicing Config related to GCode
        GCode.objects.create(
            id=1,
            Owner_id=1,
            UsedFilamentInG=123.123,
            UsedFilamentInMm=123.123,
            EstimatedPrintingTime='12:03:00',
            Name='testgcode'
        )
        # Create test slicing config to retrieve afterwards
        SlicingConfig.objects.create(
            Config=test_json,
            GCode_id=1
        )
        request = client.get(reverse('SlicingConfig-list')+'1/')
        # Test if response json is the same as we created before
        self.assertJSONEqual(json.dumps(request.data),json.dumps(test_json))
        self.assertEqual(request.status_code,status.HTTP_200_OK)

class SlicingConfigCreateTestCase(APITestCase):

    def setUp(self):
        """
        Create Test User to authenticate and add and request test objects to database
        """
        User.objects.create_user(username='testuser', id=1)

    def test_slicing_config_create(self):
        """
        Ensure that users can upload SlicingConfig by providing related GCode
        """
        client = login()
        # Creating related GCode for SlicingConfig relation
        GCode.objects.create(
            id=1,
            Owner_id=1,
            UsedFilamentInG=123.123,
            UsedFilamentInMm=123.123,
            EstimatedPrintingTime='12:03:00',
            Name='testgcode'
        )
        # Creating Json for testing
        test_json = {
            'testjson': {
                'test1': {
                    'data': 'Testdata'
                },
                'test2': {
                    'data': 'Testdata'
                },
            }
        }
        # Creating request to upload Slicing config and relate it to an existing GCode
        request = client.post(reverse('SlicingConfig-list'), {'Config':test_json, 'GCode':1}, format='json')
        entry_count = json.dumps(request.data).count('Config')
        # Test if entry was created
        self.assertEqual(request.status_code, status.HTTP_201_CREATED)
        self.assertEqual(entry_count, 1)

class PrintJobListTestCase(APITestCase):

    def setUp(self):
        """
        Create Test User to authenticate and add and request test objects to database
        """
        User.objects.create_user(username='testuser', id=1)

    def test_print_job_list(self):
        """
        Ensure that users can request owned PrintJobs
        """
        client = login()
        PrintJob.objects.create(
            Start="2021-10-21T13:39:00Z",
            End="2021-10-21T13:39:00Z",
            State=1,
            User_id=1
        )
        request = client.get(reverse('PrintJob-list'))
        entry_count = json.dumps(request.data).count('id')
        self.assertEqual(entry_count, 1)
        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_print_job_list_unowned(self):
        """
        Ensure that users cannot request unowned PrintJobs
        """
        client = login()
        # Create User that is not logged in
        User.objects.create_user(username='other_user', id=2)
        # Create PrintJob of not logged in User
        PrintJob.objects.create(
            Start="2021-10-21T13:39:00Z",
            End="2021-10-21T13:39:00Z",
            State=1,
            User_id=2
        )
        request = client.get(reverse('PrintJob-list'))
        entry_count = json.dumps(request.data).count('id')
        # Test if logged in User does not see PrintJobs of not logged in User
        self.assertEqual(entry_count, 0)

class PrintJobCreateTestCase(APITestCase):

    def setUp(self):
        """
        Create Test User to authenticate and add and request test objects to database
        """
        User.objects.create_user(username='testuser', id=1)

    def test_print_job_create(self):
        """
        Ensure that users can create PrintJobs and own them afterwards
        """
        client = login()
        request = client.post(reverse('PrintJob-list'), {'Start':'2021-10-21T13:39:00Z', 'End':'2021-10-21T13:39:00Z', 'State':1}, format='json')
        entry_count = json.dumps(request.data).count('id')
        # Test if entry was created
        self.assertEqual(request.status_code, status.HTTP_201_CREATED)
        self.assertEqual(entry_count, 1)
        # Test if created PrintJob is related to creating user
        self.assertEqual(request.data['User'], 1)

