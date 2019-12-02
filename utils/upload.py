import os
import shutil
from datetime import datetime


def post_document_path(instance, filename):
    company_id = instance.post.author.profile.department.company.id
    post_id = instance.post.id
    return f'companies/{company_id}/posts/{post_id}/{filename}'

def avatar_path(instance, filename):
    return f'profiles/{filename}'


def file_delete_path(document):
    print(document)
    task_path = os.path.abspath(os.path.join(document.path, '..'))
    shutil.rmtree(task_path)
