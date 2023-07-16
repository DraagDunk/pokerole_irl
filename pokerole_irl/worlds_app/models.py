from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse


# Create your models here.
class World(models.Model):
    members = models.ManyToManyField(User, through='WorldMember')
    name = models.CharField(max_length=100)
    description = models.TextField(default="")
    world_slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.world_slug:
            self.world_slug = self.world_slug or slugify(self.name)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('world', kwargs={"world_slug": self.world_slug})


class Character(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    world = models.ForeignKey(World, blank=True, null=True, on_delete=models.SET_NULL)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    description = models.TextField(default="")
    character_slug = models.SlugField(unique=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        if not self.character_slug:
            self.character_slug = self.character_slug or slugify(self.first_name)
        return super().save(*args, **kwargs)


class WorldMember(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    world = models.ForeignKey(World, on_delete=models.CASCADE)
    ROLES = models.TextChoices(
        "ROLE", "Owner Member")
    role = models.CharField(
        max_length=30, choices=ROLES.choices, default="Member")

    def __str__(self):
        return f"{self.user}"
