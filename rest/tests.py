import tempfile

from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from print.models import *


def login():
    client = APIClient()
    user = User.objects.get(username='testuser')
    client.force_authenticate(user=user)
    return client


class ThreeDimensionalModelTestCase(APITestCase):

    def setUp(self):
        """
        Create Test User to authenticate
        """
        User.objects.create_user('testuser')

    def test_create_model(self):
        """
        Ensure we can upload a ThreeDimensionalModel.
        """
        client = login()

        # Test correct input response
        file = SimpleUploadedFile("file.obj", b"file_content", content_type="application/octet-stream")
        correct = client.post(reverse('ThreeDimensionalModel-list'), {'File': file})
        self.assertEqual(correct.status_code, status.HTTP_200_OK)
        # Test if there is actually one file uploaded
        self.assertEqual(ThreeDimensionalModel.objects.count(), 1)

    def test_create_model_wrong_type(self):
        """
        Ensure that a wrong file type leads to a 415 Error
        """
        client = login()
        # Test incorrect file type input response
        file = SimpleUploadedFile("file.jpg", b"file_content", content_type="image/jpeg")
        incorrect_type = client.post(reverse('ThreeDimensionalModel-list'), {'File': file})
        self.assertEqual(incorrect_type.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    def test_create_model_bad_request(self):
        """
        Ensure that a bad request leads to a 400 Error
        """
        client = login()
        # Test null input, bad request
        incorrect_request = client.post(reverse('ThreeDimensionalModel-list'), None)
        self.assertEqual(incorrect_request.status_code, status.HTTP_400_BAD_REQUEST)