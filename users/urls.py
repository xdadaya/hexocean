from django.urls import path
from rest_framework import routers

from users.views import RegistrationAPIView

router = routers.SimpleRouter()

app_name = 'users'

urlpatterns = [
    path('register', RegistrationAPIView.as_view(), name='register'),
]

urlpatterns += router.urls
