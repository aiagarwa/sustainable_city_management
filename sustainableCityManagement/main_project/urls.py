from django.urls import path
from django.conf.urls import url
from .Bike_API import views_bike_api

# Building URL endpoints for API calls.
urlpatterns = [
    url(r'^bikestands_details/$', views_bike_api.show_bike_data, name ='bikestand_info'),
    url(r'^bikestands_graph/$', views_bike_api.graph_bike_data, name ='bikestand_info_graph'),
]
