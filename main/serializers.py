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
            if len(user_ids)==0:
                user_ids=list( CustomUser.objects.all().values_list('id', flat=True))
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


class CommentSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('created_date', 'author', 'post',)
