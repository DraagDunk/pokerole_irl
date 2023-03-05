from django.contrib import admin
from .models import Setting, Character, WorldMember

# Register your models here.
@admin.register(Setting)
class SettingAdmin(admin.ModelAdmin):
    list_display = ('name',)

    class EntryInline(admin.TabularInline):
        model = WorldMember
        extra = 0
    
    inlines = (EntryInline, )

@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'owner')

@admin.register(WorldMember)
class WorldMemberAdmin(admin.ModelAdmin):
    list_display = ('user', 'setting', 'role')