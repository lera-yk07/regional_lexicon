from django.contrib import admin
from .models import Region, City, Word, Comparison

@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'word_count')
    search_fields = ('name', 'description')
    list_filter = ('created_at',)

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'region', 'population', 'founded_year', 'word_count')
    search_fields = ('name', 'region__name')
    list_filter = ('region',)

@admin.register(Word)
class WordAdmin(admin.ModelAdmin):
    list_display = ('word', 'city', 'user', 'created_at', 'views_count')
    search_fields = ('word', 'meaning', 'city__name')
    list_filter = ('city__region', 'city', 'created_at')

@admin.register(Comparison)
class ComparisonAdmin(admin.ModelAdmin):
    list_display = ('city1', 'city2', 'compared_at', 'common_words_count')
    list_filter = ('compared_at',)