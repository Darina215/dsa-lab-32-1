from flask import Flask, request, jsonify
from db import get_connection

app = Flask(__name__)

@app.route("/load", methods=["POST"])
def load_currency():
    data = request.json
    name = data["currency_name"]
    rate = data["rate"]

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM currencies WHERE currency_name=%s", (name,))
    if cur.fetchone():
        return jsonify({"error": "Currency already exists"}), 400

    cur.execute(
        "INSERT INTO currencies(currency_name, rate) VALUES (%s, %s)",
        (name, rate)
    )
    conn.commit()
    conn.close()

    return jsonify({"status": "created"}), 200


@app.route("/update_currency", methods=["POST"])
def update_currency():
    data = request.json
    name = data["currency_name"]
    rate = data["rate"]

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM currencies WHERE currency_name=%s", (name,))
    if not cur.fetchone():
        return jsonify({"error": "Currency not found"}), 404

    cur.execute(
        "UPDATE currencies SET rate=%s WHERE currency_name=%s",
        (rate, name)
    )
    conn.commit()
    conn.close()

    return jsonify({"status": "updated"}), 200


@app.route("/delete", methods=["POST"])
def delete_currency():
    data = request.json
    name = data["currency_name"]

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM currencies WHERE currency_name=%s", (name,))
    if not cur.fetchone():
        return jsonify({"error": "Currency not found"}), 404

    cur.execute("DELETE FROM currencies WHERE currency_name=%s", (name,))
    conn.commit()
    conn.close()

    return jsonify({"status": "deleted"}), 200


if __name__ == "__main__":
    app.run(port=5001)