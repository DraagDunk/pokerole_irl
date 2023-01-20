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

    description = models.TextField(max_length=1000, default="")

    def __str__(self):
        return self.name


class DamageTypeChoices(models.TextChoices):
    PHYSICAL = "Physical", "Physical"
    SPECIAL = "Special", "Special"
    SUPPORT = "Support", "Support"


class TargetChoices(models.TextChoices):
    USER = "User"
    ONE_ALLY = "One Ally"
    ALL_ALLIES = "User & All Allies in Range"
    FOE = "Foe"
    RANDOM_FOE = "Random Foe"
    ALL_FOES = "All Foes in Range"
    AREA = "Area"
    BATTLEFIELD = "Battlefield"


class Move(models.Model):

    name = models.CharField(max_length=50)

    move_type = models.ForeignKey(Type, related_name="moves",
                                  on_delete=models.PROTECT, null=True, blank=True)

    power = models.IntegerField(null=True, blank=True)

    damage_stat = models.CharField(max_length=30, null=True, blank=True)

    damage_modifier = models.CharField(max_length=30, null=True, blank=True)

    primary_accuracy = models.CharField(max_length=30, null=True, blank=True)

    secondary_accuracy = models.CharField(max_length=30, null=True, blank=True)

    description = models.TextField(
        max_length=1000, default="", null=True, blank=True)

    effect = models.TextField(max_length=1000, null=True, blank=True)

    attributes = models.JSONField(default=dict)

    added_effects = models.JSONField(default=dict)

    damage_type = models.CharField(
        max_length=8, choices=DamageTypeChoices.choices, null=True, blank=True)

    target = models.CharField(
        max_length=30, choices=TargetChoices.choices, null=True, blank=True)

    def __str__(self):
        return self.name


class PokemonSpecies(models.Model):

    number = models.PositiveIntegerField()
    dex_id = models.CharField(max_length=6)
    name = models.CharField(max_length=30)
    primary_type = models.ForeignKey(
        Type, related_name="primary_species", null=True, blank=True, on_delete=models.PROTECT)
    secondary_type = models.ForeignKey(
        Type, related_name="secondary_species", null=True, blank=True, on_delete=models.SET_NULL)

    abilities = models.ManyToManyField(
        Ability, related_name="species")
    hidden_ability = models.ForeignKey(
        Ability, related_name="hidden_species", blank=True, null=True, on_delete=models.SET_NULL)
    event_ability = models.ForeignKey(
        Ability, related_name="event_species", blank=True, null=True, on_delete=models.SET_NULL)

    recommended_rank = models.CharField(max_length=30, default="")

    gender_type = models.CharField(max_length=1, default="")

    legendary = models.BooleanField(default=False)

    good_starter = models.BooleanField(default=False)

    height = models.FloatField(verbose_name="height (m)")
    weight = models.FloatField(verbose_name="weight (kg)")

    category = models.CharField(max_length=50, default="")
    description = models.TextField()

    evolutions = models.ManyToManyField(
        'self', related_name="preevolution", through="Evolution", through_fields=("from_species", "to_species"), blank=True, symmetrical=False)

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

    moves = models.ManyToManyField(
        Move, related_name="species", blank=True, through="MoveSet")

    image_name = models.CharField(max_length=50)

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
        return self.name

    def __repr__(self):
        return self.name


class Evolution(models.Model):
    from_species = models.ForeignKey(PokemonSpecies, on_delete=models.CASCADE)
    to_species = models.ForeignKey(
        PokemonSpecies, related_name='evolved_from', on_delete=models.CASCADE)
    kind = models.CharField(max_length=30, default="")
    speed = models.CharField(max_length=30, default="")


class MoveSet(models.Model):
    species = models.ForeignKey(PokemonSpecies, on_delete=models.CASCADE)
    move = models.ForeignKey(Move, on_delete=models.CASCADE)
    learned = models.CharField(max_length=30)


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
        PokemonSpecies, blank=True, null=True, on_delete=models.CASCADE)
    heal_amount = models.CharField(max_length=30, default="")
    suggested_price = models.CharField(max_length=30, default="")
    PMD_price = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return self.name
