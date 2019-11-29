from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from main.models import *
from main.serializers import *
from users.serializers import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.db.models import Q
from main.permissions import *


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated, IsAuthorOrReadOnly)
    filter_backends = (DjangoFilterBackend,
                       filters.SearchFilter,
                       filters.OrderingFilter)

    search_fields = ('text',)
    ordering_fields = ('created_date',)
    ordering = ('-created_date',)

    def get_serializer_class(self):
        if self.action == 'list':
            return PostSerializerFull
        elif self.action == 'retrieve':
            return PostSerializerFull
        return PostSerializer

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)

    #исправить на менеджера
    @action(methods=['GET'], detail=False)
    def posts_for_me(self, request):
        print('hh')
        userposts = request.user.my_userposts.all()
        print(userposts)
        posts = Post.objects.filter(Q(id__in=userposts.values('post_id') ) | Q(author_id=self.request.user.id))
        serializer = PostSerializer(posts, many=True, context={'request': request})
        return Response(serializer.data)


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

    @action(methods=['GET'], detail=True)
    def department_profiles(self, request, pk):
        department = Department.objects.get(id=pk)
        serializer = ProfileSerializer(department.profiles, many=True)
        return Response(serializer.data)


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = (IsCompanyAdmin | IsSuperUser,)

    @action(methods=['GET'], detail=True)
    def company_departments(self, request, pk):
        company = Company.objects.get(id=pk)
        serializer = DepartmentSerializer(company.departments, many=True)
        return Response(serializer.data)


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = (IsSuperUser,)
