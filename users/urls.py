from rest_framework import routers
from django.urls import path, include
from .views import UserViewSet, authenticate_user

router = routers.DefaultRouter()
router.register('', UserViewSet)

urlpatterns = [
    path('users/', include(router.urls)),
    path('api-token-auth/', authenticate_user),
]
