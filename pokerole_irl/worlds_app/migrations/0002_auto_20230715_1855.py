# Generated by Django 3.2.18 on 2023-07-15 18:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('worlds_app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='character',
            old_name='slug',
            new_name='character_slug',
        ),
        migrations.RenameField(
            model_name='world',
            old_name='slug',
            new_name='world_slug',
        ),
        migrations.RemoveField(
            model_name='worldmember',
            name='slug',
        ),
    ]
