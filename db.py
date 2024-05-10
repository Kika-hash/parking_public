import psycopg2
from configs import db_configs


def db_connection():
    db_conn = psycopg2.connect(db_configs)
    cursor_object = db_conn.cursor()
    return cursor_object


def fetch_number_of_cars(cursor_object):
    cursor_object.execute("SELECT COUNT(*) FROM parking_data")
    result = cursor_object.fetchone()
    # Extract the count from the result tuple
    number_of_cars = result[0]
    return number_of_cars


def check_car(cursor_object, car_number):
    cursor_object.execute("SELECT * FROM parking_data WHERE carNumber = %s;", (car_number,))
    car_exists = cursor_object.fetchone()

    if car_exists is not None:
        return True
    else:
        return False


def add_car(cursor_object, car_number, enter_time, money_paid):
    cursor_object.execute(
        "INSERT INTO parking_data (carNumber, canGo, enterTime, moneyPaid) VALUES (%s, %s, %s, %s)",
        (car_number, False, enter_time, money_paid,)
    )
    cursor_object.connection.commit()


def take_car(cursor_object, car_number):
    cursor_object.execute("SELECT * FROM parking_data WHERE carNumber = %s;", (car_number,))
    car_data = cursor_object.fetchone()
    return car_data


def provide_payment(cursor_object, car_number, amount):
    car_data = take_car(cursor_object, car_number)
    car_data_already_paid = car_data[2]
    new_amount = + int(car_data_already_paid) + int(amount)
    cursor_object.execute("UPDATE parking_data SET moneypaid = %s WHERE carNumber = %s;", (new_amount, car_number,))
    cursor_object.connection.commit()


def provide_parking_time(cursor_object, car_number, parking_time):
    cursor_object.execute("UPDATE parking_data SET parkingtime = %s WHERE carNumber = %s;", (parking_time, car_number,))
    cursor_object.connection.commit()

