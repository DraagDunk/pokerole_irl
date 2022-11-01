from django.contrib import admin

from .models import Pokedex, PokedexEntry, PokemonSpecies, Type, Move, Ability


@admin.register(Move)
class MoveAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'move_type', 'category')


@admin.register(Ability)
class AbilityAdmin(admin.ModelAdmin):
    list_display = ('__str__',)


@admin.register(PokemonSpecies)
class SpeciesAdmin(admin.ModelAdmin):
    list_display = ('__str__',)

    filter_horizontal = ('evolutions',)


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
