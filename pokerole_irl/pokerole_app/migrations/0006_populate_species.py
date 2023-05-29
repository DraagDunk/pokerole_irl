from django.db import migrations, models, transaction
import os
import json

from django.conf import settings


def create_species(apps, _):
    Species = apps.get_model("pokerole_app", "PokemonSpecies")
    Type = apps.get_model("pokerole_app", "Type")
    Ability = apps.get_model("pokerole_app", "Ability")

    DIR = os.path.join(settings.BASE_DIR, 'static/Version20/Pokedex')

    for filename in os.listdir(DIR):
        species = json.load(open(os.path.join(DIR, filename)))
        try:
            with transaction.atomic():
                sp_model, _ = Species.objects.update_or_create(name=species.get("Name", None), defaults={
                    "number": species.get("Number"),
                    "dex_id": species.get("DexID"),
                    "primary_type": Type.objects.filter(name=species.get("Type1", None)).first(),
                    "secondary_type": Type.objects.filter(name=species.get("Type2", None)).first(),
                    "hidden_ability": Ability.objects.filter(name=species.get("HiddenAbility")).first(),
                    "event_ability": Ability.objects.filter(name=species.get("EventAbilities", None)).first(),
                    "recommended_rank": species.get("RecommendedRank", ""),
                    "gender_type": species.get("GenderType", ""),
                    "legendary": species.get("Legendary", False),
                    "good_starter": species.get("GoodStarter", False),
                    "category": species.get("DexCategory", ""),
                    "height": species.get("Height", {}).get("Meters", 0),
                    "weight": species.get("Weight", {}).get("Kilograms", 0),
                    "description": species.get("DexDescription", ""),
                    "image_name": species.get("Image"),

                    "base_hp": species.get("BaseHP"),
                    "base_strength": species.get("Strength"),
                    "base_dexterity": species.get("Dexterity"),
                    "base_vitality": species.get("Vitality"),
                    "base_special": species.get("Special"),
                    "base_insight": species.get("Insight"),

                    "max_strength": species.get("MaxStrength"),
                    "max_dexterity": species.get("MaxDexterity"),
                    "max_vitality": species.get("MaxVitality"),
                    "max_special": species.get("MaxSpecial"),
                    "max_insight": species.get("MaxInsight")
                })

                sp_model.abilities.add(Ability.objects.filter(
                    name=species.get("Ability1")).first())
                if species.get("Ability2"):
                    sp_model.abilities.add(Ability.objects.filter(
                        name=species.get("Ability2")).first())
        except Exception as e:
            print(
                f"While populating {species.get('Name')}, encountered error: {e}")


class Migration(migrations.Migration):
    dependencies = [
        ('pokerole_app', '0005_populate_natures')
    ]

    operations = [
        migrations.AlterField(
            model_name='pokemonspecies',
            name='dex_id',
            field=models.CharField(max_length=20),
        ),
        # migrations.RunPython(
        #     create_species, reverse_code=migrations.RunPython.noop),
    ]
