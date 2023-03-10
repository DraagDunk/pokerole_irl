from django.db import models


class Type(models.Model):
    name = models.CharField(max_length=30)
    resistances = models.ManyToManyField(
        'self', related_name="not_effective", symmetrical=False, blank=True)
    weaknesses = models.ManyToManyField(
        'self', related_name="super_effective", symmetrical=False, blank=True)
    immunities = models.ManyToManyField(
        'self', related_name="no_effect", symmetrical=False, blank=True)

    def get_weaknesses_and_resistances(self):
        weak_res = {}
        for weakness in self.weaknesses.all():
            weak_res[weakness] = 2
        for resistance in self.resistances.all():
            weak_res[resistance] = 0.5
        for immunity in self.immunities.all():
            weak_res[immunity] = 0
        return weak_res

    def get_effectiveness(self):
        mods = {}
        for se in self.super_effective.all():
            mods[se] = 2
        for nve in self.not_effective.all():
            mods[nve] = 0.5
        for ne in self.no_effect.all():
            mods[ne] = 0
        return mods

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()


class Nature(models.Model):
    name = models.CharField(max_length=30)
    confidence = models.PositiveIntegerField()
    keywords = models.CharField(max_length=50, default="")
    description = models.TextField(max_length=1000, default="")

    def __str__(self):
        return self.name


class Item(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(max_length=1000, default="")
    type_bonus = models.ForeignKey(
        Type, blank=True, null=True, on_delete=models.SET_NULL)
    value = models.CharField(max_length=50, default="")
    species = models.ForeignKey(
        "PokemonSpecies", blank=True, null=True, on_delete=models.CASCADE)
    heal_amount = models.CharField(max_length=30, default="")
    suggested_price = models.CharField(max_length=30, default="")
    PMD_price = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return self.name
