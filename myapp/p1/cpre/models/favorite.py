from django.db import models
from .post import Post
from .custom_user import CustomUser

class Favorite(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='favorites')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='favorites')

    class Meta:
        unique_together = ('author', 'post')