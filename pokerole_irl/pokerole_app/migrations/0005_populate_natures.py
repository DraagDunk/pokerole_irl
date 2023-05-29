from django.db import migrations
import os
import json

from django.conf import settings


def create_natures(apps, _):
    Nature = apps.get_model("pokerole_app", "Nature")

    DIR = os.path.join(settings.BASE_DIR, 'static/Version20/Natures')

    for filename in os.listdir(DIR):
        nature = json.load(open(os.path.join(DIR, filename)))
        Nature.objects.update_or_create(name=nature.get("Name", None), defaults={
            "confidence": nature.get("Confidence", 0),
            "keywords": nature.get("Keywords", ""),
            "description": nature.get("Description", "")
        })


class Migration(migrations.Migration):
    dependencies = [
        ('pokerole_app', '0004_populate_moves')
    ]

    operations = [
        # migrations.RunPython(
        #     create_natures, reverse_code=migrations.RunPython.noop)
    ]
