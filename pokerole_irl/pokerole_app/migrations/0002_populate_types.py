from django.db import migrations


def create_types(apps, _):
    Type = apps.get_model('pokerole_app', 'Type')
    types = ('normal', 'bug', 'dark', 'dragon', 'electric', 'fairy', 'fighting', 'fire', 'flying',
             'ghost', 'grass', 'ground', 'ice', 'poison', 'psychic', 'rock', 'steel', 'water')
    for type in types:
        Type.objects.update_or_create(name=type.capitalize())


def add_weaknesses(apps, _):
    Type = apps.get_model('pokerole_app', 'Type')
    weaknesses = {
        'normal': ('fighting',),
        'bug': ('fire', 'flying', 'rock'),
        'dark': ('bug', 'fairy', 'fighting'),
        'dragon': ('dragon', 'fairy', 'ice'),
        'electric': ('ground',),
        'fairy': ('poison', 'steel'),
        'fighting': ('fairy', 'flying', 'psychic'),
        'fire': ('ground', 'rock', 'water'),
        'flying': ('electric', 'ice', 'rock'),
        'ghost': ('dark', 'ghost'),
        'grass': ('bug', 'fire', 'flying', 'ice', 'poison'),
        'ground': ('grass', 'ice', 'water'),
        'ice': ('fighting', 'fire', 'rock', 'steel'),
        'poison': ('ground', 'psychic'),
        'psychic': ('bug', 'dark', 'ghost'),
        'rock': ('grass', 'ground', 'fighting', 'steel', 'water'),
        'steel': ('fighting', 'fire', 'ground'),
        'water': ('electric', 'grass')
    }
    for key in weaknesses:
        type = Type.objects.get(name=key.capitalize())
        for weakness in weaknesses[key]:
            weakness_object = Type.objects.get(name=weakness.capitalize())
            type.weaknesses.add(weakness_object)


def add_resistances(apps, _):
    Type = apps.get_model('pokerole_app', 'Type')
    resistances = {
        'bug': ('fighting', 'grass', 'ground'),
        'dark': ('dark', 'ghost'),
        'dragon': ('electric', 'fire', 'grass', 'water'),
        'electric': ('electric', 'flying', 'steel'),
        'fairy': ('bug', 'dark', 'fighting'),
        'fighting': ('bug', 'dark', 'rock'),
        'fire': ('bug', 'fairy', 'fire', 'grass', 'ice', 'steel'),
        'flying': ('bug', 'fighting', 'grass'),
        'ghost': ('bug', 'poison'),
        'grass': ('electric', 'grass', 'ground', 'water'),
        'ground': ('poison', 'rock'),
        'ice': ('ice',),
        'poison': ('bug', 'fairy', 'fighting', 'grass', 'poison'),
        'psychic': ('fighting', 'psychic'),
        'rock': ('fire', 'flying', 'normal', 'poison'),
        'steel': ('bug', 'dragon', 'flying', 'fairy', 'grass', 'ice', 'normal', 'psychic', 'rock', 'steel'),
        'water': ('fire', 'ice', 'steel', 'water')
    }
    for key in resistances:
        type = Type.objects.get(name=key.capitalize())
        for resistance in resistances[key]:
            resistance_object = Type.objects.get(name=resistance.capitalize())
            type.resistances.add(resistance_object)


def add_immunities(apps, _):
    Type = apps.get_model('pokerole_app', 'Type')
    immunities = {
        'normal': ('ghost',),
        'dark': ('psychic',),
        'fairy': ('dragon',),
        'flying': ('ground',),
        'ghost': ('fighting', 'normal'),
        'ground': ('electric',),
        'steel': ('poison',)
    }
    for key in immunities:
        type = Type.objects.get(name=key.capitalize())
        for immunity in immunities[key]:
            immunity_object = Type.objects.get(name=immunity.capitalize())
            type.immunities.add(immunity_object)


class Migration(migrations.Migration):
    dependencies = [
        ('pokerole_app', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(
            create_types, reverse_code=migrations.RunPython.noop),
        migrations.RunPython(
            add_weaknesses, reverse_code=migrations.RunPython.noop),
        migrations.RunPython(
            add_resistances, reverse_code=migrations.RunPython.noop),
        migrations.RunPython(
            add_immunities, reverse_code=migrations.RunPython.noop)
    ]
