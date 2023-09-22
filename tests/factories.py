import random

import factory
from faker import Faker

from images.models import Image
from users.models import User, Tier

fake = Faker()


class TierFactory(factory.django.DjangoModelFactory):
    name = factory.LazyAttribute(lambda x: fake.unique.first_name())
    thumbnails_sizes = [random.randint(100, 1000) for x in range(random.randint(1, 5))]
    have_original_url = random.choice([True, False])
    can_create_links = random.choice([True, False])

    class Meta:
        model = Tier


class UserFactory(factory.django.DjangoModelFactory):
    username = factory.LazyAttribute(lambda x: fake.unique.first_name())
    password = factory.PostGenerationMethodCall('set_password', 'defaultpassword')
    email = factory.LazyAttribute(lambda x: fake.unique.email())
    tier = factory.SubFactory(TierFactory)

    class Meta:
        model = User


class ImageFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = Image
