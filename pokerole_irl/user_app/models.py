from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # avatar = models.ImageField(default='default.jpg', upload_to='profile_images')
    # Will be added later
    bio = models.TextField()

    def __str__(self):
        return self.user.username


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

