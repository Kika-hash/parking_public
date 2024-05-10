from flask import Flask, render_template, request
from back_end import enter, available_space, money_due, payment, exiting

app = Flask(__name__, static_folder="static")


@app.route("/")
def main_page():
    return render_template("main.html")


@app.route("/enter", methods=["GET", "POST"])
def provide_car():
    if request.method == "POST":
        number = request.form["carNumber"]
        response = enter(number)
        return render_template("main.html", result_message=response)
    if request.method == "GET":
        space = available_space()
        return render_template("enter.html", available_space=space)


@app.route("/check", methods=["GET", "POST"])
def check_amount():
    if request.method == "POST":
        car_number = request.form["carNumberCheck"]
        to_be_paid = money_due(car_number)
        return render_template("check.html", moneyToPay=to_be_paid)
    if request.method == "GET":
        return render_template("check.html")


@app.route("/pay", methods=["GET", "POST"])
def pay():
    if request.method == "POST":
        registration_number_payment = request.form["carNumberPay"]
        amount_payment = request.form["paymentAmount"]
        result = payment(registration_number_payment, amount_payment)
        return render_template("pay.html", result_message=result)
    if request.method == "GET":
        return render_template("pay.html")


@app.route("/leave", methods=["GET", "POST"])
def leave():
    if request.method == "POST":
        car_number = request.form["carNumberLeave"]
        result = exiting(car_number)
        return render_template("leave.html", goNoGo=result)
    if request.method == "GET":
        return render_template("leave.html")


if __name__ == '__main__':
    app.run(debug=True)
