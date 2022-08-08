from django.db import models


class Type(models.Model):
    pass


class Ability(models.Model):
    pass


class Move(models.Model):
    pass


class PokemonSpecies(models.Model):

    name = models.TextField()
    types = models.ManyToManyField(Type, related_name="species")
    abilities = models.ManyToManyField(Ability, related_name="species")

    height = models.FloatField(verbose_name="height (m)")
    weight = models.FloatField(verbose_name="weight (kg)")

    description = models.TextField()

    evolves_by = models.TextField()

    evolutions = models.ManyToManyField(related_name="preevolution")

    # Base stats
    base_strength = models.IntegerField()
    base_dexterity = models.IntegerField()
    base_vitality = models.IntegerField()
    base_special = models.IntegerField()
    base_insight = models.IntegerField()

    base_hp = models.IntegerField(verbose_name="base hit points")

    # Maximum stats
    max_strength = models.IntegerField()
    max_dexterity = models.IntegerField()
    max_vitality = models.IntegerField()
    max_special = models.IntegerField()
    max_insight = models.IntegerField()

    moveset = models.ManyToManyField(Move, related_name="species")

    @property
    def weight_lbs(self):
        return 2.2*self.weight

    @property
    def height_ft(self):
        return 3.28*self.height
