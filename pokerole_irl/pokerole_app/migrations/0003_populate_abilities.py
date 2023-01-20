from django.db import migrations
import os
import json


def create_abilities(apps, _):
    Ability = apps.get_model("pokerole_app", "Ability")
    BASE_DIR = os.path.join(os.path.basename(
        os.getcwd()), 'static/Version20/Abilities')

    for filename in os.listdir(BASE_DIR):
        ability = json.load(open(os.path.join(BASE_DIR, filename)))
        Ability.objects.update_or_create(name=ability.get("Name", None), defaults={
            "effect": ability.get("Effect", "No effect."),
            "description": ability.get("Description", "No description.")
        })


class Migration(migrations.Migration):
    dependencies = [
        ('pokerole_app', '0002_populate_types')
    ]

    operations = [
        migrations.RunPython(
            create_abilities, reverse_code=migrations.RunPython.noop)
    ]
