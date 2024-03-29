# Generated by Django 3.2.19 on 2023-05-05 20:41

from django.db import migrations, models
from django.template.defaultfilters import slugify


def populate_pokedex_slugs(apps, schema_editor):
    Pokedex = apps.get_model("pokerole_app", "Pokedex")

    for pokedex in Pokedex.objects.iterator():
        # Save to set the slug
        pokedex.slug = slugify(pokedex.name)
        pokedex.save()


class Migration(migrations.Migration):

    dependencies = [
        ('pokerole_app', '0006_pokedexentry_description_and_rarity_change'),
    ]

    operations = [
        migrations.AddField(
            model_name='pokedex',
            name='slug',
            field=models.SlugField(default='slug', blank=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='pokedexentry',
            name='description',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.RunPython(populate_pokedex_slugs,
                             reverse_code=migrations.RunPython.noop)
    ]
