import pytest
from django.core.files.uploadedfile import SimpleUploadedFile

from rest_framework.test import APIClient
from tests.factories import UserFactory, TierFactory


@pytest.mark.django_db
def test_create_image(client: APIClient, user_factory: UserFactory, tier_factory: TierFactory, image_cleanup) -> None:
    user = user_factory.create()
    payload = dict(
        username=user.username,
        password="defaultpassword",
    )
    response = client.post('/users/login', payload)
    access = f'Bearer {response.data["access"]}'
    client.credentials(HTTP_AUTHORIZATION=access)
    with open('tests/test_files/tree.jpg', 'rb') as img_file:
        img = SimpleUploadedFile('tree.jpg', img_file.read())

    response = client.post('/images/', {'img': img}, format='multipart')
    image_id = response.data['id']
    image_cleanup(image_id)

    assert len(response.data['thumbnails']) == len(user.tier.thumbnails_sizes)
    assert bool(response.data['original']) == user.tier.have_original_url


@pytest.mark.django_db
def test_create_links(client: APIClient, user_factory: UserFactory, tier_factory: TierFactory, image_cleanup) -> None:
    user = user_factory.create()
    payload = dict(
        username=user.username,
        password="defaultpassword",
    )
    response = client.post('/users/login', payload)
    access = f'Bearer {response.data["access"]}'
    client.credentials(HTTP_AUTHORIZATION=access)
    with open('tests/test_files/tree.jpg', 'rb') as img_file:
        img = SimpleUploadedFile('tree.jpg', img_file.read())

    response = client.post('/images/', {'img': img}, format='multipart')
    image_id = response.data['id']
    response = client.post(f'/images/{image_id}/create_expiring_link/', {'time_to_live': 10000})
    image_cleanup(image_id)
    assert (response.status_code == 201) == user.tier.can_create_links