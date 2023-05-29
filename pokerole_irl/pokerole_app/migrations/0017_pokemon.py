# Generated by Django 3.2.19 on 2023-05-29 20:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('worlds_app', '0003_alter_world_options'),
        ('pokerole_app', '0016_auto_20230529_1939'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pokemon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nickname', models.CharField(blank=True, max_length=100, null=True)),
                ('happiness', models.PositiveIntegerField(default=1)),
                ('loyalty', models.PositiveIntegerField(default=1)),
                ('current_hp', models.PositiveIntegerField(blank=True, default=0)),
                ('current_will', models.PositiveIntegerField(blank=True, default=0)),
                ('battle_count', models.PositiveIntegerField(default=0)),
                ('victory_count', models.PositiveIntegerField(default=0)),
                ('strength', models.PositiveIntegerField(default=0)),
                ('dexterity', models.PositiveIntegerField(default=0)),
                ('vitality', models.PositiveIntegerField(default=0)),
                ('special', models.PositiveIntegerField(default=0)),
                ('insight', models.PositiveIntegerField(default=0)),
                ('tough', models.PositiveIntegerField(default=0)),
                ('cool', models.PositiveIntegerField(default=0)),
                ('beauty', models.PositiveIntegerField(default=0)),
                ('cute', models.PositiveIntegerField(default=0)),
                ('clever', models.PositiveIntegerField(default=0)),
                ('brawl', models.PositiveIntegerField(default=0)),
                ('channel', models.PositiveIntegerField(default=0)),
                ('clash', models.PositiveIntegerField(default=0)),
                ('evasion', models.PositiveIntegerField(default=0)),
                ('alert', models.PositiveIntegerField(default=0)),
                ('athletic', models.PositiveIntegerField(default=0)),
                ('nature', models.PositiveIntegerField(default=0)),
                ('stealth', models.PositiveIntegerField(default=0)),
                ('allure', models.PositiveIntegerField(default=0)),
                ('etiquette', models.PositiveIntegerField(default=0)),
                ('intimidate', models.PositiveIntegerField(default=0)),
                ('perform', models.PositiveIntegerField(default=0)),
                ('rank', models.PositiveIntegerField(choices=[(0, 'Starter'), (1, 'Beginner'), (2, 'Amateur'), (3, 'Ace'), (4, 'Pro'), (5, 'Master'), (6, 'Champion')], default=0)),
                ('held_item', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='pokerole_app.item')),
                ('moves', models.ManyToManyField(blank=True, to='pokerole_app.Move')),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('pokemon_nature', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='pokerole_app.nature')),
                ('species', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pokerole_app.pokemonspecies')),
                ('trainer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='owned_pokemon', to='worlds_app.character')),
            ],
        ),
    ]
