from typing import Any
from django.forms import ModelForm, ModelMultipleChoiceField, CheckboxSelectMultiple

from .models.pokemon_models import Pokemon
from .models.move_models import Move
from worlds_app.models import Character


class PokemonCreateForm(ModelForm):
    class Meta:
        model = Pokemon
        fields = ("nickname", "species", "pokemon_nature",
                  "rank", "trainer")

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['trainer'].queryset = Character.objects.filter(owner=user)


class PokemonEditForm(ModelForm):
    class Meta:
        model = Pokemon
        fields = ("nickname", "rank", "strength", "dexterity",
                  "vitality", "special", "insight", "moves",
                  "tough", "cool", "beauty", "cute", "clever",
                  "brawl", "channel", "clash", "evasion",
                  "alert", "athletic", "nature", "stealth",
                  "allure", "etiquette", "intimidate", "perform")

    moves = ModelMultipleChoiceField(
        queryset=Move.objects.all(), widget=CheckboxSelectMultiple)

    def __init__(self, *args, **kwargs):
        if kwargs.get('instance'):
            initial = kwargs.setdefault('initial', {})
            initial['moves'] = [
                move.pk for move in kwargs['instance'].moves.all()]

        super().__init__(*args, **kwargs)
        self.fields['moves'].queryset = Move.objects.filter(
            moveset__species=self.instance.species, moveset__learned__lte=self.instance.rank)

    def _calculate_added_attribute_points(self):
        added_points = 0
        for field in ("strength", "dexterity", "vitality", "special", "insight"):
            added_points += self.cleaned_data[field] - \
                getattr(self.instance.species, "base_" + field)
        return added_points

    def _calculate_added_social_attribute_points(self):
        added_points = 0
        for field in ("tough", "cool", "beauty", "cute", "clever"):
            added_points += self.cleaned_data[field] - 1
        return added_points

    def _calculate_added_skill_points(self):
        added_points = 0
        for field in ("brawl", "channel", "clash", "evasion", "alert", "athletic", "nature", "stealth", "allure", "etiquette", "intimidate", "perform"):
            added_points += self.cleaned_data[field]
        return added_points

    def clean(self) -> dict[str, Any]:
        allowed_points = min(8, int(self.cleaned_data['rank']) * 2)
        added_points = self._calculate_added_attribute_points()
        if added_points > allowed_points:
            for field in ("strength", "dexterity", "vitality", "special", "insight"):
                self.add_error(
                    field, f"You added {added_points}, you are only allowed to add {allowed_points} at this rank!")

        added_social_points = self._calculate_added_social_attribute_points()
        if added_social_points > allowed_points:
            for field in ("tough", "cool", "beauty", "cute", "clever"):
                self.add_error(
                    field, f"You added {added_social_points}, you are only allowed to add {allowed_points} at this rank!")

        added_skill_points = self._calculate_added_skill_points()
        allowed_skill_points = sum(
            [5-rank for rank in range(min(5, self.cleaned_data['rank']+1))])
        if added_skill_points > allowed_skill_points:
            for field in ("brawl", "channel", "clash", "evasion", "alert", "athletic", "nature", "stealth", "allure", "etiquette", "intimidate", "perform"):
                if self.cleaned_data[field] > 0:
                    self.add_error(
                        field, f"You added {added_skill_points}, you are only allowed to add {allowed_skill_points} at this rank!")

        allowed_moves = (self.cleaned_data.get(
            'insight') or self.instance.insight) + 2
        moves = len(self.cleaned_data['moves'])
        if moves > allowed_moves:
            self.add_error(
                'moves', f"You added {moves} moves, but are only allowed {allowed_moves} with this amount of insight.")

    def save(self, commit=True):
        instance = super().save(commit=False)

        old_save_m2m = self.save_m2m

        def save_m2m():
            old_save_m2m()

            instance.moves.clear()
            instance.moves.add(*self.cleaned_data['moves'])
        self.save_m2m = save_m2m

        if commit:
            instance.save()
            self.save_m2m()

        return instance
