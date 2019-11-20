from rest_framework import serializers
from main.models import *
from users.serializers import *


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = '__all__'
        read_only_fields = ('date_from', 'author',)


class PostSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(read_only=True)
    user_ids = serializers.ListField(
        child=serializers.IntegerField(), required=False
    )
    documents = serializers.ListField(
        child=serializers.FileField(), required=False
    )

    class Meta:
        model = Post
        fields = ('text', 'author', 'user_ids', 'documents', 'created_date')
        read_only_fields = ('created_date', 'author',)
        write_only_fields = ('user_ids', 'documents',)

    def create(self, validated_data):
        user_ids = validated_data.pop('user_ids')
        documents = validated_data.pop('documents')
        post = Post(**validated_data)
        post.save()
        for i in user_ids:
            user = CustomUser.objects.get(id=i)
            userpost = UserPost(user=user, post=post)
            userpost.save()
        for j in documents:
            postdocument = PostDocument(post=post, document=j)
            postdocument.save()

        return post


class CommentSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('created_date', 'author', 'post',)
