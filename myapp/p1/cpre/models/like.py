from django.db import models
from .post import Post
from .custom_user import CustomUser

class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='likes')

    class Meta:
        unique_together = ('author', 'post')