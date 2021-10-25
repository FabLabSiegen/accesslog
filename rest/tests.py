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
        file = SimpleUploadedFile("file.obj", b"file_content", content_type="application/octet-stream")
        response = client.post(reverse('ThreeDimensionalModel-list'), {'File': file})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Test if there is actually one file uploaded
        self.assertEqual(ThreeDimensionalModel.objects.count(), 1)