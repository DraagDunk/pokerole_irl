from django.db import models

from .species_models import PokemonSpecies

class Pokedex(models.Model):
    name = models.CharField(max_length=255)
    species = models.ManyToManyField(PokemonSpecies, through='PokedexEntry')

    def __str__(self):
        return self.name


class PokedexEntry(models.Model):
    species = models.ForeignKey(
        PokemonSpecies, on_delete=models.CASCADE, related_name="entries")
    pokedex = models.ForeignKey(Pokedex, on_delete=models.CASCADE)
    number = models.IntegerField()

    RARITIES = models.TextChoices(
        "Rarities", "Legendary Very_rare Rare Uncommon Common")
    rarity = models.CharField(
        max_length=30, choices=RARITIES.choices, null=True, blank=True)

    def __str__(self):
        return f"{self.pokedex} #{self.number}: {self.species}"