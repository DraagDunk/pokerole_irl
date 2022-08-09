from django.contrib import admin

from .models import PokemonSpecies


@admin.register(PokemonSpecies)
class SpeciesAdmin(admin.ModelAdmin):
    list_display = ('__str__',)

    filter_horizontal = ('evolutions',)
