from django.db import models


class Type(models.Model):
    name = models.CharField(max_length=30)
    resistances = models.ManyToManyField(
        'self', related_name="not_effective", symmetrical=False, blank=True)
    weaknesses = models.ManyToManyField(
        'self', related_name="super_effective", symmetrical=False, blank=True)
    immunities = models.ManyToManyField(
        'self', related_name="no_effect", symmetrical=False, blank=True)

    def __str__(self):
        return self.name


class Ability(models.Model):
    pass


class Move(models.Model):
    pass


class PokemonSpecies(models.Model):

    name = models.CharField(max_length=30)
    variant = models.CharField(max_length=30, null=True, blank=True)
    types = models.ManyToManyField(Type, related_name="species", blank=True)
    abilities = models.ManyToManyField(
        Ability, related_name="species", blank=True)

    height = models.FloatField(verbose_name="height (m)")
    weight = models.FloatField(verbose_name="weight (kg)")

    description = models.TextField()

    evolves_by = models.CharField(max_length=30, null=True, blank=True)

    evolutions = models.ManyToManyField(
        'self', related_name="preevolution", blank=True, symmetrical=False)

    # Base stats
    base_strength = models.PositiveIntegerField()
    base_dexterity = models.PositiveIntegerField()
    base_vitality = models.PositiveIntegerField()
    base_special = models.PositiveIntegerField()
    base_insight = models.PositiveIntegerField()

    base_hp = models.PositiveIntegerField(verbose_name="base hit points")

    # Maximum stats
    max_strength = models.PositiveIntegerField()
    max_dexterity = models.PositiveIntegerField()
    max_vitality = models.PositiveIntegerField()
    max_special = models.PositiveIntegerField()
    max_insight = models.PositiveIntegerField()

    moveset = models.ManyToManyField(Move, related_name="species", blank=True)

    @property
    def weight_lbs(self):
        return 2.2*self.weight

    @property
    def height_ft(self):
        return 3.28*self.height

    def __str__(self):
        return f"{self.variant} {self.name}" if self.variant else f"{self.name}"

    def __repr__(self):
        return f"{self.variant} {self.name}" if self.variant else f"{self.name}"


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
