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
        Create Test User to authenticate
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
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        # Test if there is actually one file uploaded
        self.assertEqual(ThreeDimensionalModel.objects.count(), 1)

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
        # Test null input, bad request
        request = client.post(reverse('ThreeDimensionalModel-list'), None)
        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)

class ThreeDimensionalModelListTestCase(APITestCase):

    def setUp(self):
        """
        Create Test User to authenticate and add test objects to database
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

    def test_list_model_shared(self):
        """
        Ensure that shared users can request models shared with them
        """
        client = login()
        ThreeDimensionalModel.objects.create(SharedWithUser_id=1)
        request = client.get(reverse('ThreeDimensionalModel-list'))
        entry_count = json.dumps(request.data).count('id')
        self.assertEqual(entry_count, 1)
