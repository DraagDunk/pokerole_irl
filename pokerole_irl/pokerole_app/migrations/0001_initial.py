# Generated by Django 3.2.16 on 2023-01-20 21:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ability',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=50)),
                ('effect', models.TextField(default='', max_length=1000)),
                ('description', models.TextField(default='', max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='Evolution',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kind', models.CharField(default='', max_length=30)),
                ('speed', models.CharField(default='', max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Move',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('power', models.IntegerField(blank=True, null=True)),
                ('damage_stat', models.CharField(blank=True, max_length=30, null=True)),
                ('damage_modifier', models.CharField(blank=True, max_length=30, null=True)),
                ('primary_accuracy', models.CharField(blank=True, max_length=30, null=True)),
                ('secondary_accuracy', models.CharField(blank=True, max_length=30, null=True)),
                ('description', models.TextField(blank=True, default='', max_length=1000, null=True)),
                ('effect', models.TextField(blank=True, max_length=1000, null=True)),
                ('attributes', models.JSONField(default=dict)),
                ('added_effects', models.JSONField(default=dict)),
                ('damage_type', models.CharField(blank=True, choices=[('Physical', 'Physical'), ('Special', 'Special'), ('Support', 'Support')], max_length=8, null=True)),
                ('target', models.CharField(blank=True, choices=[('User', 'User'), ('One Ally', 'One Ally'), ('User & All Allies in Range', 'All Allies'), ('Foe', 'Foe'), ('Random Foe', 'Random Foe'), ('All Foes in Range', 'All Foes'), ('Area', 'Area'), ('Battlefield', 'Battlefield')], max_length=30, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='MoveSet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('learned', models.CharField(max_length=30)),
                ('move', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pokerole_app.move')),
            ],
        ),
        migrations.CreateModel(
            name='Nature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('confidence', models.PositiveIntegerField()),
                ('keywords', models.CharField(default='', max_length=50)),
                ('description', models.TextField(default='', max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='Pokedex',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('immunities', models.ManyToManyField(blank=True, related_name='no_effect', to='pokerole_app.Type')),
                ('resistances', models.ManyToManyField(blank=True, related_name='not_effective', to='pokerole_app.Type')),
                ('weaknesses', models.ManyToManyField(blank=True, related_name='super_effective', to='pokerole_app.Type')),
            ],
        ),
        migrations.CreateModel(
            name='PokemonSpecies',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.PositiveIntegerField()),
                ('dex_id', models.CharField(max_length=6)),
                ('name', models.CharField(max_length=30)),
                ('recommended_rank', models.CharField(default='', max_length=30)),
                ('gender_type', models.CharField(default='', max_length=1)),
                ('legendary', models.BooleanField(default=False)),
                ('good_starter', models.BooleanField(default=False)),
                ('height', models.FloatField(verbose_name='height (m)')),
                ('weight', models.FloatField(verbose_name='weight (kg)')),
                ('category', models.CharField(default='', max_length=50)),
                ('description', models.TextField()),
                ('base_strength', models.PositiveIntegerField()),
                ('base_dexterity', models.PositiveIntegerField()),
                ('base_vitality', models.PositiveIntegerField()),
                ('base_special', models.PositiveIntegerField()),
                ('base_insight', models.PositiveIntegerField()),
                ('base_hp', models.PositiveIntegerField(verbose_name='base hit points')),
                ('max_strength', models.PositiveIntegerField()),
                ('max_dexterity', models.PositiveIntegerField()),
                ('max_vitality', models.PositiveIntegerField()),
                ('max_special', models.PositiveIntegerField()),
                ('max_insight', models.PositiveIntegerField()),
                ('image_name', models.CharField(max_length=50)),
                ('abilities', models.ManyToManyField(related_name='species', to='pokerole_app.Ability')),
                ('event_ability', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='event_species', to='pokerole_app.ability')),
                ('evolutions', models.ManyToManyField(blank=True, related_name='preevolution', through='pokerole_app.Evolution', to='pokerole_app.PokemonSpecies')),
                ('hidden_ability', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='hidden_species', to='pokerole_app.ability')),
                ('moves', models.ManyToManyField(blank=True, related_name='species', through='pokerole_app.MoveSet', to='pokerole_app.Move')),
                ('primary_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='primary_species', to='pokerole_app.type')),
                ('secondary_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='secondary_species', to='pokerole_app.type')),
            ],
        ),
        migrations.CreateModel(
            name='PokedexEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField()),
                ('rarity', models.CharField(blank=True, choices=[('Legendary', 'Legendary'), ('Very_rare', 'Very Rare'), ('Rare', 'Rare'), ('Uncommon', 'Uncommon'), ('Common', 'Common')], max_length=30, null=True)),
                ('pokedex', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pokerole_app.pokedex')),
                ('species', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='entries', to='pokerole_app.pokemonspecies')),
            ],
        ),
        migrations.AddField(
            model_name='pokedex',
            name='species',
            field=models.ManyToManyField(through='pokerole_app.PokedexEntry', to='pokerole_app.PokemonSpecies'),
        ),
        migrations.AddField(
            model_name='moveset',
            name='species',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pokerole_app.pokemonspecies'),
        ),
        migrations.AddField(
            model_name='move',
            name='move_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='moves', to='pokerole_app.type'),
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('description', models.TextField(default='', max_length=1000)),
                ('value', models.CharField(default='', max_length=50)),
                ('heal_amount', models.CharField(default='', max_length=30)),
                ('suggested_price', models.CharField(default='', max_length=30)),
                ('PMD_price', models.PositiveIntegerField(blank=True, null=True)),
                ('species', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pokerole_app.pokemonspecies')),
                ('type_bonus', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='pokerole_app.type')),
            ],
        ),
        migrations.AddField(
            model_name='evolution',
            name='from_species',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pokerole_app.pokemonspecies'),
        ),
        migrations.AddField(
            model_name='evolution',
            name='to_species',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='evolved_from', to='pokerole_app.pokemonspecies'),
        ),
    ]
