import math
from time import localtime
from datetime import datetime

from configs import total_space, free_time_secs, price_first_hour, price_next_hours
from db import db_connection, fetch_number_of_cars, check_car, add_car, take_car, provide_payment, provide_parking_time


def available_space():
    cursor_object = db_connection()
    number_of_cars = fetch_number_of_cars(cursor_object)
    return total_space - number_of_cars


def enter(car_number):
    cursor_object = db_connection()
    car_exists = check_car(cursor_object, car_number)
    if not car_exists:
        nice_time = localtime()
        timestamp = datetime.now()
        money_paid = 0
        add_car(cursor_object, car_number, timestamp, money_paid)
        return f"Car with registration number {car_number} entered parking at {nice_time.tm_hour}:{nice_time.tm_min}"
    else:
        pass


def parking_time(car_number):
    cursor_object = db_connection()
    enter_time = take_car(cursor_object, car_number)[5]
    current_timestamp = datetime.now().timestamp()

    parking_time_seconds = current_timestamp - enter_time.timestamp()
    parking_time_hours = parking_time_seconds / 3600

    return parking_time_seconds, parking_time_hours


def money_due(car_number):
    cursor_object = db_connection()
    car_exists = check_car(cursor_object, car_number)
    if car_exists:
        parking_time_seconds, parking_time_hours = parking_time(car_number)
        money_paid = take_car(cursor_object, car_number)[2]

        if parking_time_seconds <= free_time_secs:
            # If parking time is within free time
            return 0

        elif parking_time_seconds <= 3600:
            # Charge for the first hour
            return price_first_hour - int(money_paid)

        else:
            # Charge for next hours
            return price_first_hour + ((math.ceil(parking_time_hours) - 1) * price_next_hours) - int(money_paid)
    else:
        pass


def payment(car_number, amount):
    cursor_object = db_connection()
    car_exists = check_car(cursor_object, car_number)
    if car_exists:
        money_due_payment = money_due(car_number)
        if int(money_due_payment) - int(amount) <= 0:
            provide_payment(cursor_object, car_number, amount)
            return "You can leave our parking now - thanks for visiting!"
        else:
            provide_payment(cursor_object, car_number, amount)
            return "You need to pay all your charges before leaving parking"
    else:
        return "There is no such a car on our parking"


def exiting(car_number):
    cursor_object = db_connection()
    car_exists = check_car(cursor_object, car_number)
    if car_exists:
        # For edge case when car is entering the parking and immediately leaving, without checking the moneyDue
        able_to_leave = payment(car_number, 0)
        if able_to_leave == "You can leave our parking now - thanks for visiting!":
            parking_time_hours = math.ceil(parking_time(car_number)[1])
            provide_parking_time(cursor_object, car_number, parking_time_hours)
            return "OPEN"
        else:
            return "CLOSE"
    else:
        return "There is no such a car on our parking"
