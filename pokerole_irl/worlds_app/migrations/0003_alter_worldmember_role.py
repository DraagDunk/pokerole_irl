# Generated by Django 3.2.16 on 2023-03-05 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('worlds_app', '0002_rename_members_worldmember_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='worldmember',
            name='role',
            field=models.CharField(choices=[('Owner', 'Owner'), ('Member', 'Member')], default='Member', max_length=30),
        ),
    ]
