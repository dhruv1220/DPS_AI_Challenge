from distutils.log import debug
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/predict', methods=["POST"])
def add_guide():
    year = request.json['year']
    if 'month' in request.json:
        month = request.json['month']
        return jsonify({'content': month})
    return jsonify({'content_year':'month not present'})

if __name__ == '__main__':
    app.run(debug = True)
