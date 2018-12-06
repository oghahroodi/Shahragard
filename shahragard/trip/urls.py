from django.urls import path
from . import views

urlpatterns = [
    path('apiv1/trip/', views.TripHandler.as_view()),
]