from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect, HttpResponseNotAllowed, HttpResponse
from django.urls import reverse, reverse_lazy
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q, F
from django.db.models import Prefetch

from .models import *
from .form import *

PAGIN_PAGE_NUM = 5

# NOTE: search use GET, this is a function-based view
def search(request):
    filters = {}
    form = {}
    or_filter = Q()
    sort = None

    ingred_filters = Q()
    ingred_exclude = {}

    #recipe = Recipe.objects.all()
    recipe = Recipe.objects.annotate(total_time=F('cook_time')+F('prep_time'))

    if request.method == 'GET':
        # create a form instance and populate it with data from the request:
        form = SearchForm(request.GET)

        if form.is_valid():
            search = form.cleaned_data['search']
            recipe_name = form.cleaned_data['recipe_name']
            categorie = form.cleaned_data['categorie']
            categorieII = form.cleaned_data['categorieII']
            created_after = form.cleaned_data['created_after']
            created_before = form.cleaned_data['created_before']
            time_lte = form.cleaned_data['time_lte']
            ingredients = form.cleaned_data['ingredients']
            exclude_ingred = form.cleaned_data['exclude_ingred']
            sort = form.cleaned_data['sort']
            sort_reverse = form.cleaned_data['sort_reverse']

            # TODO: this is general search, need to be designed carefully
            if search:
                search_split = search.split()
                #or_filter = Q(name__icontains='') | Q(categorie__icontains='') | Q(categorieII__icontains='') | Q(ingred__name__icontains='')
                for i in search_split:
                    or_filter = or_filter | Q(name__icontains=i) | Q(categorie__icontains=i) | Q(categorieII__icontains=i) | Q(ingred__name__icontains=i)
                recipe = recipe.filter(or_filter).distinct()

            if recipe_name:
                filters['name__icontains'] = recipe_name

            if categorie:
                filters['categorie__in'] = categorie

            if categorieII:
                filters['categorieII__in'] = categorieII

            if created_after:
                filters['pub_date__date__gte'] = created_after

            if created_before:
                filters['pub_date__date__lte'] = created_before

            if time_lte:
                filters['total_time__lte'] = time_lte

            if ingredients:
                ingred_split = ingredients.split()
                for i in ingred_split:
                    ingred_filters = ingred_filters | Q(ingred__name__icontains=i)
                recipe = recipe.filter(ingred_filters).distinct()

            if exclude_ingred:
                exclude_split = exclude_ingred.split()
                for i in exclude_split:
                    ingred_exclude['ingred__name__icontains'] = i
                recipe = recipe.exclude(**ingred_exclude).distinct()

    else:
        return HttpResponseNotAllowed(['GET'])


    if sort:
        if sort == 'vw':
            sort_order = ['status__total_viewing'] if sort_reverse else ['-status__total_viewing']
        elif sort == 'rt':
            sort_order = ['status__total_rating'] if sort_reverse else ['-status__total_rating']
        elif sort == 'up':
            sort_order = ['pub_date'] if sort_reverse else ['-pub_date']
        elif sort == 'ab':
            sort_order = ['name'] if sort_reverse else ['-name']
        elif sort == 'tt':
            sort_order = ['total_time'] if sort_reverse else ['-total_time']
    else:
        sort_order = ['pub_date']

    if not filters and not or_filter and not ingred_filters and not ingred_exclude:
        recipes = []
        num_results = 0
    else:
        recipes = recipe.filter(**filters).order_by(*sort_order).select_related('status')[:3000]
        num_results = recipes.count()

    page = request.GET.get('p')
    paginator = Paginator(recipes, PAGIN_PAGE_NUM)  # Show 50 items per page

    try:
        recipe_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        recipe_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        recipe_list = paginator.page(paginator.num_pages)
    # NOTE: write the custom template function

    return render(request, "recipe/result.html", {'recipe_list': recipe_list, 'form': form, 'num_results': num_results})
