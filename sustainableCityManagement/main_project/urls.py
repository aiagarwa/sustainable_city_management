from django.urls import path
from django.conf.urls import url
from . import views_wiki
from . import views_trial
from .Bike_API import views_bikeAPI

urlpatterns = [
    url(r'^wiki$', views_wiki.wiki_trial, name ='img wiki'),
    url(r'^trial$', views_trial.helloworld, name ='trial'),
    url(r'^fetch_bikeAPI$', views_bikeAPI.bike_details, name ='fetch_bikeAPI'),
]
