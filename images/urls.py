from rest_framework import routers

from images.views import ImageViewSet

router = routers.SimpleRouter()
router.register(r'', ImageViewSet)

urlpatterns = []

urlpatterns += router.urls
