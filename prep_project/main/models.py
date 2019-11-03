from django.db import models
from django.contrib.auth.models import User, AbstractUser, AbstractBaseUser, PermissionsMixin, BaseUserManager
from rest_framework.authtoken.models import Token


class Company(models.Model):
  name = models.CharField(max_length=255)


class Department(models.Model):
  name = models.CharField(max_length=255)
  company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='departments')


class Profile(models.Model):
  first_name = models.CharField(max_length=255, null=True)
  phone = models.CharField(max_length=255, null=True)
  isFemale = models.BooleanField(null=True)
  last_name = models.CharField(max_length=255, null=True)
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='department_employees', null=True)
  is_head = models.BooleanField(null=True)
  avatar = models.CharField(max_length=1000, null=True)

  @property
  def company(self):
    return self.department.company

  @property
  def head(self):
    return Profile.objects.get(department=self.department, is_head=True).id


class Report(models.Model):
  author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports')
  text = models.CharField(max_length=255)
  date_from = models.DateTimeField(auto_now=True)
  date_to = models.DateTimeField()


class Post(models.Model):
  author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
  text = models.CharField(max_length=2550)
  created_date = models.DateTimeField(auto_now=True)
  file = models.FileField(null=True)


class Comment(models.Model):
  author = models.ForeignKey(User, on_delete=models.CASCADE)
  text = models.CharField(max_length=255)
  created_date = models.DateTimeField(auto_now=True)
  post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
