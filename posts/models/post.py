import uuid
from django.db import models
from django.contrib.auth.models import User

from lib.models import MainModel

# Create your models here.

class Post(MainModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    videoUrl: models.TextField()
    tags: models.TextField()
    sport = models.CharField(max_length=100)
    num_likes = models.IntegerField(default=0)
    num_views = models.IntegerField(default=0)
    num_comments = models.IntegerField(default=0)

    def __str__(self):
        return self.title
