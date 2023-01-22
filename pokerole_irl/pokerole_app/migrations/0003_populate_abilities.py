from django.db import migrations
import os
import json

from django.conf import settings


def create_abilities(apps, _):
    Ability = apps.get_model("pokerole_app", "Ability")
    DIR = os.path.join(settings.BASE_DIR, 'static/Version20/Abilities')

    for filename in os.listdir(DIR):
        ability = json.load(open(os.path.join(DIR, filename)))
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
