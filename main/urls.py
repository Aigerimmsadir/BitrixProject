from django.urls import path
from rest_framework.routers import DefaultRouter
from main.views import *
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

from users.views import TokenObtainPairView

urlpatterns = [
    path('api/token/'  , TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('posts/<int:pk>/comments/', CommentList.as_view()),
    # path('departments/<int:pk>/profiles/', ProfilesOfDepartment.as_view())

]

router = DefaultRouter()
router.register('posts', PostViewSet, base_name='main')
router.register('profiles', ProfileViewSet, base_name='main')
router.register('companies', CompanyViewSet, base_name='main')
router.register('departments', DepartmentViewSet, base_name='main')

urlpatterns += router.urls
