from django.db.models.signals import post_save, pre_delete, post_delete, pre_save
from django.dispatch import receiver

from main.models import *


@receiver(post_save, sender=Company)
def company_created(sender, instance, created, **kwargs):
    if created:
        d = Department.objects.create(company=instance, name='Administrators')
        c = CustomUser()
        c.email = f'{instance.name}_admin@gmail.com'
        c.set_password('root')
        c.save()
        p = Profile.objects.create(user=c, department=d, is_company_admin=True)
        print(p)


@receiver(pre_delete, sender=Post)
def post_deleted(sender, instance, **kwargs):
    docs = PostDocument.objects.filter(post=instance)
    bool(docs)
    print(docs)
    for postdocument in docs:
        file_delete_path(document=postdocument.document)


@receiver(post_delete, sender=Profile)
def profile_deleted(sender, instance, **kwargs):
    if instance.avatar:
        file_delete_path(instance.avatar)


@receiver(pre_save, sender=Profile)
def is_head_check_uniqueness(sender, instance, **kwargs):
    if instance.is_head:
        department = instance.department
        if Profile.objects.filter(department=department, is_head=True).exists():
            raise Exception('Only 1 head of department allowed')
