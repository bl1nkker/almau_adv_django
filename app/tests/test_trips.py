from typing import List, Optional

from django.http import HttpResponseRedirect  # type: ignore
from django.test import TestCase, Client

from app.models import Car, Trip  # type: ignore

def cars_number(cars: List, model: str, speed: int, color: str) -> int:
    quantity = 0
    for car in cars:
        if car.model == model and car.speed == speed and car.color == color:
            quantity += 1
    return quantity

def get_car(cars: List, model: str, speed: int, color: str) -> Optional[Car]:
    for car in cars:
        if car.model == model and car.speed == speed and car.color == color:
            return car
    return None

def get_trip(trips: List, date: str, km: int) -> Optional[Trip]:
    for trip in trips:
        if str(trip.date) == date and trip.km == km:
            return trip
    return None

def compare_cars(car_one, car_two) -> bool:
    return car_one['model'] == car_two.model and car_one["speed"] == car_two.speed and car_one["color"] == car_two.color

def compare_trips(trip_dict, trip_obj) -> bool:
    return str(trip_dict['trip_date']) == str(trip_obj.date) and trip_dict['trip_km'] == trip_obj.km

def trips_number(trips: List, car_id: int) -> int:
    quantity = 0
    for trip in trips:
        if trip.car.id == car_id:
            quantity += 1
    return quantity

class TestTrips(TestCase):
    def test_add_trip(self):

        # Create car
        c = Client()
        response = c.get("/")
        assert "cars" in response.context
        number_of_cars = len(response.context["cars"])
        response = c.post("/add_car/", {
            "model": "Porsche",
            "speed": 340,
            "color": "red",
        })
        assert isinstance(response, HttpResponseRedirect)
        assert response.url == "/"
        cars_response = c.get("/")
        assert "cars" in cars_response.context
        self.assertEquals(len(cars_response.context["cars"]), number_of_cars + 1)
        assert 'button onclick="delete_car' in cars_response.content.decode("UTF8")
        assert cars_number(
            cars=cars_response.context["cars"],
            model="Porsche",
            speed=340,
            color="red",
        ) == 1
        # Get car id
        car = get_car(cars=cars_response.context["cars"],
            model="Porsche",
            speed=340,
            color="red")
        assert car.id is not None
        # Context validation
        response = c.get(f"/cars/{car.id}/trips")
        assert "trips" in response.context
        assert "car" in response.context

        # Create trip
        response = c.post(f"/cars/{car.id}/trips", {
            "trip_km": 100,
            "trip_date": "2020-01-01",
        })
        assert isinstance(response, HttpResponseRedirect)

        # Context validation
        response = c.get(f"/cars/{car.id}/trips")
        assert "trips" in response.context
        assert "car" in response.context

        # Check trip
        assert trips_number(trips=response.context["trips"], car_id=car.id) == 1

        cars_response = c.get("/")
        car = get_car(cars=cars_response.context["cars"],
            model="Porsche",
            speed=340,
            color="red")
        assert car.total_trip_km() == 100

    def test_delete_trip(self):
        # Create car
        c = Client()
        response = c.get("/")
        assert "cars" in response.context
        number_of_cars = len(response.context["cars"])
        response = c.post("/add_car/", {
            "model": "Porsche",
            "speed": 340,
            "color": "red",
        })
        assert isinstance(response, HttpResponseRedirect)
        assert response.url == "/"

        cars_response = c.get("/")
        assert "cars" in cars_response.context
        self.assertEquals(len(cars_response.context["cars"]), number_of_cars + 1)
        assert 'button onclick="delete_car' in cars_response.content.decode("UTF8")
        assert cars_number(
            cars=cars_response.context["cars"],
            model="Porsche",
            speed=340,
            color="red",
        ) == 1
        # Get car 
        car = get_car(cars=cars_response.context["cars"],
            model="Porsche",
            speed=340,
            color="red")
        assert car.id is not None

        # Context validation
        response = c.get(f"/cars/{car.id}/trips")
        assert "trips" in response.context
        assert "car" in response.context

        # Create trip
        response = c.post(f"/cars/{car.id}/trips", {
            "trip_km": 100,
            "trip_date": "2020-01-01",
        })
        assert isinstance(response, HttpResponseRedirect)

        # Context validation
        response = c.get(f"/cars/{car.id}/trips")
        assert "trips" in response.context
        assert "car" in response.context
        # Check trip
        assert trips_number(trips=response.context["trips"], car_id=car.id) == 1

        # Get trip
        trip = get_trip(trips=response.context["trips"], date="2020-01-01", km=100)
        assert trip.id is not None

        # Delete trip
        response = c.delete(f'/delete_trip/{trip.id}')

        # Context validation
        response = c.get(f"/cars/{car.id}/trips")
        assert trips_number(trips=response.context["trips"], car_id=car.id) == 0

    def test_edit_trip(self):
        # Create car
        c = Client()
        response = c.get("/")
        assert "cars" in response.context
        number_of_cars = len(response.context["cars"])
        response = c.post("/add_car/", {
            "model": "Porsche",
            "speed": 340,
            "color": "red",
        })
        assert isinstance(response, HttpResponseRedirect)
        assert response.url == "/"

        cars_response = c.get("/")
        assert "cars" in cars_response.context
        self.assertEquals(len(cars_response.context["cars"]), number_of_cars + 1)
        assert 'button onclick="delete_car' in cars_response.content.decode("UTF8")
        assert cars_number(
            cars=cars_response.context["cars"],
            model="Porsche",
            speed=340,
            color="red",
        ) == 1
        # Get car 
        car = get_car(cars=cars_response.context["cars"],
            model="Porsche",
            speed=340,
            color="red")
        assert car.id is not None

        # Context validation
        response = c.get(f"/cars/{car.id}/trips")
        assert "trips" in response.context
        assert "car" in response.context

        # Create trip
        response = c.post(f"/cars/{car.id}/trips", {
            "trip_km": 100,
            "trip_date": "2020-01-01",
        })
        assert isinstance(response, HttpResponseRedirect)

        # Context validation
        response = c.get(f"/cars/{car.id}/trips")
        assert "trips" in response.context
        assert "car" in response.context
        # Check trip
        assert trips_number(trips=response.context["trips"], car_id=car.id) == 1

        # Get trip
        trip = get_trip(trips=response.context["trips"], date="2020-01-01", km=100)
        assert trip.id is not None

        updated_trip = {
            "id_": trip.id,
            "trip_km": 123,
            "trip_date": "2020-01-02",
        }
        c.post(f"/cars/{car.id}/trips", updated_trip)

        response = c.get(f"/cars/{car.id}/trips")
        assert compare_trips(trip_dict=updated_trip, trip_obj=response.context["trips"][0]) == False