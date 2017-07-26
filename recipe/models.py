from __future__ import unicode_literals

import datetime

from django.db import models
from django.utils import timezone
from django.db.models import Count

from django.core.validators import MaxValueValidator, MinValueValidator

from django.contrib.auth.models import User


# Create your models here.

MAX_LENGTH = 2048
NAME_MAX_LENGTH = 128
LINK_MAX_LENGTH = 255

# NOTE: ingredients unit
UNIT_TYPE = (
    ('lb', 'pound'),
    ('oc', 'ounce'),
    ('dr', 'drop'),
    ('cp', 'cup'),
    ('ts', 'teaspoon'),
    ('pc', 'piece'),
    ('ph', 'pinch'),
    ('sl', 'slice'),
    ('sp', 'spoon'),
)# NOTE: ALL are US unit, should use a function to convert to Metric
 # And the list is not completed yet
 # Can user add new unit type?


class User_Content(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='content')



class Ingredient_buylink(models.Model):
    # NOTE: to store all our buylinks of ingredients
    # when user create an ingredients_usage, query from here

    name = models.CharField(max_length=NAME_MAX_LENGTH)
    link_to_buy = models.CharField(max_length=LINK_MAX_LENGTH, blank=True, null=True)
    unit = models.CharField(max_length=2, choices=UNIT_TYPE, default='lb')
    price = models.CharField(max_length=2, blank=True, null=True)

    def __str__(self):              # __unicode__ on Python 2
        return self.name


class Recipe(models.Model):
    name = models.CharField(max_length=NAME_MAX_LENGTH)
    #ingredients_usage = models.ManyToManyField(Ingredient, through = "Ingred_usage")

    CATE_TYPE = (
        ('br', 'Breakfast'),
        ('lc', 'Lunch'),
        ('bc', 'Brunch'),
        ('dn', 'Dinner'),
        ('sn', 'Snack'),
        ('ot', 'Other'),
    )
    categorie = models.CharField(max_length=2, choices=CATE_TYPE, blank=False, null=True, default='ot')

    CATE_TYPEII = (
        ('sp', 'Soup'),
        ('md', 'Main Dish'),
        ('ap', 'Appetizer'),
        ('fe', 'Fast Eat'),
        ('ot', 'Other'),
    )
    categorieII = models.CharField(max_length=2, choices=CATE_TYPEII, blank=False, null=True, default='ot')

    prep_time = models.IntegerField("Recipe preparation time", blank=True, null=True)
    cook_time = models.IntegerField("Recipe cook time", blank=True, null=True)
    video_link = models.CharField("video link to preparation", max_length=LINK_MAX_LENGTH, blank=True, null=True)
    origin_link = models.CharField("original attribution link", max_length=LINK_MAX_LENGTH, blank=True, null=True)

    complete_image = models.ImageField("photo of completed recipe", upload_to = 'recipe/', blank=True, null=True)
    logo = models.ImageField("logo of originating publication", upload_to = 'recipe/', blank=True, null=True) # upload_to = ?

    pub_date = models.DateTimeField("date added", auto_now_add=True)
    edit_date = models.DateTimeField("date last modifed", auto_now=True)
    # NOTE: auto_now_add -> First created time
    #       auto_now     -> Last modified time

    direction = models.TextField(blank = True, default = '') # one big HTML

    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='recipe')# one user can have many recipes

    def __str__(self):              # __unicode__ on Python 2
        return self.name

class RecipeStatus(models.Model):
    recipe = models.OneToOneField(Recipe, on_delete=models.CASCADE, related_name='status')
    total_viewing = models.IntegerField(default=0,
        validators=[MinValueValidator(0), ])
    total_rating = models.DecimalField(default=0.0, max_digits=3, decimal_places=2,
        validators=[MaxValueValidator(5), MinValueValidator(1)])

class Ingred_usage(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='ingred')
    name = models.CharField(max_length=NAME_MAX_LENGTH, default = '')
    amount = models.FloatField(validators = [MinValueValidator(0), ])
    unit = models.CharField(max_length=2, choices=UNIT_TYPE, default='lb')

class Comment(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField(blank = True, default = '')
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name='comments')
    pub_date = models.DateTimeField("date added", auto_now_add=True, null=True)
    edit_date = models.DateTimeField("date last modifed", auto_now=True, null=True)
    #rating = models.IntegerField(default=1,
    #    validators=[MaxValueValidator(5), MinValueValidator(1)])
