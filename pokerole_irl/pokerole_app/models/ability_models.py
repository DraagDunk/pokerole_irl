from django.db import models

class Ability(models.Model):

    name = models.CharField(max_length=50, default="")

    effect = models.TextField(max_length=1000, default="")

    description = models.TextField(max_length=1000, default="")

    def __str__(self):
        return self.name