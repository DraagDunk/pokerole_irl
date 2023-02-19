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
    creator = models.OneToOneField(User, on_delete=models.CASCADE)
    members = models.ManyToManyField(User, related_name='+')
    name = models.CharField(max_length=30)
    description = models.TextField(max_length=1000, default="")


    def __str__(self):
        return self.name

class Character(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    setting = models.ForeignKey(Setting, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    description = models.TextField(max_length=1000, default="")


    def __str__(self):
        return self.name

