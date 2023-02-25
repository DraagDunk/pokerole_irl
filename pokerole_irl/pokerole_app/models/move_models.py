from django.db import models
from django.urls import reverse_lazy

from .base_models import Type


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

    def get_absolute_url(self):
        return reverse_lazy("move", kwargs={"pk": self.pk})
