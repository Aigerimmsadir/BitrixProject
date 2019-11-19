def post_document_path(instance, filename):
    company_id = instance.post.author.profile.department.company.id
    post_id = instance.post.id
    return f'companies/{company_id}/posts/{post_id}/{filename}'
