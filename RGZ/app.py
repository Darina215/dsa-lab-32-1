from flask import Flask, request, jsonify, render_template, redirect
from flask_sqlalchemy import SQLAlchemy

from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    login_required,
    logout_user,
    current_user
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from datetime import datetime
import requests

from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "finance_login_page"


class User(UserMixin, db.Model):

    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    login = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    password_hash = db.Column(
        db.String(255),
        nullable=False
    )


class Operation(db.Model):

    __tablename__ = "operations"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    date = db.Column(
        db.Date,
        nullable=False
    )

    sum = db.Column(
        db.Numeric(10, 2),
        nullable=False
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id")
    )

    type_operation = db.Column(
        db.String(20),
        nullable=False
    )


class Budget(db.Model):

    __tablename__ = "budget"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    month = db.Column(
        db.String(20),
        nullable=False
    )

    amount = db.Column(
        db.Numeric(10, 2),
        nullable=False
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id")
    )


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


def get_currency_rate(currency):

    if currency == "RUB":
        return 1

    try:

        response = requests.get(
            f"http://127.0.0.1:5001/rate?currency={currency}"
        )

        if response.status_code != 200:
            raise Exception("Currency service error")

        data = response.json()

        if "rate" not in data:
            raise Exception("Rate not found")

        return float(data["rate"])

    except Exception as e:

        print("Currency service error:", e)

        raise Exception("UNEXPECTED ERROR")


@app.route("/")
def home():
    return redirect("/finance_login")


@app.route("/finance_register", methods=["GET"])
def finance_register_page():

    return render_template(
        "finance_register.html"
    )


@app.route("/reg", methods=["POST"])
def register():

    try:
        data = request.get_json()  

        login = data.get("login")  
        password = data.get("password")  

        if not login or not password:
            return jsonify({"message": "Login and password required"}), 400  

        existing_user = User.query.filter_by(login=login).first()  

        if existing_user:
            return jsonify({"message": "User already exists"}), 400  

        password_hash = generate_password_hash(password)  

        user = User(login=login, password_hash=password_hash)  

        db.session.add(user)  
        db.session.commit() 

        return redirect("/finance_login")  

    except Exception as e:
        print(e)  
        return jsonify({"message": "UNEXPECTED ERROR"}), 500  


@app.route("/finance_login", methods=["GET"])
def finance_login_page():

    return render_template(
        "finance_auth.html"
    )


@app.route("/login", methods=["POST"])
def login():

    try:

        login = request.form.get("login")
        password = request.form.get("password")

        user = User.query.filter_by(login=login).first()

        if not user:
            return jsonify({"message": "User not found"}), 404

        if not check_password_hash(user.password_hash, password):
            return jsonify({"message": "Wrong password"}), 401

        login_user(user)

        return redirect("/operations")

    except Exception as e:
        print(e)
        return jsonify({"message": "UNEXPECTED ERROR"}), 500


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/finance_login")


@app.route("/add_operation", methods=["POST"])
@login_required
def add_operation():
    try:
        data = request.get_json()
        
        type_op = data.get("type_operation")
        sum_op = data.get("sum")
        date_op = data.get("date")
        
        if not type_op or not sum_op or not date_op:
            return jsonify({"message": "Missing required fields"}), 400
        
        if type_op not in ["income", "expense"]:
            return jsonify({"message": "Invalid operation type"}), 400
        
        if float(sum_op) <= 0:
            return jsonify({"message": "Sum must be positive"}), 400
        
        operation = Operation(
            type_operation=type_op,
            sum=sum_op,
            date=date_op,
            user_id=current_user.id
        )
        
        db.session.add(operation)
        db.session.commit()
        
        return jsonify({"message": "OK"}), 200
        
    except Exception as e:
        print(e)
        return jsonify({"message": "UNEXPECTED ERROR"}), 500


@app.route("/budget", methods=["GET", "POST"])
@login_required
def budget():

    try:

        if request.method == "GET":
            return render_template("finance_budget.html")

        amount = request.form.get("amount")

        current_month = datetime.now().strftime("%Y-%m")

        existing_budget = Budget.query.filter_by(
            user_id=current_user.id,
            month=current_month
        ).first()

        if existing_budget:

            existing_budget.amount = amount

        else:

            new_budget = Budget(
                month=current_month,
                amount=amount,
                user_id=current_user.id
            )

            db.session.add(new_budget)

        db.session.commit()

        return render_template(
            "finance_budget.html",
            success="Бюджет успешно сохранен"
        )

    except Exception as e:
        print(e)
        return jsonify({ "message": "UNEXPECTED ERROR"}), 500


@app.route("/operations", methods=["GET"])
@login_required
def operations():

    try:

        currency = request.args.get(
            "currency",
            "RUB"
        )

        rate = get_currency_rate(currency)

        operations = Operation.query.filter_by(
            user_id=current_user.id
        ).all()

        current_month = datetime.now().strftime("%Y-%m")

        budget = Budget.query.filter_by(
            user_id=current_user.id,
            month=current_month
        ).first()

        budget_value = None

        if budget:

            budget_value = round(
                float(budget.amount) / rate,
                2
            )

        operations_data = []

        for op in operations:

            converted_sum = round(
                float(op.sum) / rate,
                2
            )

            operations_data.append({
                "date": str(op.date),
                "sum": converted_sum,
                "type": op.type_operation
            })

        return render_template(
            "finance_operations.html",
            operations=operations_data,
            budget=budget_value,
            currency=currency
        )

    except Exception as e:
        print(e)
        return jsonify({"message": "UNEXPECTED ERROR"}), 500


@app.route("/add_operation_page")
@login_required
def add_operation_page():
    return render_template("add_operation.html")


if __name__ == "__main__":

    with app.app_context():
        db.create_all()

    app.run(debug=True)