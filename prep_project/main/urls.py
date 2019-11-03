from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token


from main.views import *

urlpatterns = [
    path('login/', obtain_jwt_token),
    path('posts/<int:pk>/comments/', CommentList.as_view())
]


router = DefaultRouter()
router.register('users', UserViewSet, base_name='main')
router.register('register', RegisterUserViewSet, base_name='main')
router.register('posts', PostViewSet, base_name='main')
router.register('profiles', ProfileViewSet, base_name='main')
router.register('departments', DepartmentViewSet, base_name='main')

urlpatterns += router.urls
