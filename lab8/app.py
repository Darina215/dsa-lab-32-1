from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import json
import os

app = Flask(__name__)

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["100 per day"]
)


DATA_FILE = "data.json"

data = {}


def load_data():
    global data

    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)
        except:
            data = {}
    else:
        data = {}


def save_data():
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


load_data()


@app.route('/set', methods=['POST'])
@limiter.limit("10 per minute")
def set_value():
    body = request.get_json()

    if not body:
        return jsonify({"error": "JSON не передан"}), 400

    key = body.get("key")
    value = body.get("value")

    if key is None or value is None:
        return jsonify({"error": "Необходимо указать key и value"}), 400

    data[key] = value
    save_data()

    return jsonify({
        "message": "Значение сохранено",
        "key": key,
        "value": value
    })


@app.route('/get/<key>', methods=['GET'])
def get_value(key):

    if key in data:
        return jsonify({
            "key": key,
            "value": data[key]
        })

    return jsonify({
        "error": "Ключ не найден"
    }), 404


@app.route('/delete/<key>', methods=['DELETE'])
@limiter.limit("10 per minute")
def delete_value(key):

    if key in data:
        del data[key]
        save_data()

        return jsonify({
            "message": "Ключ удален"
        })

    return jsonify({
        "error": "Ключ не найден"
    }), 404


@app.route('/exists/<key>', methods=['GET'])
def exists(key):

    return jsonify({
        "exists": key in data
    })


if __name__ == '__main__':
    app.run(debug=True)