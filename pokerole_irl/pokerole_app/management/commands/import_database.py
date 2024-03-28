import os
import json

from django.core.management.base import BaseCommand, CommandParser
from django.conf import settings
from django.db import transaction

from ...models import Ability, Move, Type, Nature, PokemonSpecies, Item, MoveSet, Evolution, Pokedex, PokedexEntry


def import_abilities():
    print("\nImporting abilities ...")
    DIR = os.path.join(settings.BASE_DIR, 'static/Version20/Abilities')

    for filename in os.listdir(DIR):
        ability = json.load(open(os.path.join(DIR, filename)))
        Ability.objects.update_or_create(name=ability.get("Name", None), defaults={
            "effect": ability.get("Effect", "No effect."),
            "description": ability.get("Description", "No description.")
        })


def import_moves():
    print("\nImporting moves ...")
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


def import_natures():
    print("\nImporting natures ...")
    DIR = os.path.join(settings.BASE_DIR, 'static/Version20/Natures')

    for filename in os.listdir(DIR):
        nature = json.load(open(os.path.join(DIR, filename)))
        Nature.objects.update_or_create(name=nature.get("Name", None), defaults={
            "confidence": nature.get("Confidence", 0),
            "keywords": nature.get("Keywords", ""),
            "description": nature.get("Description", "")
        })


def import_species():
    print("\nImporting species ...")
    DIR = os.path.join(settings.BASE_DIR, 'static/Version20/Pokedex')

    for filename in os.listdir(DIR):
        species = json.load(open(os.path.join(DIR, filename)))
        try:
            with transaction.atomic():
                sp_model, _ = PokemonSpecies.objects.update_or_create(dex_id=species.get("DexID"), defaults={
                    "name": species.get("Name"),
                    "number": species.get("Number"),
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


def import_items():
    print("\nImporting items ...")
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


def import_movesets():
    print("\nImporting movesets ...")
    DIR = os.path.join(settings.BASE_DIR, 'static/Version20/Learnsets')
    ranks = {"Starter": 0, "Beginner": 1, "Amateur": 2,
             "Ace": 3, "Pro": 4, "Master": 5, "Champion": 6}

    for filename in os.listdir(DIR):
        learnset = json.load(open(os.path.join(DIR, filename)))
        species = PokemonSpecies.objects.filter(
            name=learnset.get("Name")).first()
        for move in learnset.get("Moves", []):
            try:
                move_model = Move.objects.get(name=move.get("Name"))
                rank_val = ranks[move.get("Learned")]
                MoveSet.objects.update_or_create(species=species, move=move_model, defaults={
                    "learned": rank_val
                })
            except Move.DoesNotExist:
                print(f"{species} moveset: {move.get('Name')} does not exist.")
            except Exception as e:
                print(f"Importing moveset for {species.name} raised: {e}")


def import_evolutions():
    print("\nImporting evolutions ...")
    DIR = os.path.join(settings.BASE_DIR, 'static/Version20/Pokedex')

    for filename in os.listdir(DIR):
        species = json.load(open(os.path.join(DIR, filename)))
        sp_model = PokemonSpecies.objects.filter(
            dex_id=species.get("DexID")).first()
        for evo in species.get("Evolutions", []):
            if from_sp := evo.get("From", None):
                try:
                    Evolution.objects.update_or_create(
                        from_species=PokemonSpecies.objects.get(name=from_sp), to_species=sp_model, defaults={
                            "kind": evo.get("Kind", ""),
                            "speed": evo.get("Speed", "")
                        })
                except PokemonSpecies.DoesNotExist:
                    print(f"{from_sp} not found.")
                except Exception as e:
                    print(f"Evolution {from_sp} -> {species.get('Name')}: {e}")


def import_pokedexes():
    print("\nImporting pokédexes ...")
    # National
    national, _ = Pokedex.objects.get_or_create(name="National Dex")

    for spec in PokemonSpecies.objects.iterator():
        PokedexEntry.objects.update_or_create(species=spec, pokedex=national, defaults={
            "number": spec.number
        })

    # Kanto
    kanto, _ = Pokedex.objects.get_or_create(name="Kanto Dex")

    for id in range(1, 152):
        id_string = str(id).zfill(4)
        species = PokemonSpecies.objects.get(dex_id=id_string)
        PokedexEntry.objects.update_or_create(species=species, pokedex=kanto, defaults={
            "number": id
        })


class Command(BaseCommand):
    help = "Imports all pokémon species, abilities, moves, natures, items, movesets, evolution trees, and pokédexes from the Pokérole database."

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("--only", nargs="+", type=str)

    def handle(self, *args, only=[], **options):
        if not only or "abilities" in only:
            import_abilities()
        if not only or "moves" in only:
            import_moves()
        if not only or "natures" in only:
            import_natures()
        if not only or "species" in only:
            import_species()
        if not only or "items" in only:
            import_items()
        if not only or "movesets" in only:
            import_movesets()
        if not only or "evolutions" in only:
            import_evolutions()
        if not only or "pokedexes" in only:
            import_pokedexes()
        print("\nImport finished!")
