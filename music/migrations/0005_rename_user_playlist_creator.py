# Generated by Django 4.1.7 on 2023-02-27 03:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0004_alter_playlist_song'),
    ]

    operations = [
        migrations.RenameField(
            model_name='playlist',
            old_name='user',
            new_name='creator',
        ),
    ]
