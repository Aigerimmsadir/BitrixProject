from django.db import models
from users.models import CustomUser

class UserPostManager(models.Manager):
    def created_by_user(self, user):
        return super(UserPostManager, self).get_queryset().filter(author=user)

    def most_recent(self, user):
        return super(UserPostManager, self).get_queryset().order_by('-created_date').filter(author=user)

    def shared_with_current_user(self, user):
        return user.shared_posts.all()
