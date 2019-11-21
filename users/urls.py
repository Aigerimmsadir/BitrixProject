from rest_framework import routers
from django.urls import path, include
from .views import UserViewSet, TokenObtainPairView

router = routers.DefaultRouter()
router.register('', UserViewSet)

urlpatterns = [
    path('users/', include(router.urls)),
]
