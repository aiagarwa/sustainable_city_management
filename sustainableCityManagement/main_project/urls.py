from django.urls import path
from django.conf.urls import url
from . import views_wiki
from . import views_trial
from .Bike_API import views_bikeAPI

urlpatterns = [
    url(r'^wiki/$', views_wiki.wiki_trial, name ='img wiki'),
    url(r'^trial/$', views_trial.helloworld, name ='trial'),
    url(r'^bikestands_details/$', views_bikeAPI.suggestBikeRelocate, name ='bikestand_info'),
    # url(r'^historical_bikestands_details/$', views_bikeAPI.suggestBikeRelocate, name ='fetch_bikestand_historical'),
]
