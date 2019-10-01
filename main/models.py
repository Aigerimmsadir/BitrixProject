from django.db import models
from users.models import CustomUser
from main.constants import *


class Company(models.Model):
    name = models.CharField(max_length=80)
    logo = models.FileField()

    class Meta:
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'

    def __str__(self):
        return self.name


class Department(models.Model):
    name = models.CharField(max_length=80)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class EmployeeManager(models.Manager):
    def get_queryset(self, department_id):
        return super().get_queryset().filter(department_id=department_id)


class Employee(models.Model):
    first_name = models.CharField(max_length=80, null=True)
    last_name = models.CharField(max_length=80, null=True)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    position = models.IntegerField(choices=POSITIONS)
    date_of_birth = models.DateTimeField(null=True)
    objects = models.Manager()
    department_employees = EmployeeManager()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Post(models.Model):
    text = models.CharField(max_length=3000, blank=True)
    created_date = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)


class PostDocument(models.Model):
    document = models.FileField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)


class Comment(models.Model):
    text = models.CharField(max_length=3000)
    created_date = models.DateTimeField(auto_now=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)


class Report(models.Model):
    text = models.CharField(max_length=3000, blank=True)
    date_from = models.DateTimeField()
    date_to = models.DateTimeField()
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
