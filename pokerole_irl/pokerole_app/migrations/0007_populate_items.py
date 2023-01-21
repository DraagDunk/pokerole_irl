from django.db import migrations
import os
import json

from django.conf import settings


def create_items(apps, _):
    Item = apps.get_model("pokerole_app", "Item")
    Type = apps.get_model("pokerole_app", "Type")
    PokemonSpecies = apps.get_model("pokerole_app", "PokemonSpecies")

    DIR = os.path.join(settings.BASE_DIR, 'static/Version20/Items')

    for filename in os.listdir(DIR):
        item = json.load(open(os.path.join(DIR, filename)))
        Item.objects.update_or_create(name=item.get("Name", None), defaults={
            "description": item.get("Description", ""),
            "type_bonus": Type.objects.filter(name=item.get("TypeBonus", None)).first() if item.get("TypeBonus", None) else None,
            "value": item.get("Value", ""),
            "species": PokemonSpecies.objects.filter(name=item.get("SpecificPokemon", None)).first() if item.get("SpecificPokemon", None) else None,
            "heal_amount": item.get("HealAmount", ""),
            "suggested_price": item.get("SuggestedPrice", None),
            "PMD_price": item.get("PMDPrice", None) if item.get("PMDPrice", None) else None
        })


class Migration(migrations.Migration):
    dependencies = [
        ('pokerole_app', '0006_populate_species')
    ]

    operations = [
        migrations.RunPython(
            create_items, reverse_code=migrations.RunPython.noop)
    ]
