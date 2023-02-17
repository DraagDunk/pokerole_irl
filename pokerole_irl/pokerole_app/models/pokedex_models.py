from django.db import models
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model

from .species_models import PokemonSpecies


class Pokedex(models.Model):
    name = models.CharField(max_length=255)
    species = models.ManyToManyField(PokemonSpecies, through='PokedexEntry')
    owner = models.ForeignKey(
        get_user_model(), null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse_lazy("pokedex_entries", kwargs={"dex_pk": self.pk})


class PokedexEntry(models.Model):
    species = models.ForeignKey(
        PokemonSpecies, on_delete=models.CASCADE, related_name="entries")
    pokedex = models.ForeignKey(Pokedex, on_delete=models.CASCADE)
    number = models.IntegerField()

    class Rarities(models.TextChoices):
        LEGENDARY = ("legendary", "Legendary")
        VERY_RARE = ("very_rare", "Very Rare")
        RARE = ("rare", "Rare")
        UNCOMMON = ("uncommon", "Uncommon")
        COMMON = ("common", "Common")
    rarity = models.CharField(
        max_length=30, choices=Rarities.choices, null=True, blank=True)

    def __str__(self):
        return f"{self.pokedex} #{self.number}: {self.species}"

    def get_absolute_url(self):
        return reverse_lazy("pokedex_entry", kwargs={"dex_pk": self.pokedex.pk, "pk": self.pk})
