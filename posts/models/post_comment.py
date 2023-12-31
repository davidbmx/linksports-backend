from django.db import models
from django.contrib.auth.models import User

from lib.models import MainModel
from .post import Post

class PostComment(MainModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post')
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='post_comment')
    comment = models.TextField()

    def __str__(self):
        return self.user.username
