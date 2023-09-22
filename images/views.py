from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.decorators import action
from django.http import FileResponse, HttpResponseForbidden, HttpResponseNotFound, HttpResponseBadRequest
from images.models import Image, Link

from images.serializers import ImageSerializer
from hexocean import settings
from images.permissions import IsOwner, IsAdmin

import os
import shutil
from uuid import UUID
from time import time


class ServeProtectedMedia(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, file_path):
        try:
            img_uuid = UUID(file_path.split('/')[0])
        except ValueError:
            return HttpResponseNotFound()

        image = Image.objects.get(id=img_uuid)
        if image:
            if request.user == image.user:
                try:
                    response = FileResponse(open(f'imgs/{file_path}', 'rb'))
                    return response
                except FileNotFoundError:
                    return HttpResponseNotFound()
        else:
            return HttpResponseNotFound()

        return HttpResponseForbidden()


class ImageViewSet(ModelViewSet):
    queryset = Image.objects.all()
    permission_classes = (IsAuthenticated, )
    serializer_class = ImageSerializer
    http_method_names = ['get', 'post', 'delete', 'head', 'options']

    def get_permissions(self):
        if self.request.method in ['GET', 'DELETE']:
            self.permission_classes = (IsOwner | IsAdmin, )
        else:
            self.permission_classes = (IsAuthenticated, )
        return super(ImageViewSet, self).get_permissions()

    def list(self, request, *args, **kwargs):
        images = Image.objects.filter(user=request.user)
        serializer = self.get_serializer(images, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        if self.request.user.tier.have_original_url:
            serializer.save(user=self.request.user, original=serializer.validated_data.get('img'))
        else:
            serializer.save(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        folder_path = os.path.join(settings.MEDIA_ROOT, f'imgs/{instance.id}')
        response = super().destroy(request, *args, **kwargs)
        if os.path.isdir(folder_path):
            shutil.rmtree(folder_path)
        return response

    @action(detail=True, methods=['POST'])
    def create_expiring_link(self, request, pk):
        if not self.request.user.tier.can_create_links:
            return HttpResponseForbidden()
        time_to_live = int(request.data.get('time_to_live'))

        if not time_to_live:
            return Response({'error': 'time_to_live is required'}, status=status.HTTP_400_BAD_REQUEST)
        time_to_live = int(time_to_live)
        if 300 > time_to_live or time_to_live > 30000:
            return Response({'error': f'time_to_live is limited between 300 and 30000 seconds'},
                            status=status.HTTP_400_BAD_REQUEST)
        image = get_object_or_404(Image, id=pk, user=request.user)
        link = Link.objects.create(image=image, timestamp_start=int(time()), time_to_live=time_to_live)
        return Response({'url': link.id}, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['GET'])
    def link(self, request, pk):
        link = get_object_or_404(Link, id=pk)
        if link.timestamp_start + link.time_to_live > int(time()):
            image = get_object_or_404(Image, pk=link.image.id)
            try:
                response = FileResponse(open(f'{image.original}', 'rb'))
                return response
            except FileNotFoundError:
                return HttpResponseNotFound()
        return HttpResponseNotFound()
