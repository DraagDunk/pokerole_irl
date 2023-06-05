from django.db import models
from django.db.models.constraints import UniqueConstraint
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.urls import reverse_lazy


class World(models.Model):
    members = models.ManyToManyField(User, through='WorldMember')
    name = models.CharField(max_length=100)
    description = models.TextField(default="")
    slug = models.SlugField(blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, **kwargs):
        self.slug = slugify(self.name)
        super().save(**kwargs)

    UniqueConstraint(fields=["name"], name="name_constraint")


class Character(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    world = models.ForeignKey(
        World, blank=True, null=True, on_delete=models.SET_NULL)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    description = models.TextField(default="")
    slug = models.SlugField(blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def save(self, **kwargs):
        self.slug = slugify(str(self))
        super().save(**kwargs)

    def get_absolute_url(self):
        return reverse_lazy("character", kwargs={"world_slug": self.world.slug, "slug": self.slug})

    UniqueConstraint(fields=["world", "first_name",
                     "last_name"], name="name_world_constraint")


class WorldMember(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    world = models.ForeignKey(World, on_delete=models.CASCADE)
    ROLES = models.TextChoices(
        "ROLE", "Owner Member")
    role = models.CharField(
        max_length=30, choices=ROLES.choices, default="Member")

    def __str__(self):
        return f"{self.user}"
