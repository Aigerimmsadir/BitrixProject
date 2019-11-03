from rest_framework import serializers
from main.models import *


class CompanySerializer(serializers.ModelSerializer):
  class Meta:
    model = Company
    fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
  company = CompanySerializer()

  class Meta:
    model = Profile
    fields = (
    'first_name', 'last_name', 'phone', 'isFemale', 'is_head', 'avatar', "user", "department", 'company', 'head')

    read_only_fields = ('user',)


class UserSerializer(serializers.ModelSerializer):
  password = serializers.CharField(write_only=True)
  profile = ProfileSerializer()

  class Meta:
    model = User
    fields = ('username', 'email', 'date_joined', 'password', 'profile')
    read_only_fields = ('profile',)

  def create(self, validated_data):
    user = User.objects.create_user(**validated_data)
    profile = Profile.objects.create(user=user)
    return user


class DepartmentSerializer(serializers.ModelSerializer):
  class Meta:
    model = Department
    fields = '__all__'


class ReportSerializer(serializers.ModelSerializer):
  author = serializers.HiddenField(default=serializers.CurrentUserDefault())

  class Meta:
    model = Report
    fields = '__all__'
    read_only_fields = ('date_from', 'author',)


class PostSerializer(serializers.ModelSerializer):
  author = UserSerializer(read_only=True)

  class Meta:
    model = Post
    fields = '__all__'
    read_only_fields = ('created_date', 'author',)


class CommentSerializer(serializers.ModelSerializer):
  author = UserSerializer(read_only=True)
  class Meta:
    model = Comment
    fields = '__all__'
    read_only_fields = ('created_date', 'author', 'post',)
