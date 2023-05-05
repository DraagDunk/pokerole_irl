from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    slug = models.SlugField(blank=True)

    # avatar = models.ImageField(default='default.jpg', upload_to='profile_images')
    # Will be added later
    bio = models.TextField()

    def __str__(self):
        return self.user.username

    def save(self, **kwargs):
        self.slug = slugify(self.user.username)
        super().save(**kwargs)
