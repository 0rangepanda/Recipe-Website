# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-07-26 15:47
from __future__ import unicode_literals

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(blank=True, default='')),
                ('pub_date', models.DateTimeField(auto_now_add=True, null=True, verbose_name='date added')),
                ('edit_date', models.DateTimeField(auto_now=True, null=True, verbose_name='date last modifed')),
            ],
        ),
        migrations.CreateModel(
            name='Ingred_usage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=128)),
                ('amount', models.FloatField(validators=[django.core.validators.MinValueValidator(0)])),
                ('unit', models.CharField(choices=[('lb', 'pound'), ('oc', 'ounce'), ('dr', 'drop'), ('cp', 'cup'), ('ts', 'teaspoon'), ('pc', 'piece'), ('ph', 'pinch'), ('sl', 'slice'), ('sp', 'spoon')], default='lb', max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='Ingredient_buylink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('link_to_buy', models.CharField(blank=True, max_length=255, null=True)),
                ('unit', models.CharField(choices=[('lb', 'pound'), ('oc', 'ounce'), ('dr', 'drop'), ('cp', 'cup'), ('ts', 'teaspoon'), ('pc', 'piece'), ('ph', 'pinch'), ('sl', 'slice'), ('sp', 'spoon')], default='lb', max_length=2)),
                ('price', models.CharField(blank=True, max_length=2, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usr_name', models.CharField(max_length=128)),
                ('usr_id', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('categorie', models.CharField(choices=[('br', 'Breakfast'), ('lc', 'Lunch'), ('bc', 'Brunch'), ('dn', 'Dinner'), ('sn', 'Snack'), ('ot', 'Other')], default='ot', max_length=2, null=True)),
                ('categorieII', models.CharField(choices=[('sp', 'Soup'), ('md', 'Main Dish'), ('ap', 'Appetizer'), ('fe', 'Fast Eat'), ('ot', 'Other')], default='ot', max_length=2, null=True)),
                ('prep_time', models.IntegerField(blank=True, null=True, verbose_name='Recipe preparation time')),
                ('cook_time', models.IntegerField(blank=True, null=True, verbose_name='Recipe cook time')),
                ('video_link', models.CharField(blank=True, max_length=255, null=True, verbose_name='video link to preparation')),
                ('origin_link', models.CharField(blank=True, max_length=255, null=True, verbose_name='original attribution link')),
                ('complete_image', models.ImageField(blank=True, null=True, upload_to='recipe/', verbose_name='photo of completed recipe')),
                ('logo', models.ImageField(blank=True, null=True, upload_to='recipe/', verbose_name='logo of originating publication')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='date added')),
                ('edit_date', models.DateTimeField(auto_now=True, verbose_name='date last modifed')),
                ('direction', models.TextField(blank=True, default='')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipe.MyUser')),
            ],
        ),
        migrations.CreateModel(
            name='RecipeStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_viewing', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('total_rating', models.DecimalField(decimal_places=2, default=0.0, max_digits=3, validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(1)])),
                ('recipe', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='status', to='recipe.Recipe')),
            ],
        ),
        migrations.AddField(
            model_name='ingred_usage',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingred', to='recipe.Recipe'),
        ),
        migrations.AddField(
            model_name='comment',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='recipe.Recipe'),
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL),
        ),
    ]