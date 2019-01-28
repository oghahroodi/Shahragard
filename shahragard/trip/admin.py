from django.contrib import admin
from .models import Trip, RequestTrip, Comment

admin.site.register(Trip)
admin.site.register(RequestTrip)
admin.site.register(Comment)
