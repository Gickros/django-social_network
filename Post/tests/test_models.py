# Create your tests here.
from django.test import TestCase
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from Post.api.models import Post



class PostTests(TestCase):
   
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="12345678"
        )

        self.image = SimpleUploadedFile(
            "test.jpg",
            b"file_content",
            content_type="image/jpeg"
        )

    def test_create_post(self):
        Post.objects.create(
            title="Test",
            desc="Description",
            author=self.user,
            image=self.image,
        )

        self.assertEqual(Post.objects.count(), 1)