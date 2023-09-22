import uuid

from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.db import models
from django.contrib.postgres.fields import ArrayField

from users.managers import UserManager
from users.userABC import UserABC


class Tier(models.Model):
    name = models.CharField(max_length=30, unique=True, primary_key=True)
    thumbnails_sizes = ArrayField(models.IntegerField(), size=10, null=False)
    have_original_url = models.BooleanField(default=False)
    can_create_links = models.BooleanField(default=False)


def get_basic_tier():
    try:
        Tier.objects.get_or_create(name="Premium", defaults={'thumbnails_sizes': [200, 400], 'have_original_url': True})
        Tier.objects.get_or_create(name="Enterprise", defaults={'thumbnails_sizes': [200, 400], 'have_original_url': True,
                                                                'can_create_links': True})
        return Tier.objects.get_or_create(
            name="Basic",
            defaults={'thumbnails_sizes': [200]}
        )[0].pk
    except Exception as exc:
        print(exc)


class User(UserABC):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tier = models.ForeignKey('users.Tier', on_delete=models.SET_NULL, default=get_basic_tier,
                             null=True, related_name='tier')

    objects = UserManager()
