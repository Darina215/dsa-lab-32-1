from flask import Flask, render_template, request
import requests

app = Flask(__name__)

CURRENCY_MANAGER = "http://localhost:5001"
DATA_MANAGER = "http://localhost:5002"


@app.route("/")
def index():
    return render_template("gateway.html", message="")


@app.route("/add", methods=["POST"])
def add():
    data = request.form.to_dict()
    r = requests.post(f"{CURRENCY_MANAGER}/load", json=data)

    msg = "Валюта добавлена" if r.status_code == 200 else r.text
    return render_template("gateway.html", message=msg)


@app.route("/update", methods=["POST"])
def update():
    data = request.form.to_dict()
    r = requests.post(f"{CURRENCY_MANAGER}/update_currency", json=data)

    msg = "Курс обновлён" if r.status_code == 200 else r.text
    return render_template("gateway.html", message=msg)


@app.route("/delete", methods=["POST"])
def delete():
    data = request.form.to_dict()
    r = requests.post(f"{CURRENCY_MANAGER}/delete", json=data)

    msg = "Валюта удалена" if r.status_code == 200 else r.text
    return render_template("gateway.html", message=msg)


@app.route("/convert", methods=["GET"])
def convert():
    r = requests.get(f"{DATA_MANAGER}/convert", params=request.args)

    if r.status_code == 200:
        d = r.json()
        msg = f"{d['amount']} → {d['converted']} ({d['currency']})"
    else:
        msg = "Ошибка конвертации"

    return render_template("gateway.html", message=msg)


@app.route("/list")
def list_currencies():
    r = requests.get(f"{DATA_MANAGER}/currencies")

    if r.status_code == 200:
        data = r.json()
        msg = "<br>".join([f"{c['currency_name']}: {c['rate']}" for c in data])
    else:
        msg = "Ошибка получения списка"

    return render_template("gateway.html", message=msg)


if __name__ == "__main__":
    app.run(port=5000)