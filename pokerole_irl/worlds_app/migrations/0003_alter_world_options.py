# Generated by Django 3.2.19 on 2023-05-29 17:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('worlds_app', '0002_world_character_slugs'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='world',
            options={'ordering': ['name']},
        ),
    ]
