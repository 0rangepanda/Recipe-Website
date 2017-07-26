from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.urls import reverse

# Create your views here.

def index(request):
    template = loader.get_template('index.html') #within ./template
    context = {}
    return HttpResponse(template.render(context, request))
