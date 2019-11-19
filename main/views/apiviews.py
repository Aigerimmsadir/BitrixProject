from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from main.models import *
from main.serializers import *
from users.serializers import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters


class CommentList(APIView):
    http_method_names = ['get', 'post']
    permission_classes = (IsAuthenticated,)

    def get_project(self, pk):
        return Post.objects.get(id=pk)

    def get(self, request, pk):
        post = self.get_project(pk)
        comments = post.comments.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request, pk):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(post_id=pk, author=request.user)
            return Response(serializer.data)
        return Response(serializer.errors)

