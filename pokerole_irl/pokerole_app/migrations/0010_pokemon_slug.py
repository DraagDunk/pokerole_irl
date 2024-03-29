# Generated by Django 3.2.19 on 2023-06-05 16:04

from django.db import migrations, models
from django.template.defaultfilters import slugify


def populate_slugs(apps, schema_editor):
    Pokemon = apps.get_model("pokerole_app", "Pokemon")

    for pkmn in Pokemon.objects.all():
        # Save to generate slug
        pkmn.slug = slugify(f"{pkmn.species.name}_{pkmn.nickname}")
        pkmn.save()


class Migration(migrations.Migration):

    dependencies = [
        ('pokerole_app', '0009_pokemon'),
    ]

    operations = [
        migrations.AddField(
            model_name='pokemon',
            name='slug',
            field=models.SlugField(default='slug_missing'),
            preserve_default=False,
        ),
        migrations.RunPython(
            populate_slugs, reverse_code=migrations.RunPython.noop)
    ]
