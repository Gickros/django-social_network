import pytest
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from Post.api.models import Post


@pytest.fixture
def user():
    return User.objects.create_user(
        username="testuser",
        password="12345678",
    )


@pytest.fixture
def image():
    return SimpleUploadedFile(
        "test.jpg",
        b"file_content",
        content_type="image/jpeg",
    )


@pytest.fixture
def post(user, image):
    return Post.objects.create(
        title="My First Post",
        desc="Test",
        author=user,
        image=image,
    )


@pytest.mark.django_db
def test_create_post(post):
    assert Post.objects.count() == 1


@pytest.mark.django_db
def test_slug(post):
    assert post.slug == "my-first-post"

@pytest.mark.django_db
def test_author(post,user):
    assert Post.author==user


