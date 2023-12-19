# Generated by Django 4.2.5 on 2023-12-19 02:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='postbookmark',
            name='user_bookmark',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_book', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='postcomment',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post', to='posts.post'),
        ),
        migrations.AlterField(
            model_name='postcomment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_comment', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='postlike',
            name='user_like',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_like', to=settings.AUTH_USER_MODEL),
        ),
    ]
