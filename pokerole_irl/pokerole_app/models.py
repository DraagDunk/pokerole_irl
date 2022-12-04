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

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()


class Ability(models.Model):

    name = models.CharField(max_length=50, default="")

    effect = models.TextField(max_length=1000, default="")

    def __str__(self):
        return self.name


class Move(models.Model):

    name = models.CharField(max_length=50)

    description = models.TextField(
        max_length=1000, default="", null=True, blank=True)

    move_type = models.ForeignKey(Type, related_name="moves",
                                  on_delete=models.PROTECT, null=True, blank=True)

    power = models.IntegerField(null=True, blank=True)

    ranged = models.BooleanField(default=False)

    target = models.CharField(max_length=30, null=True, blank=True)

    primary_accuracy = models.CharField(max_length=30, null=True, blank=True)

    secondary_accuracy = models.CharField(max_length=30, null=True, blank=True)

    reduced_accuracy = models.IntegerField(default=0, null=True, blank=True)

    damage_stat = models.CharField(max_length=30, null=True, blank=True)

    damage_modifier = models.IntegerField(null=True, blank=True)

    additional_info = models.TextField(max_length=1000, null=True, blank=True)

    class CategoryChoices(models.TextChoices):
        PHYSICAL = "PH", "Physical"
        SPECIAL = "SP", "Special"
        SUPPORT = "SU", "Support"

    category = models.CharField(
        max_length=2, choices=CategoryChoices.choices, null=True, blank=True)

    class TargetChoices(models.TextChoices):
        USER = "USER", "User"
        ONE_ALLY = "ONE_ALLY", "One Ally"
        ALL_ALLIES = "ALL_ALLIES", "User & All Allies in Range"
        FOE = "FOE", "Foe"
        RANDOM_FOE = "RANDOM_FOE", "Random Foe"
        ALL_FOES = "ALL_FOES", "All Foes in Range"
        AREA = "AREA", "Area"
        BATTLEFIELD = "BATTLEFIELD", "Battlefield"

    def __str__(self):
        return self.name


class PokemonSpecies(models.Model):

    name = models.CharField(max_length=30)
    variant = models.CharField(max_length=30, null=True, blank=True)
    primary_type = models.ForeignKey(
        Type, related_name="primary_species", null=True, blank=True, on_delete=models.PROTECT)
    secondary_type = models.ForeignKey(
        Type, related_name="secondary_species", null=True, blank=True, on_delete=models.SET_NULL)
    abilities = models.ManyToManyField(
        Ability, related_name="species", blank=True)

    height = models.FloatField(verbose_name="height (m)")
    weight = models.FloatField(verbose_name="weight (kg)")

    category = models.CharField(max_length=50, default="")
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

    moveset = models.ManyToManyField(
        Move, related_name="species", blank=True)

    @property
    def weight_lbs(self):
        return round(2.2*self.weight, 1)

    @property
    def height_ft(self):
        return round(3.28*self.height, 1)

    def get_weaknesses_and_resistances(self):
        wr_primary = self.primary_type.get_weaknesses_and_resistances()

        if self.secondary_type:
            wr_secondary = self.secondary_type.get_weaknesses_and_resistances()

            weak_res = wr_primary
            for key, val in wr_secondary.items():
                if key in weak_res.keys():
                    weak_res[key] *= val
                else:
                    weak_res[key] = val
            return weak_res
        else:
            return wr_primary

    @property
    def weaknesses(self):
        weak_list = []
        for key, val in self.get_weaknesses_and_resistances().items():
            if val > 1:
                weak_list.append(f"{key} x{val}")
        return ", ".join(weak_list)

    @property
    def resistances(self):
        res_list = []
        for key, val in self.get_weaknesses_and_resistances().items():
            if val < 1:
                res_list.append(f"{key} x{val}")
        return ", ".join(res_list)

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
