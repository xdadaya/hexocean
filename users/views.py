from django.db import IntegrityError
from django.http import HttpRequest
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from users.serializers import RegistrationSerializer


class RegistrationAPIView(APIView):
    def post(self, request: HttpRequest) -> Response:
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response({'msg': "Successful registration", "user": serializer.data},
                                status=status.HTTP_201_CREATED)
            except IntegrityError:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
