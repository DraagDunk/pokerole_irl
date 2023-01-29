from django.contrib import admin

from .models import Pokedex, PokedexEntry, PokemonSpecies, Type, Move, Ability, Nature, Item, Evolution, MoveSet, Profile


@admin.register(Move)
class MoveAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'move_type', 'damage_type')


@admin.register(Ability)
class AbilityAdmin(admin.ModelAdmin):
    list_display = ('__str__',)


@admin.register(PokemonSpecies)
class SpeciesAdmin(admin.ModelAdmin):
    list_display = ('__str__',)

    filter_horizontal = ('abilities',)

    class MoveSetInline(admin.TabularInline):
        model = MoveSet
        extra = 0

    class EvolutionInline(admin.TabularInline):
        model = Evolution
        fk_name = "from_species"
        extra = 0

    class PreEvolutionInline(admin.TabularInline):
        model = Evolution
        fk_name = "to_species"
        extra = 0

    inlines = [MoveSetInline, EvolutionInline, PreEvolutionInline]


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

    class EntryInline(admin.TabularInline):
        model = PokedexEntry
        extra = 0

    inlines = [EntryInline]


@admin.register(Nature)
class NatureAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'confidence', 'keywords')


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'species', 'suggested_price', 'PMD_price')


@admin.register(Evolution)
class EvolutionAdmin(admin.ModelAdmin):
    list_display = ('from_species', 'to_species', 'kind', 'speed')


@admin.register(MoveSet)
class MoveSetAdmin(admin.ModelAdmin):
    list_display = ('move', 'species', 'learned')
    
admin.site.register(Profile)
