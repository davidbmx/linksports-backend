from django.db import models
from django.contrib.auth.models import User

from lib.models import MainModel
from .post import Post

class PostLike(MainModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_likes')
    user_like = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='post_like')

    def __str__(self):
        return self.user