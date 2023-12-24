import uuid
from django.db import models

from lib.models import MainModel

# Create your models here.
def upload_image(instance, filename):
    return f'user/{instance.user.uid}/posts/{filename}'

class Post(MainModel):
    TYPE_CHOICE = (
        ('VIDEO', 'VIDEO'),
        ('IMAGE', 'IMAGE'),
    )
    VISIBILITY_CHOICE = (
        ('PUBLIC', 'PUBLIC'),
        ('DRAFT', 'DRAF'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='posts')
    description = models.CharField(max_length=200, blank=True, null=True)
    video = models.FileField(upload_to=upload_image, blank=True, null=True)
    video_thumb = models.FileField(upload_to=upload_image, blank=True, null=True)
    tags = models.TextField()
    sport = models.CharField(max_length=100)
    num_likes = models.IntegerField(default=0)
    num_views = models.IntegerField(default=0)
    num_comments = models.IntegerField(default=0)
    type_post = models.CharField(max_length=10, choices=TYPE_CHOICE, default=TYPE_CHOICE[0][0])
    visibility = models.CharField(max_length=10, choices=VISIBILITY_CHOICE, default=VISIBILITY_CHOICE[0][0])

    def __str__(self):
        return self.description
