from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register((TeamPlayer))


@admin.register(Sport)
class SportAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'team', 'status']

@admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):
    list_display = ['id', 'match', 'inning', 'status', 'win_loss', 'total_score', 'over', 'current_over']

@admin.register(ScoreAdd)
class ScoreAddAdmin(admin.ModelAdmin):
    list_display = ['id', 'score', 'ball', 'run', 'comment']