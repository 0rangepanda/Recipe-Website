
from django.views.generic import TemplateView

from django.conf.urls import include, url
from django.contrib.auth import views as auth_views

from . import views

app_name = 'recipe'

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^create/', views.RecipeCreate.as_view(), name='create'),
    url(r'^search/$', views.search, name='search-result'),
    #url(r'^test/(?P<pk>[0-9]+)/', views.detail, name='test'),
    url(r'^(?P<pk>[0-9]+)/', views.RecipeDetailView.as_view(), name='detail'),
    url(r'^update/(?P<pk>[0-9]+)/', views.RecipeUpdate.as_view(), name='update'),
    url(r'^delete/(?P<pk>[0-9]+)/', views.RecipeDelete.as_view(), name='delete'),

    #Django User
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^accounts/signup/', views.signup, name='signup'),
]
