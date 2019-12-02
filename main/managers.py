from django.db import models
from main.models import *
from users.models import *
from django.db.models import Q
from django.db.models import F


class UserPostManager(models.Manager):
    def created_by_user(self, user):
        return super(UserPostManager, self).get_queryset().filter(author=user)

    def most_recent(self, user):
        return super(UserPostManager, self).get_queryset().order_by('-created_date').filter(author=user)

    def shared_with_current_user(self, user):
        return user.shared_posts.all()

    def shared_with_current_user_or_created_by(self, user):
        userposts = user.shared_posts.all()
        posts = super(UserPostManager, self).get_queryset().filter(
            Q(id__in=userposts.values('id')) | Q(author_id=user.id))
        return posts


class ReportManager(models.Manager):
    def created_by_user(self, user):
        return super(ReportManager, self).get_queryset().filter(author=user)

    def recent(self, user):
        return super(ReportManager, self).get_queryset().order_by('-date_from').filter(author=user)

    def reports_of_my_employees(self, user):
        if user.profile.is_head:
            department = user.profile.department
            employees = department.profiles.all()
            employees_users = CustomUser.objects.filter(Q(id__in=employees.values('user')) & ~Q(id=user.id))
            print(employees_users)
            reports = super(ReportManager, self).get_queryset().filter(author__in=employees_users)
            print(reports)
            return reports

    def reports_of_the_employee(self, user, profile):
        if user.profile.is_head:
            return super(ReportManager, self).get_queryset().filter(author=profile.user)


class ProfileManager(models.Manager):
    def company_admins(self):
        return super(ProfileManager, self).get_queryset().filter(is_company_admin=True)

    def department_heads(self):
        return super(ProfileManager, self).get_queryset().filter(is_head=True)

    def all_employees_of_company(self, company):
        return super(ProfileManager, self).get_queryset().filter(department__in=company.departments.all())

    def all_employees_of_company_ordered(self, company):
        return super(ProfileManager, self).get_queryset().select_related('user').annotate(
            lastname=F('user__last_name')).order_by('lastname').filter(department__in=company.departments.all())


class PostDocumentManager(models.Manager):
    pass
#     def my_documents(self, user):
#         return super(PostDocumentManager, self).get_queryset().select_related('post').select_related('author').annotate(
#             author=F('author')
#         ).filter(author=user)
#
#     def documents_for_me(self, user, posts):
#         return super(PostDocumentManager, self).get_queryset().filter(post_id__in=posts.values('id'))
#
#     def recent_my_documents(self, user):
#         return super(PostDocumentManager, self).get_queryset().select_related('post').annotate(
#             date=F('post__created_date')).order_by('date').filter(post_id=user.id)
