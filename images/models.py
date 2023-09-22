from django.db import models
from users.models import User
import uuid
from django.dispatch import receiver
import os


def original_upload_to(instance, filename):
    return f'imgs/{instance.id}/original/{filename}'


class Image(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    original = models.ImageField(upload_to=original_upload_to, null=True, blank=True)


def thumbnail_upload_to(instance, filename):
    return f'imgs/{instance.image.id}/thumbnails/{filename}'


class ImageThumbnail(models.Model):
    image = models.ForeignKey(Image, on_delete=models.CASCADE, related_name="thumbnails")
    thumbnail = models.ImageField(upload_to=thumbnail_upload_to, default="", null=True, blank=True)


@receiver(models.signals.post_delete, sender=ImageThumbnail)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.thumbnail:
        if os.path.isfile(instance.thumbnail.path):
            os.remove(instance.thumbnail.path)


class Link(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    timestamp_start = models.IntegerField()
    time_to_live = models.IntegerField()
