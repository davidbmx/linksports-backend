from django.contrib import admin
from configuration.models import Sport

# Register your models here.
@admin.register(Sport)
class SportAdmin(admin.ModelAdmin):
    pass