from django.db import models
# from django.contrib.auth.models import CustomUser, AbstractCustomUser, AbstractBaseCustomUser, PermissionsMixin, BaseCustomUserManager
from users.models import CustomUser
from rest_framework.authtoken.models import Token
from utils.upload import *
from utils.validators import post_document_size, post_document_extension


class Company(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'

    def __str__(self):
        return self.name


class Department(models.Model):
    name = models.CharField(max_length=255)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='departments')

    def __str__(self):
        return f'{self.name} ({self.company})'


class Profile(models.Model):
    phone = models.CharField(max_length=255, null=True)
    is_company_admin = models.BooleanField(default=False)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='profiles')
    is_head = models.BooleanField(null=True)
    avatar = models.ImageField(upload_to=avatar_path, null=True)
    date_of_birth = models.DateField(null=True)

    @property
    def company(self):
        return self.department.company

    @property
    def head(self):
        try:
            return Profile.objects.get(department=self.department, is_head=True).user.id
        except:
            return None

    def __str__(self):
        return f'{self.user.email}, department - {self.department.name}'


class Report(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='reports')
    text = models.CharField(max_length=255)
    date_from = models.DateTimeField(auto_now=True)
    date_to = models.DateTimeField()

    def __str__(self):
        return f'{self.author.username}, {self.date_from}'


class Post(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='posts')
    text = models.CharField(max_length=2550)
    created_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.author.email}, created at:{self.created_date}'


class PostDocument(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='documents')
    document = models.FileField(upload_to=post_document_path, validators=[post_document_size, post_document_extension],
                                null=True)

    def __str__(self):
        return f'{self.post}(document #){self.id}'


class Comment(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    created_date = models.DateTimeField(auto_now=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return f'comment of {self.author.email}, post: {self.post}'


# any to many чтоб
class UserPost(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='my_userposts')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_users')

    def __str__(self):
        return f'user{self.user.email}, post: {self.post}'
