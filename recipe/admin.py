# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import *
#from .user import *

# Register your models here.

class IngredusageInline(admin.TabularInline): # NOTE: take less space
    model = Ingred_usage
    extra = 3

class CommentsInline(admin.TabularInline): # NOTE: take less space
    model = Comment
    extra = 3

class RecipeStatusInline(admin.StackedInline): # NOTE: take less space
    model = RecipeStatus

class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'pub_date', 'user')
    list_filter = ['pub_date']
    search_fields = ['name']
    inlines = [IngredusageInline, RecipeStatusInline, CommentsInline]
    fieldsets = [
        (None,                    {'fields': ['name']}),
        ('Categorie information', {'fields': ['categorie', 'categorieII']}),
        ('Recipe information',    {'fields': ['prep_time','cook_time','video_link',
            'origin_link','complete_image','logo','user']}),
        ('Direction',             {'fields': ['direction']}),
    ]



admin.site.register(User_Content)
admin.site.register(Ingredient_buylink)
admin.site.register(Recipe, RecipeAdmin)

#admin.site.register(User)
admin.site.register(Comment)
