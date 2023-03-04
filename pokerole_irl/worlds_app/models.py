from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Setting(models.Model):
    owner = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    members = models.ManyToManyField(User, related_name='+', blank=True)
    name = models.CharField(max_length=100)
    description = models.TextField(default="")


    def __str__(self):
        return self.name

class Character(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    setting = models.ForeignKey(Setting, blank=True, null=True, on_delete=models.SET_NULL)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    description = models.TextField(default="")


    def __str__(self):
        return self.name