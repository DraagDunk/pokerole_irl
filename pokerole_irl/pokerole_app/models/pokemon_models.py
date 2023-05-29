from django.db import models

from .species_models import PokemonSpecies
from .base_models import Item, Nature, RankChoices
from .move_models import Move
from worlds_app.models import Character


class Pokemon(models.Model):
    species = models.ForeignKey(PokemonSpecies, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=100, null=True, blank=True)
    trainer = models.ForeignKey(
        Character, blank=True, null=True, related_name='owned_pokemon', on_delete=models.SET_NULL)

    nature = models.ForeignKey(Nature, null=True, on_delete=models.SET_NULL)

    happiness = models.PositiveIntegerField(default=1)
    loyalty = models.PositiveIntegerField(default=1)

    current_hp = models.PositiveIntegerField(blank=True, default=0)
    current_will = models.PositiveIntegerField(blank=True, default=0)

    held_item = models.ForeignKey(
        Item, blank=True, null=True, on_delete=models.SET_NULL)
    # Status-model does not exist yet.
    # status = models.ForeinKey(Status, blank=True, null=True)

    battle_count = models.PositiveIntegerField(default=0)
    victory_count = models.PositiveIntegerField(default=0)

    moves = models.ManyToManyField(Move, blank=True)

    # Stats
    strength = models.PositiveIntegerField(default=0)
    dexterity = models.PositiveIntegerField(default=0)
    vitality = models.PositiveIntegerField(default=0)
    special = models.PositiveIntegerField(default=0)
    insight = models.PositiveIntegerField(default=0)

    # Social stats
    tough = models.PositiveIntegerField(default=0)
    cool = models.PositiveIntegerField(default=0)
    beauty = models.PositiveIntegerField(default=0)
    cute = models.PositiveIntegerField(default=0)
    clever = models.PositiveIntegerField(default=0)

    # Skills
    brawl = models.PositiveIntegerField(default=0)
    channel = models.PositiveIntegerField(default=0)
    clash = models.PositiveIntegerField(default=0)
    evasion = models.PositiveIntegerField(default=0)
    alert = models.PositiveIntegerField(default=0)
    athletic = models.PositiveIntegerField(default=0)
    nature = models.PositiveIntegerField(default=0)
    stealth = models.PositiveIntegerField(default=0)
    allure = models.PositiveIntegerField(default=0)
    etiquette = models.PositiveIntegerField(default=0)
    intimidate = models.PositiveIntegerField(default=0)
    perform = models.PositiveIntegerField(default=0)

    rank = models.PositiveIntegerField(default=0, choices=RankChoices.choices)

    def __str__(self):
        if self.trainer:
            return f"{self.trainer}'s {self.species} '{self.nickname or self.species}'"
        else:
            return f"Wild {self.species} '{self.nickname or self.species}'"

    @property
    def hp(self):
        return self.species.base_hp + self.vitality

    @property
    def will(self):
        return self.insight + 2

    @property
    def initiative(self):
        return self.dexterity + self.alert

    @property
    def physical_clash(self):
        return self.strength + self.clash

    @property
    def special_clash(self):
        return self.special + self.clash

    @property
    def evade(self):
        return self.dexterity + self.evasion

    @property
    def defense(self):
        return self.vitality

    @property
    def special_defense(self):
        return self.insight

    @property
    def possible_moves(self):
        return self.species.moves.filter(learned__lte=self.rank).prefetch_related("move")

    def save(self):
        species = self.species
        # Stats
        self.strength = self.constrain_stat(
            self.strength, species.base_strength, species.max_strength)
        self.dexterity = self.constrain_stat(
            self.dexterity, species.base_dexterity, species.max_dexterity)
        self.vitality = self.constrain_stat(
            self.vitality, species.base_vitality, species.max_vitality)
        self.special = self.constrain_stat(
            self.special, species.base_special, species.max_special)
        self.insight = self.constrain_stat(
            self.insight, species.base_insight, species.max_insight)
        # Social stats
        self.tough = self.constrain_stat(self.tough, 1, 5)
        self.cool = self.constrain_stat(self.cool, 1, 5)
        self.beauty = self.constrain_stat(self.beauty, 1, 5)
        self.cute = self.constrain_stat(self.cute, 1, 5)
        self.clever = self.constrain_stat(self.clever, 1, 5)
        # Skills
        self.brawl = self.constrain_stat(self.brawl, 0, 5)
        self.channel = self.constrain_stat(self.channel, 0, 5)
        self.clash = self.constrain_stat(self.clash, 0, 5)
        self.evasion = self.constrain_stat(self.evasion, 0, 5)
        self.alert = self.constrain_stat(self.alert, 0, 5)
        self.athletic = self.constrain_stat(self.athletic, 0, 5)
        self.nature = self.constrain_stat(self.nature, 0, 5)
        self.stealth = self.constrain_stat(self.stealth, 0, 5)
        self.allure = self.constrain_stat(self.allure, 0, 5)
        self.etiquette = self.constrain_stat(self.etiquette, 0, 5)
        self.intimidate = self.constrain_stat(self.intimidate, 0, 5)
        self.perform = self.constrain_stat(self.perform, 0, 5)
        # Other
        self.happiness = self.constrain_stat(self.happiness, 1, 5)
        self.loyalty = self.constrain_stat(self.loyalty, 1, 5)
        self.current_hp = self.constrain_stat(self.current_hp, 0, self.hp)
        self.current_will = self.constrain_stat(
            self.current_will, 0, self.will)
        super().save()

    def constrain_stat(self, stat, base_stat, max_stat):
        return min([max([stat, base_stat]), max_stat])
