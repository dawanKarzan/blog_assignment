from django.db import models

class Role(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    can_read = models.BooleanField(default=False)
    can_create = models.BooleanField(default=False)
    can_update = models.BooleanField(default=False)
    can_delete = models.BooleanField(default=False)