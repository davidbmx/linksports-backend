from django.db import models

from lib.models import MainModel
from posts.models import Post

# Create your models here.
def upload_image(instance, filename):
    return f'user/{instance.post.user.uid}/posts/images/{filename}'

class PostImage(MainModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_images')
    image = models.ImageField(upload_to=upload_image)
    width = models.IntegerField(default=0)
    height = models.IntegerField(default=0)

    def __str__(self):
        return self.image.name