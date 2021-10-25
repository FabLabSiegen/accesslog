import tempfile

from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from print.models import *

class ThreeDimensionalModelTests(APITestCase):

    def setUp(self):
        """
        Create Test User to authenticate
        """
        User.objects.create_user('testuser')

    def test_create_model(self):
        """
        Ensure we can upload a ThreeDimensionalModel.
        """
        client = APIClient()
        user = User.objects.get(username='testuser')
        client.force_authenticate(user=user)

        # Test correct input response
        correct_file = SimpleUploadedFile("file.obj", b"file_content", content_type="application/octet-stream")
        correct = client.post(reverse('ThreeDimensionalModel-list'), {'File': correct_file})
        self.assertEqual(correct.status_code, status.HTTP_200_OK)
        # Test if there is actually one file uploaded
        self.assertEqual(ThreeDimensionalModel.objects.count(), 1)

        # Test incorrect file type input response
        incorrect_file = SimpleUploadedFile("file.jpg", b"file_content", content_type="image/jpeg")
        incorrect_type = client.post(reverse('ThreeDimensionalModel-list'), {'File': incorrect_file})
        self.assertNotEqual(incorrect_type.status_code, status.HTTP_200_OK)
        self.assertEqual(incorrect_type.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

        # Test null input, bad request
        incorrect_request = client.post(reverse('ThreeDimensionalModel-list'), None)
        self.assertEqual(incorrect_request.status_code, status.HTTP_400_BAD_REQUEST)