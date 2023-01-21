from django.db import migrations
import os
import json


def create_pokedexes(apps, _):
    Pokedex = apps.get_model("pokerole_app", "Pokedex")
    Entry = apps.get_model("pokerole_app", "PokedexEntry")
    Species = apps.get_model("pokerole_app", "PokemonSpecies")

    # National
    national, _ = Pokedex.objects.update_or_create(name="National Dex")

    for spec in Species.objects.iterator():
        Entry.objects.update_or_create(species=spec, pokedex=national, defaults={
            "number": spec.number
        })

    # Kanto
    kanto, _ = Pokedex.objects.update_or_create(name="Kanto Dex")

    for id in range(1, 152):
        id_string = str(id).zfill(4)
        species = Species.objects.get(dex_id=id_string)
        Entry.objects.update_or_create(species=species, pokedex=kanto, defaults={
            "number": id
        })


class Migration(migrations.Migration):
    dependencies = [
        ('pokerole_app', '0008_populate_movesets')
    ]

    operations = [
        migrations.RunPython(
            create_pokedexes, reverse_code=migrations.RunPython.noop)
    ]
