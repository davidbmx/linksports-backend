from django.contrib import admin
from .models import Post, PostImage

# Register your models here.


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'description', 'video', 'type_post']

@admin.register(PostImage)
class PostImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'image', 'width', 'height',]
