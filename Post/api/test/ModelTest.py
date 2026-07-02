# Create your tests here.
from django.test import TestCase
from .models import Post,Comment



class PostTests(TestCase):
    def test_create_post(self):
        Post.objects.create(**data)
        self.assertEqual(Post.objects.count(),1)
