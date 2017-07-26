from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect, HttpResponseNotAllowed, HttpResponse
from django.urls import reverse, reverse_lazy
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.db.models import Count

from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.edit import FormView
from django.views import View

from django.utils import timezone

from django import forms
from django.forms import formset_factory

from django.db.models import Prefetch

#For login
from django.contrib.auth.decorators import login_required #function-based view
from django.contrib.auth.mixins import LoginRequiredMixin #class-based view

from .models import *
from .form import *
from .search import *
from .user import *



class IndexView(ListView):
    # NOTE: display a list of objects
    template_name = 'recipe/index.html'
    context_object_name = 'latest_recipe_list'

    def get_queryset(self):
        """
        Return the last five published recipes
        """
        return Recipe.objects.all().order_by('-pub_date')[:20]


class RecipeDetailView(DetailView):

    model = Recipe
    template_name = 'recipe/detail.html'

    def get_context_data(self, **kwargs):# NOTE: override get_context_data to add more info
        context = super(RecipeDetailView, self).get_context_data(**kwargs)
        print kwargs
        context['now'] = timezone.now()
        context['ingredients'] = Ingred_usage.objects.filter(recipe=context['object'])
        context['comments'] = Comment.objects.filter(recipe=context['object']).order_by('edit_date')
        #context['status'] = RecipeStatus.objects.filter(recipe=context['object'])
        # TODO: Reduce query times, currently 6
        return context





class RecipeCreate(LoginRequiredMixin, CreateView):

    model = Recipe
    form_class = RecipeForm
    template_name = 'recipe/create.html'

    #login_url = '/login/'
    #redirect_field_name = 'redirect_to'

    # On successful form submission
    def get_success_url(self):
        return reverse('recipe:index')

    def get_context_data(self, **kwargs):
        context = super(RecipeCreate, self).get_context_data(**kwargs)
        if self.request.POST:
            context['form'] = RecipeForm(self.request.POST)
            context['inlines'] = RecipeFormSet(self.request.POST)
        else:
            context['form'] = RecipeForm()
            context['inlines'] = RecipeFormSet()
        return context

    # Validate forms
    def form_valid(self, form):
        context = self.get_context_data()
        inlines = context['inlines']

        if inlines.is_valid() and form.is_valid():
            self.object = form.save(commit=False)
    
            if self.request.user:
                self.object.user = self.request.user # NOTE: Not added_by
            self.object.save()

            inlines.instance = self.object
            inlines.save()

            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

class RecipeUpdate(UpdateView):

    model = Recipe
    template_name = 'recipe/update.html'
    form_class = RecipeUpdateForm

    # On successful form submission
    def get_success_url(self):
        return reverse('recipe:index')

    def get_context_data(self, **kwargs):
        context = super(RecipeUpdate, self).get_context_data(**kwargs)

        if self.request.POST.get('delete'):
            obj.delete()
        elif self.request.POST:
            context['form'] = RecipeForm(self.request.POST, instance=self.object)
            context['inlines'] = RecipeFormSet(self.request.POST, instance=self.object)
        else:
            context['form'] = RecipeForm(instance=self.object)
            context['inlines'] = RecipeFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        inlines = context['inlines']

        if inlines.is_valid() and form.is_valid():
            self.object = form.save()

            if self.request.user:
                self.object.added_by = self.request.user
            self.object.save()

            inlines.instance = self.object
            inlines.save()

            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))
    # Save inlineform data

class RecipeDelete(DeleteView):
    model = Recipe
    success_url = reverse_lazy('recipe:index')
