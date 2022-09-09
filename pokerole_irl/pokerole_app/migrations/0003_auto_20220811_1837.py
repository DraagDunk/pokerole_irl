# Generated by Django 3.2.15 on 2022-08-11 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pokerole_app', '0002_auto_20220811_1641'),
    ]

    operations = [
        migrations.AddField(
            model_name='type',
            name='name',
            field=models.CharField(default='none', max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='type',
            name='resistances',
            field=models.ManyToManyField(related_name='not_effective', to='pokerole_app.Type'),
        ),
        migrations.AddField(
            model_name='type',
            name='weaknesses',
            field=models.ManyToManyField(related_name='super_effective', to='pokerole_app.Type'),
        ),
    ]
