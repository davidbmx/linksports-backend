from django.db import models

from lib.models import MainModel

# Create your models here.
class Sport(MainModel):
    title = models.CharField(max_length=100)
    icon = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.title