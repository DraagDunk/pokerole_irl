from django.db import migrations
import os
import json


def create_movesets(apps, _):
    MoveSet = apps.get_model("pokerole_app", "MoveSet")
    Move = apps.get_model("pokerole_app", "Move")
    PokemonSpecies = apps.get_model("pokerole_app", "PokemonSpecies")

    BASE_DIR = os.path.join(os.path.basename(
        os.getcwd()), 'static/Version20/Learnsets')

    for filename in os.listdir(BASE_DIR):
        learnset = json.load(open(os.path.join(BASE_DIR, filename)))
        species = PokemonSpecies.objects.get(name=learnset.get("Name"))
        for move in learnset.get("Moves", []):
            try:
                move_model = Move.objects.get(name=move.get("Name"))
                MoveSet.objects.update_or_create(species=species, move=move_model, defaults={
                    "learned": move.get("Learned")
                })
            except:
                print(f"{move.get('Name')} does not exist.")


class Migration(migrations.Migration):
    dependencies = [
        ('pokerole_app', '0007_populate_items')
    ]

    operations = [
        migrations.RunPython(
            create_movesets, reverse_code=migrations.RunPython.noop)
    ]
