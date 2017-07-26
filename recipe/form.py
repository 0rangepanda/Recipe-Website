from django import forms
from django.forms import formset_factory, inlineformset_factory
from django.forms import ModelForm
from django.forms.formsets import BaseFormSet

from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )

class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        exclude = ['ingredients_usage','user']

class RecipeUpdateForm(RecipeForm):
    class Meta:
        model = Recipe
        exclude = ['ingredients_usage','user']

class IngredientForm(ModelForm):
    class Meta:
        model = Ingred_usage
        fields = '__all__'

RecipeFormSet = inlineformset_factory(Recipe, Ingred_usage,
    form=RecipeForm, extra=5, can_delete=True, can_order=False)

RecipeUpdateFormSet = inlineformset_factory(Recipe, Ingred_usage,
    form=RecipeUpdateForm, extra=5, can_delete=True, can_order=False)

class SearchForm(forms.Form):
    SORT_CHOICE = (
        ('vw', 'View'),
        ('rt', 'Rate'),
        ('up', 'Update'),
        ('ab', 'Alphabet'),
        ('tt', 'Total Time'),
    )

    search = forms.CharField(label='Search', required=False, strip=True, help_text='General Search')

    recipe_name = forms.CharField(label='Recipe Name', required=False, strip=True, help_text='Recipe Name')
    #categorie = forms.ChoiceField(label='Category I', choices=Recipe.CATE_TYPE, required=False)
    categorie   = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, label='Category', choices=Recipe.CATE_TYPE, required=False)
    categorieII = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, label='Category II', choices=Recipe.CATE_TYPEII, required=False)

    time_lte = forms.IntegerField(label='Cook Time Less Than', required=False, help_text='Cook time less than', min_value = 0)

    created_after = forms.DateField(label='Created after', required=False, help_text="Find recipes created after this date.")
    created_before = forms.DateField(label='Created before', required=False, help_text="Find recipes created before this date.")

    ingredients = forms.CharField(label='Include Ingredients', required=False, strip=True, help_text='Recipes use these Ingredient')
    exclude_ingred = forms.CharField(label='Exclude Ingredients', required=False, strip=True, help_text='Recipes dont use these Ingredient')

    sort = forms.ChoiceField(label='Sort by', choices=SORT_CHOICE, required=False, help_text='Choose an alternative way to sort')
    sort_reverse = forms.BooleanField(label='Reverse Order', required=False)
