from django.urls import path
from . import views

urlpatterns = [
    path('apiv1/search/', views.SearchTrips.as_view()),
]
