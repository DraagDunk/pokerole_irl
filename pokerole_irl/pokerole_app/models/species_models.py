from django.db import models
from django.urls import reverse_lazy

from .base_models import Type, RankChoices
from .ability_models import Ability
from .move_models import Move


class PokemonSpecies(models.Model):

    number = models.PositiveIntegerField()
    dex_id = models.CharField(max_length=20)
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
    def weight_kg(self):
        return f"{self.weight} kg"

    @property
    def weight_lbs(self):
        return f"{round(2.2*self.weight, 1)} lbs"

    @property
    def height_m(self):
        return f"{self.height} m"

    @property
    def height_ft(self):
        feet = round(3.28*self.height, 1)
        return f"{int(feet//1)}\'{int((feet%1)*12)}\""

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
    def types(self):
        typ = str(self.primary_type)
        if self.secondary_type:
            typ += f", {self.secondary_type}"
        return typ

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

    @property
    def is_mega(self):
        return self.name.endswith("Form)") and "(Mega" in self.name

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def book_image(self):
        return f"https://raw.githubusercontent.com/Willowlark/Pokerole-Data/master/images/BookSprites/{self.image_name}"

    def box_image(self):
        return f"https://raw.githubusercontent.com/Willowlark/Pokerole-Data/master/images/BoxSprites/{self.image_name}"

    def get_absolute_url(self):
        return reverse_lazy("species", kwargs={"pk": self.pk})


class Evolution(models.Model):
    from_species = models.ForeignKey(PokemonSpecies, on_delete=models.CASCADE)
    to_species = models.ForeignKey(
        PokemonSpecies, related_name='evolved_from', on_delete=models.CASCADE)
    kind = models.CharField(max_length=30, default="")
    speed = models.CharField(max_length=30, default="")


class MoveSet(models.Model):
    species = models.ForeignKey(PokemonSpecies, on_delete=models.CASCADE)
    move = models.ForeignKey(Move, on_delete=models.CASCADE)
    learned = models.PositiveIntegerField(
        default=0, choices=RankChoices.choices)
