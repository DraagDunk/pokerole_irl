from django.db import migrations
import os
import json

from django.conf import settings


def create_evolutions(apps, _):
    Species = apps.get_model("pokerole_app", "PokemonSpecies")
    Evolution = apps.get_model("pokerole_app", "Evolution")

    DIR = os.path.join(settings.BASE_DIR, 'static/Version20/Pokedex')

    for filename in os.listdir(DIR):
        species = json.load(open(os.path.join(DIR, filename)))
        sp_model = Species.objects.filter(name=species.get("Name")).first()
        for evo in species.get("Evolutions", []):
            if from_sp := evo.get("From", None):
                try:
                    Evolution.objects.update_or_create(
                        from_species=Species.objects.get(name=from_sp), to_species=sp_model, defaults={
                            "kind": evo.get("Kind", ""),
                            "speed": evo.get("Speed", "")
                        })
                except:
                    print(f"{from_sp} not found.")


class Migration(migrations.Migration):
    dependencies = [
        ('pokerole_app', '0009_populate_pokedexes')
    ]

    operations = [
        # migrations.RunPython(
        #     create_evolutions, reverse_code=migrations.RunPython.noop),
    ]
