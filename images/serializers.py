from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.base import ContentFile

from images.models import Image, ImageThumbnail

from PIL import Image as PILImage
from io import BytesIO


class ThumbnailSerializer(serializers.ModelSerializer):
    thumbnail = serializers.ImageField(max_length=None, use_url=True)

    class Meta:
        model = ImageThumbnail
        fields = ["id", "image", "thumbnail"]


def custom_validator(value):
    valid_formats = ['png', 'jpeg', 'jpg']
    if not any([True if value.name.endswith(i) else False for i in valid_formats]):
        raise ValidationError(f'{value.name} is not a valid image format')


class ImageSerializer(serializers.ModelSerializer):
    thumbnails = ThumbnailSerializer(many=True, read_only=True)
    img = serializers.ImageField(write_only=True, validators=[custom_validator])
    original = serializers.ImageField(max_length=None, use_url=True, read_only=True)

    class Meta:
        model = Image
        fields = '__all__'

    def create(self, validated_data):
        uploaded_image = validated_data.pop("img")
        image = Image.objects.create(**validated_data)
        pil_image = PILImage.open(uploaded_image)
        for size in image.user.tier.thumbnails_sizes:
            with BytesIO() as buffer:
                pil_copy = pil_image.copy()
                pil_copy.thumbnail((size, size))
                pil_copy.save(buffer, format='JPEG')
                file_name = f'{uploaded_image.name.split(".")[0]}_{size}.jpg'
                file = ContentFile(buffer.getvalue())
                file = InMemoryUploadedFile(file, None, file_name, 'image/jpeg', file.size, None)
                ImageThumbnail.objects.create(image=image, thumbnail=file)
        return image
