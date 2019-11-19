from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token

from main.views import *

urlpatterns = [
    path('posts/<int:pk>/comments/', CommentList.as_view()),
    # path('departments/<int:pk>/profiles/', ProfilesOfDepartment.as_view())

]

router = DefaultRouter()
router.register('posts', PostViewSet, base_name='main')
router.register('profiles', ProfileViewSet, base_name='main')
router.register('companies', CompanyViewSet, base_name='main')
router.register('departments', DepartmentViewSet, base_name='main')

urlpatterns += router.urls
