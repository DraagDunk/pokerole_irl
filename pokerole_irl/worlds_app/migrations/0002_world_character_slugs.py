# Generated by Django 3.2.19 on 2023-05-05 20:41

from django.db import migrations, models
from django.template.defaultfilters import slugify


def populate_world_slugs(apps, schema_editor):
    World = apps.get_model("worlds_app", "World")

    for world in World.objects.iterator():
        # Save to set the slug
        world.slug = slugify(world.name)
        world.save()


def populate_character_slugs(apps, schema_editor):
    Character = apps.get_model("worlds_app", "Character")

    for character in Character.objects.iterator():
        # Save to set the slug
        character.slug = slugify(str(character))
        character.save()


class Migration(migrations.Migration):

    dependencies = [
        ('worlds_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='character',
            name='slug',
            field=models.SlugField(default='slug', blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='world',
            name='slug',
            field=models.SlugField(default='slug', blank=True),
            preserve_default=False,
        ),
        migrations.RunPython(populate_world_slugs,
                             reverse_code=migrations.RunPython.noop),
        migrations.RunPython(populate_character_slugs,
                             reverse_code=migrations.RunPython.noop)
    ]
