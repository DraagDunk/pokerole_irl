# Generated by Django 3.2.18 on 2023-05-01 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pokerole_app', '0014_pokedexentry_description_and_rarity_change'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pokedexentry',
            name='description',
            field=models.TextField(blank=True, default=''),
        ),
    ]