from django.contrib import admin

from .models import Profile, Setting

admin.site.register(Profile)

@admin.register(Setting)
class SettingAdmin(admin.ModelAdmin):
    list_display = ('name',)

