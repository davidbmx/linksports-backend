from django.db import models

from lib.models import MainModel
from posts.models import Post

# Create your models here.
def upload_file(instance, filename):
    return f'user/{instance.post.user.uid}/posts/assets/{filename}'

class PostAsset(MainModel):
    TYPE_CHOICE = (
        ('VIDEO', 'VIDEO'),
        ('IMAGE', 'IMAGE'),
    )
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_assets')
    file = models.FileField(upload_to=upload_file)
    type_file = models.CharField(max_length=5, choices=TYPE_CHOICE, default=TYPE_CHOICE[1][0])
    width = models.IntegerField(default=0)
    height = models.IntegerField(default=0)

    def __str__(self):
        return self.image.name