from django.db import models
from django.contrib.auth.models import User

from lib.models import MainModel

# Create your models here.
class Profile(MainModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    uid = models.CharField(max_length=150, db_index=True, unique=True)
    likes = models.IntegerField(default=0)
    bookmarks = models.IntegerField(default=0)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.uid

