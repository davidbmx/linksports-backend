from django.db import models
from django.contrib.auth.models import AbstractUser

from lib.models import MainModel

def upload_image(instance, filename):
    return f'avatar/{instance.uid}/{filename}'

class User(MainModel, AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name']
    email = models.EmailField(
        'email address',
        unique=True,
        error_messages={
            'unique': 'Correo ya se encuentra registrado'
        }
    )
    name = models.CharField(max_length=30, blank=True, null=True)
    uid = models.TextField(db_index=True, blank=True, null=True)
    bookmarks = models.IntegerField(default=0)
    num_fans = models.IntegerField(default=0)
    num_following = models.IntegerField(default=0)
    num_posts = models.IntegerField(default=0)
    description = models.CharField(max_length=80, blank=True, null=True)
    active = models.BooleanField(default=True)
    avatar = models.ImageField(upload_to=upload_image, blank=True, null=True)

    def __str__(self):
        return self.username

    def get_short_name(self):
        return self.username

class Device(MainModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='devices')
    device_id = models.CharField(max_length=150)
    platform = models.CharField(max_length=150)
    version = models.CharField(max_length=150)

    def __str__(self):
        return self.platform
    
class Following(MainModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_follow')
    user_following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_follower')

    def __str__(self):
        return f'{self.user.name} following by {self.user_following}'
    

