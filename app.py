from distutils.log import debug
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/predict', methods=["POST"])
def get_prediction():
    ret = {}
    year = request.json['year']
    # Check if year is a number
    if not str(year).isnumeric():
        return jsonify({'Error': '"year" should be a numeric value'})
    ret['year'] = int(year)

    if 'month' in request.json:
        month = request.json['month']
        # Check if month is number between 1 & 12 (included)
        if not str(month).isnumeric():
            return jsonify({'Error': '"month" should be a numeric value'})
        elif int(month) < 1 or int(month) > 12:
            return jsonify({'Error': 'Invalid month value'})
        ret['month'] = int(month)

    if 'category' in request.json:
        category = request.json['category']
        if category not in ['Verkehrsunfälle', 'Alkoholunfälle', 'Fluchtunfälle']:
            return jsonify({'Error': 'Invalid category'})
        ret['category'] = category
    if 'type' in request.json:
        type = request.json['type']
        if type not in ['insgesamt', 'Verletzte und Getötete', 'mit Personenschäden']:
            return jsonify({'Error': 'Invalid type'})
        ret['type'] = type
    
    return jsonify(ret)

if __name__ == '__main__':
    app.run(debug = True)
