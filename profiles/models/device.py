from django.db import models

from lib.models import MainModel
from .profile import Profile

class Device(MainModel):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='devices')
    device_id = models.CharField(max_length=150)
    platform = models.CharField(max_length=150)
    version = models.CharField(max_length=150)

    def __str__(self):
        return self.platform


