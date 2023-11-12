from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/add', methods=['GET', 'POST'])
def add_numbers():
    if request.method == 'GET':
        num1 = float(request.args.get('num1', 0))
        num2 = float(request.args.get('num2', 0))
    elif request.method == 'POST':
        data = request.get_json()
        num1 = float(data.get('num1', 0))
        num2 = float(data.get('num2', 0))

    result = num1 + num2
    response = {'result': result}

    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
