# Generated by Django 4.2.5 on 2023-12-19 06:48

from django.db import migrations, models
import django.db.models.deletion
import posts.models.post_image


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_remove_post_title_remove_post_videourl_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='image',
        ),
        migrations.CreateModel(
            name='PostImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modified at')),
                ('image', models.ImageField(upload_to=posts.models.post_image.upload_image)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_images', to='posts.post')),
            ],
            options={
                'ordering': ['-created', '-modified'],
                'get_latest_by': 'created',
                'abstract': False,
            },
        ),
    ]
