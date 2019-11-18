from rest_framework import serializers
from main.models import *
from users.serializers import *

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

  class Meta:
    model = Post
    fields = '__all__'
    read_only_fields = ('created_date', 'author',)


class CommentSerializer(serializers.ModelSerializer):
  author = CustomUserSerializer(read_only=True)
  class Meta:
    model = Comment
    fields = '__all__'
    read_only_fields = ('created_date', 'author', 'post',)