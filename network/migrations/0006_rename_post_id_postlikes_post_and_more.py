# Generated by Django 4.2.3 on 2023-10-21 14:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0005_post_likes'),
    ]

    operations = [
        migrations.RenameField(
            model_name='postlikes',
            old_name='post_id',
            new_name='post',
        ),
        migrations.RenameField(
            model_name='postlikes',
            old_name='user_id',
            new_name='user',
        ),
    ]
