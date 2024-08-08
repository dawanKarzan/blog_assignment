from django.db import models
from .tag import Tag
from .custom_user import CustomUser

class Post(models.Model):
    title = models.CharField(max_length=255)
    html_body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    header_image = models.ImageField(upload_to='post_header/', default='post_header/default.jpg')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, related_name='posts', related_query_name='post')