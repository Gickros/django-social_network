import tempfile

import pytest
from PIL import Image
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework.test import APIClient

from Post.api.models import Post

User = get_user_model()


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def user():
    return User.objects.create_user(
        username="testuser",
        password="12345678",
    )


@pytest.fixture
def image():
    file = tempfile.NamedTemporaryFile(suffix=".jpg")

    img = Image.new("RGB", (100, 100), color="white")
    img.save(file, "JPEG")
    file.seek(0)

    return SimpleUploadedFile(
        "test.jpg",
        file.read(),
        content_type="image/jpeg",
    )


@pytest.fixture
def post(user, image):
    return Post.objects.create(
        title="Test Post",
        desc="Description",
        author=user,
        image=image,
    )


@pytest.mark.django_db
def test_get_posts(client, post):
    response = client.get(reverse("post-list"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_single_post(client, post):
    response = client.get(reverse("post-detail", args=[post.id]))
    assert response.status_code == 200


@pytest.mark.django_db
def test_create_post_authorized(client, user, image):
    client.force_authenticate(user=user)

    response = client.post(
        reverse("post-list"),
        {
            "title": "New Post",
            "desc": "Description",
            "image": image,
        },
        format="multipart",
    )

    assert response.status_code == 201


@pytest.mark.django_db
def test_create_post_unauthorized(client, image):
    response = client.post(
        reverse("post-list"),
        {
            "title": "New Post",
            "desc": "Description",
            "image": image,
        },
        format="multipart",
    )

    assert response.status_code in (401, 403)


@pytest.mark.django_db
def test_update_post(client, user, post):
    client.force_authenticate(user=user)

    response = client.patch(
        reverse("post-detail", args=[post.id]),
        {"title": "Updated"},
    )

    assert response.status_code == 200


@pytest.mark.django_db
def test_delete_post(client, user, post):
    client.force_authenticate(user=user)

    response = client.delete(
        reverse("post-detail", args=[post.id])
    )

    assert response.status_code == 204


@pytest.mark.django_db
def test_post_count(post):
    assert Post.objects.count() == 1


@pytest.mark.django_db
def test_post_title(post):
    assert post.title == "Test Post"


@pytest.mark.django_db
def test_post_not_found(client):
    response = client.get(reverse("post-detail", args=[99999]))
    assert response.status_code == 404