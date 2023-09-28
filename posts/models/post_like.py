from django.db import models
from django.contrib.auth.models import User

from lib.models import MainModel
from .post import Post

class PostLike(MainModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user_like = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user