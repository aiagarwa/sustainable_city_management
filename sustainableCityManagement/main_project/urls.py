from django.urls import path
from django.conf.urls import url
from . import views_wiki
from . import views_trial

urlpatterns = [
    url(r'^wiki$', views_wiki.wiki_trial, name ='img wiki'),
    url(r'^trial$', views_trial.helloworld, name ='trial'),
]
