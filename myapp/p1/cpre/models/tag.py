from django.db import models

class TagManager(models.Manager):
    def create(self, **kwargs):
        tag, created = self.get_or_create(**kwargs)
        return tag
    
class Tag(models.Model):
    name = models.CharField(max_length=255)
    objects = TagManager()