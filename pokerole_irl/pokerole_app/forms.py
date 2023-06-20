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
                  "vitality", "special", "insight", "moves")

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
