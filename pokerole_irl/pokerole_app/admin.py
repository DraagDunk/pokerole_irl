from django.contrib import admin

from .models import Pokedex, PokedexEntry, PokemonSpecies, Type, Move, Ability, Nature, Item, Evolution


@admin.register(Move)
class MoveAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'move_type', 'damage_type')


@admin.register(Ability)
class AbilityAdmin(admin.ModelAdmin):
    list_display = ('__str__',)


@admin.register(PokemonSpecies)
class SpeciesAdmin(admin.ModelAdmin):
    list_display = ('__str__',)

    filter_horizontal = ('evolutions', 'moves', 'abilities')


@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display = ('__str__',)

    filter_horizontal = ('weaknesses', 'resistances', 'immunities')


@admin.register(PokedexEntry)
class PokedexEntryAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'pokedex', 'species', 'number')


@admin.register(Pokedex)
class PokedexAdmin(admin.ModelAdmin):
    list_display = ('__str__',)


@admin.register(Nature)
class NatureAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'confidence', 'keywords')


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'species', 'suggested_price', 'PMD_price')


@admin.register(Evolution)
class EvolutionAdmin(admin.ModelAdmin):
    list_display = ('from_species', 'to_species', 'kind', 'speed')
