import random
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Возможные операции
operations = ["sum", "sub", "mul", "div"]


# Раздел I.

@app.route('/number/', methods=['GET'])
def get_number():
    param = int(request.args.get('param', 1))
    rand_num = random.randint(1, 10)

    result = rand_num * param

    return jsonify({
        "number": result,
        "operation": random.choice(operations)
    })


@app.route('/number/', methods=['POST'])
def post_number():
    data = request.get_json()
    json_param = int(data.get('jsonParam', 1))

    rand_num = random.randint(1, 10)
    operation = random.choice(operations)

    result = rand_num * json_param

    return jsonify({
        "number": result,
        "operation": operation
    })


@app.route('/number/', methods=['DELETE'])
def delete_number():
    return jsonify({
        "number": random.randint(1, 10),
        "operation": random.choice(operations)
    })


# Раздел II.

def calculate_expression():
    base_url = "http://127.0.0.1:5000/number/"

    # 1. GET
    param = random.randint(1, 10)
    r1 = requests.get(base_url, params={"param": param}).json()

    # 2. POST
    json_param = random.randint(1, 10)
    r2 = requests.post(
        base_url,
        json={"jsonParam": json_param},
        headers={"Content-Type": "application/json"}
    ).json()

    # 3. DELETE
    r3 = requests.delete(base_url).json()

    responses = [r1, r2, r3]

    print("Ответы сервера:")
    for r in responses:
        print(r)

    # 4. Вычисление
    result = responses[0]["number"]

    for r in responses[1:]:
        num = r["number"]
        op = r["operation"]

        if op == "sum":
            result += num
        elif op == "sub":
            result -= num
        elif op == "mul":
            result *= num
        elif op == "div":
            if num != 0:
                result /= num

    result = int(result)

    print("Итоговый результат:", result)


# Запуск

if __name__ == "__main__":
    from threading import Thread

    # Запускаем сервер в отдельном потоке
    server = Thread(target=lambda: app.run(debug=False))
    server.start()

    # Даем серверу запуститься
    import time
    time.sleep(1)

    # Запускаем клиентскую часть
    calculate_expression()