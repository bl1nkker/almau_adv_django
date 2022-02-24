from django.http import HttpRequest, HttpResponse  # type: ignore
from django.shortcuts import render, redirect  # type: ignore
from django.contrib.auth.models import User  # type: ignore

from app.models import Car, Trip

car_id_to_edit = ''


def index(request: HttpRequest) -> HttpResponse:
    catalog = Car.objects.all()
    return render(request, "index.html", context={
        "cars": catalog
    })

def delete(request: HttpRequest, id_: str) -> HttpResponse:
    global cars
    Car.objects.get(id=id_).delete()
    return HttpResponse("", status=204)

def add_car(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        if request.POST.get("id_", "") == "":
            Car.objects.create(
                model=request.POST.get("model", ""),
                speed=int(request.POST.get("speed", "")),
                color=request.POST.get("color", ""),
            )
        else:
            car = Car.objects.get(pk=int(request.POST.get("id_", "")))
            car.model = request.POST.get("model", "")
            car.speed = int(request.POST.get("speed", ""))
            car.color = request.POST.get("color", "")
            car.save()
    return redirect("/")


def car_trips(request: HttpRequest, id_: int) -> HttpResponse:
    selected_car = Car.objects.get(id=id_)
    trips = Trip.objects.filter(car=selected_car)
    return render(request, "trips.html", context={
        "trips": trips,
        "selected_car": selected_car
    })

def submit_trip(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        if request.POST.get("id_", "") == "":
            Trip.objects.create(
                car=Car.objects.get(id=request.POST.get("car_id", "")),
                date=request.POST.get("date", ""),
                km=int(request.POST.get("km", "")),
            )
        else:
            trip = Trip.objects.get(pk=int(request.POST.get("id_", "")))
            trip.date = request.POST.get("date", "")
            trip.km = int(request.POST.get("km", ""))
            trip.save()
    return redirect("/")
def delete_trip(request: HttpRequest, id_: str) -> HttpResponse:
    Trip.objects.get(id=id_).delete()
    return HttpResponse("", status=204)
# TODO: homework: Implement trips CRUD
# TODO: class: pagination for trips
# TODO: class: filtering for trips by date
# TODO: class: search cars
