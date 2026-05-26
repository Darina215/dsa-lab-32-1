from flask import Flask, request, jsonify

app = Flask(__name__)

RATES = {
    "USD": 100.01,
    "EUR": 110.50
}

@app.route("/rate", methods=["GET"])
def get_rate():

    try:
        currency = request.args.get("currency")

        if not currency or currency not in RATES:
            return jsonify({"message": "UNKNOWN CURRENCY"}), 400

        return jsonify({"rate": RATES[currency]}), 200

    except Exception as e:
        print(e)
        return jsonify({"message": "UNEXPECTED ERROR"}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5001)