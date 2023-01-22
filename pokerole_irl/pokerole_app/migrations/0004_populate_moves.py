from django.db import migrations
import os
import json

from django.conf import settings


def create_moves(apps, _):
    Move = apps.get_model("pokerole_app", "Move")
    Type = apps.get_model("pokerole_app", "Type")

    DIR = os.path.join(settings.BASE_DIR, 'static/Version20/Moves')

    for filename in os.listdir(DIR):
        move = json.load(open(os.path.join(DIR, filename)))
        try:
            Move.objects.update_or_create(name=move.get("Name", None), defaults={
                "move_type": Type.objects.filter(name=move.get("Type", None)).first() if move.get("Type", None) else None,
                "damage_type": move.get("DmgType", ""),
                "power": move.get("Power", None),
                "damage_stat": move.get("Damage1", ""),
                "damage_modifier": move.get("Damage2", ""),
                "primary_accuracy": move.get("Accuracy1", ""),
                "secondary_accuracy": move.get("Accuracy2", ""),
                "target": move.get("Target", ""),
                "effect": move.get("Effect", ""),
                "description": move.get("Description", ""),
                "attributes": json.dumps(move.get("Attributes", {})),
                "added_effects": json.dumps(move.get("AddedEffects", {}))
            })
        except Exception as e:
            print(
                f"While populating {move.get('Name')}, encountered error: {e}")


class Migration(migrations.Migration):
    dependencies = [
        ('pokerole_app', '0003_populate_abilities')
    ]

    operations = [
        migrations.RunPython(
            create_moves, reverse_code=migrations.RunPython.noop)
    ]