from django.contrib import admin

from .models import Profile, Setting, Character

admin.site.register(Profile)

@admin.register(Setting)
class SettingAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner')

@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'owner')

