from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse_lazy

# Create your models here.
class World(models.Model):
    members = models.ManyToManyField(User, through='WorldMember')
    name = models.CharField(max_length=100)
    description = models.TextField(default="")


    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse_lazy("world", kwargs={"pk": self.pk})

class Character(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    world = models.ForeignKey(World, blank=True, null=True, on_delete=models.SET_NULL)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    description = models.TextField(default="")


    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    
class WorldMember(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    world = models.ForeignKey(World, on_delete=models.CASCADE)
    ROLES = models.TextChoices(
        "ROLE", "Owner Member")
    role = models.CharField(
        max_length=30, choices=ROLES.choices, default="Member")
    
    def __str__(self):
        return f"{self.user}"