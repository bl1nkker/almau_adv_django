from django.contrib import admin  # type: ignore
from django.http import HttpRequest, HttpResponse  # type: ignore
from django.urls import path  # type: ignore
from app.views import (
    index,
    delete,
    add_car,
    car_trips,
    submit_trip,
    delete_trip
)

urlpatterns = [
    path('', index),
    path('delete/<str:id_>', delete),
    path('add_car/', add_car),
    path('cars/<int:id_>', car_trips),
    path('submit_trip/', submit_trip),
    path('delete_trip/<str:id_>', delete_trip),

    path('admin777/', admin.site.urls),
]
