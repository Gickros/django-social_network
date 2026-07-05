import pytest
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile

from Post.api.models import Post

User = get_user_model()


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
        desc="Description",
        author=user,
        image=image,
    )


@pytest.mark.django_db
def test_post_created(post):
    assert Post.objects.count() == 1


@pytest.mark.django_db
def test_slug_created(post):
    assert post.slug == "my-first-post"


@pytest.mark.django_db
def test_post_author(post, user):
    assert post.author == user


@pytest.mark.django_db
def test_default_status(post):
    assert post.status == Post.Status.DRAFT


@pytest.mark.django_db
def test_title_saved(post):
    assert post.title == "My First Post"


@pytest.mark.django_db
def test_image_saved(post):
    assert post.image.name.endswith(".jpg")