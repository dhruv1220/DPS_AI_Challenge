from distutils.log import debug
from flask import Flask, request, jsonify
import final_model

app = Flask(__name__)

@app.route('/predict', methods=["POST"])
def get_prediction():
    year = request.json['year']
    # Check if year is a number
    if not str(year).isnumeric():
        return jsonify({'Error': '"year" should be a numeric value'})
    
    final_df = final_model.model_output(int(year))

    if 'month' in request.json:
        month = request.json['month']
        # Check if month is number between 1 & 12 (included)
        if str(month) != 'Summe':
            if len(str(month)) > 2:
                month = str(month)[-2:]
            if not str(month).isnumeric():
                return jsonify({'Error': '"month" should be a numeric value'})
            elif int(month) < 1 or int(month) > 12:
                return jsonify({'Error': 'Invalid month value'})
            final_df = final_df[final_df['month'] == int(month)]

    if 'category' in request.json:
        category = request.json['category']
        if category not in ['Verkehrsunfälle', 'Alkoholunfälle', 'Fluchtunfälle']:
            return jsonify({'Error': 'Invalid category'})
        final_df = final_df[final_df['category'] == category]
        
    if 'type' in request.json:
        type = request.json['type']
        if type not in ['insgesamt', 'Verletzte und Getötete', 'mit Personenschäden']:
            return jsonify({'Error': 'Invalid type'})
        final_df = final_df[final_df['type'] == type]
    
    prediction = int(final_df['prediction'].sum())
    return jsonify({'prediction': prediction})

if __name__ == '__main__':
    app.run(debug = True)
