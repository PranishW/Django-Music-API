# Generated by Django 4.1.7 on 2023-02-27 14:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0013_alter_like_album_alter_like_song'),
    ]

    operations = [
        migrations.RenameField(
            model_name='like',
            old_name='song',
            new_name='sname',
        ),
    ]
