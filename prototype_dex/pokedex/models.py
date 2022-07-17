from django.db import models


class Pokedex(models.Model):
    name = models.CharField(max_length=255)
    primarytype = models.CharField(max_length=255)
    secondarytype = models.CharField(max_length=255)
