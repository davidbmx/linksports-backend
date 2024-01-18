from django.contrib import admin
from .models import Post, PostAsset

# Register your models here.


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'description', 'type_post']

@admin.register(PostAsset)
class PostImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'file', 'type_file', 'width', 'height',]
