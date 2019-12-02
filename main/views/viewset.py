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

    def get_queryset(self):
        if self.action == 'list':
            return Post.user_posts.shared_with_current_user_or_created_by(self.request.user)
        return Post.objects.all()

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)

    @action(methods=['GET'], detail=False)
    def my_posts(self, request):
        posts = Post.user_posts.created_by_user(self.request.user)
        serializer = PostSerializer(posts, many=True, context={'request': request})
        return Response(serializer.data)

    @action(methods=['GET'], detail=False)
    def my_recent_posts(self, request):
        posts = Post.user_posts.most_recent(self.request.user)
        serializer = PostSerializer(posts, many=True, context={'request': request})
        return Response(serializer.data)


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProfileSerializerFull
        return ProfileSerializer

    @action(methods=['GET'], detail=True)
    def department_profiles(self, request, pk):
        department = Department.objects.get(id=pk)
        serializer = ProfileSerializer(department.profiles, many=True)
        return Response(serializer.data)

    @action(methods=['GET'], detail=False)
    def company_profiles(self, request):
        company = self.request.user.profile.company
        profiles = Profile.profiles.all_employees_of_company_ordered(company)
        serializer = ProfileSerializerFull(profiles, many=True)
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


class ReportViewSet(viewsets.ModelViewSet):
    serializer_class = ReportSerializer
    permission_classes = (IsAuthenticated, IsAuthorOrReadOnly)

    def get_queryset(self):
        return Report.my_reports.created_by_user(self.request.user)

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)

    @action(methods=['GET'], detail=False)
    def reports_of_employees(self, request):
        reports = Report.my_reports.reports_of_my_employees(self.request.user)
        serializer = ReportSerializer(reports, many=True)
        return Response(serializer.data)

    @action(methods=['GET'], detail=True)
    def reports_of_the_employee(self, request, pk):
        employee = Profile.objects.get(id=pk)
        reports = Report.my_reports.reports_of_the_employee(self.request.user, employee)
        serializer = ReportSerializer(reports, many=True)
        return Response(serializer.data)


class PostDocumentViewSet(viewsets.ModelViewSet):
    serializer_class = PostDocumentSerializer
    permission_classes = (IsAuthenticated,)
    queryset = PostDocument.objects.all()

    # @action(methods=['GET'], detail=False)
    # def my_documents(self, request):
    #     docs = PostDocument.documents.my_documents(self.request.user)
    #     serializer = PostDocumentSerializerFull(docs, many=True)
    #     return Response(serializer.data)
    #
    # @action(methods=['GET'], detail=False)
    # def documents_for_me(self, request):
    #     myposts=Post.user_posts.shared_with_current_user_or_created_by(self.request.user)
    #     docs = PostDocument.documents.documents_for_me(self.request.user,myposts)
    #     serializer = PostDocumentSerializerFull(docs, many=True)
    #     return Response(serializer.data)