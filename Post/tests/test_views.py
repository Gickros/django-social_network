import pytest
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from Post.api.models import Post
from .test_models import image,user
from rest_framework.test import APIClient
##force_authenticate - регистрация пользователя для апи клиента   не выполняя настоящие действие для входа в систему
##    format="multipart",  # если отправляешь файл
@python.fixture
def client():
    return ApiClient()
@pytest.fixture
def post(user, image):
    return Post.objects.create(
        title="My First Post",
        desc="Test",
        author=user,
        image=image,
    )


@python.mark.djang_db
def create_1_post(client,post):
    response = client.get ('posts/')
    assert response.status_code== 200
    assert len(response.data)==1

@pytest.mark.django_db
def test_get_post(client, post):
    response = client.get(f"/posts/{post.id}/")

    assert response.status_code == 200
    assert response.data["title"] == post.title

@pytest.mark.django_db
def test_delete_post(client, user, post):
    client.force_authenticate(user=user)

    response = client.delete(f"/posts/{post.id}/")

    assert response.status_code == 204
    assert Post.objects.count() == 0