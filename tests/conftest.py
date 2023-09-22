import pytest
import os
import shutil
from django.contrib.auth.models import AnonymousUser
from pytest_factoryboy import register
from rest_framework.test import APIClient

from tests.factories import UserFactory, TierFactory, ImageFactory


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def anonymous_user():
    return AnonymousUser()


@pytest.fixture
def image_cleanup():
    image_id = []

    def set_image_id(id):
        image_id.append(id)
    yield set_image_id

    try:
        dir_path = f"imgs/{image_id[0]}"
        if os.path.exists(dir_path):
            shutil.rmtree(dir_path)
    except Exception as e:
        print(f"Failed to delete directory: {e}")


register(UserFactory)
register(TierFactory)
register(ImageFactory)
