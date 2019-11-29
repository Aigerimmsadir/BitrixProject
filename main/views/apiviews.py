from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from main.serializers import *
from django.shortcuts import get_object_or_404



class CommentList(APIView):
    http_method_names = ['get', 'post']
    permission_classes = (IsAuthenticated, IsAuthorOrReadOnly)

    def get(self, request, pk):
        post_comment = get_object_or_404(PostComment, pk=pk)
        comments = post_comment.comments.all()
        serializer = CommentSerializer(comments, many=True,context={'request': request})
        return Response(serializer.data)

    def post(self, request, pk):
        serializer = CommentSerializer(data=request.data, context={'request': request, 'post_comment_id': self.kwargs['pk']})
        if serializer.is_valid():
            serializer.save(post_comment_id=pk)
            return Response(serializer.data)
        return Response(serializer.errors)



class PostCommentList(APIView):
    http_method_names = ['get', 'post']
    permission_classes = (IsAuthenticated, IsAuthorOrReadOnly)

    def get_post(self, pk):
        return Post.objects.get(id=pk)

    def get(self, request, pk):
        post = self.get_post(pk)
        comments = post.post_comments.all()
        serializer = PostCommentSerializer(comments, many=True,context={'request': request})
        return Response(serializer.data)

    def post(self, request, pk):
        serializer = PostCommentSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(post_id=pk, author=request.user)
            return Response(serializer.data)
        return Response(serializer.errors)

# class CommentToCommentViewSet(viewsets.ModelViewSet):
#     queryset = CommentToComment.objects.all()
#     serializer_class = CommentToCommentSerializer
