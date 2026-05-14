from flask import Flask, request, jsonify
from db import get_connection

app = Flask(__name__)

@app.route("/convert", methods=["GET"])
def convert():
    name = request.args.get("currency")
    amount = float(request.args.get("amount"))

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT rate FROM currencies WHERE currency_name=%s", (name,))
    row = cur.fetchone()

    if not row:
        return jsonify({"error": "Currency not found"}), 404

    rate = float(row[0])
    result = amount * rate

    return jsonify({
        "currency": name,
        "amount": amount,
        "converted": result
    }), 200


@app.route("/currencies", methods=["GET"])
def get_currencies():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT currency_name, rate FROM currencies")
    rows = cur.fetchall()

    return jsonify([
        {"currency_name": r[0], "rate": float(r[1])}
        for r in rows
    ]), 200


if __name__ == "__main__":
    app.run(port=5002)