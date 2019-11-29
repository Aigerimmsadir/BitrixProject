from rest_framework import serializers
from main.models import *
from users.serializers import *
from django.db import transaction

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


class PostSerializerShort(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


class PostSerializerFull(PostSerializerShort):
    author = CustomUserSerializer()

    class Meta(PostSerializerShort.Meta):
        fields = PostSerializerShort.Meta.fields


class PostSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(read_only=True)
    user_ids = serializers.ListField(
        child=serializers.IntegerField(), required=False
    )
    documents_uploaded = serializers.ListField(
        child=serializers.FileField(), required=False
    )

    class Meta:
        model = Post
        fields = ('id','text', 'author', 'user_ids', 'documents_uploaded', 'created_date')
        read_only_fields = ('created_date', 'author',)

    def create(self, validated_data):
        with transaction.atomic():
            user_ids = validated_data.pop('user_ids')
            print(user_ids)
            documents = validated_data.pop('documents_uploaded')
            print(documents)
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


# class CommentSerializer(serializers.ModelSerializer):
#     author = CustomUserSerializer(read_only=True)

#     class Meta:
#         model = Comment
#         fields = '__all__'
#         read_only_fields = ('created_date', 'author', 'comment',)

class PostCommentSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(read_only=True)

    class Meta:
        model = PostComment
        fields = '__all__'
        read_only_fields = ('created_date', 'author', 'post',)

class CommentSerializer(serializers.Serializer):
    author = CustomUserSerializer(read_only=True)
    post_comment = PostCommentSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('created_date', 'author', 'comment', 'post_comment')

    def create(self, validated_data):
           # commented_id = self.context['post_comment_id']
           user = self.context['request'].user
           commenter = Comment.objects.create(author=user, **validated_data)
           # comment_to_comment = CommentToComment.objects.create(commented_id=commented_id, commenter_id=commenter.id)
           return commenter


    def update(self, instance, validated_data):
           # commented_id = self.context['post_comment_id']
           instance.text = validated_data.get('text', instance.text)
           instance.save()
           # comment_to_comment = CommentToComment.objects.create(commented_id=commented_id, commenter_id=commenter.id)
           return instance


