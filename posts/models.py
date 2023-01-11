from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractUser
from tinymce.models import HTMLField
# Create your models here.

class User(AbstractUser):
    pass


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_post")
    title = models.CharField(max_length=165)
    body = HTMLField()
    created_at = models.DateTimeField(default=datetime.now, blank=True)