from flask import Flask, request, jsonify
import pickle
import pandas as pd
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests

# Load model and processors
with open('robust_scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)
with open('model_freq_map.pkl', 'rb') as f:
    model_freq_map = pickle.load(f)
with open('logistic_model.pkl', 'rb') as f:
    model = pickle.load(f)
with open('model_metrics.json', 'r') as f:
    metrics = json.load(f)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        category_anomaly = data.get('category_anomaly')
        maker = data.get('maker')
        model_name = data.get('model')
        seat_count = data.get('seatCount')
        door_count = data.get('doorCount')
        repair_cost = float(data.get('repairCost'))
        repair_hours = float(data.get('repairHours'))
        repair_complexity = data.get('repairComplexity')

        # Validate input
        if category_anomaly not in {0, 1}:
            return jsonify({'error': 'category_anomaly must be 0 or 1'}), 400
        if not (2 <= seat_count <= 20):
            return jsonify({'error': 'seatCount must be between 2-20'}), 400
        if not (2 <= door_count <= 7):
            return jsonify({'error': 'doorCount must be between 2-7'}), 400
        if repair_complexity not in {1, 2, 3, 4}:
            return jsonify({'error': 'repairComplexity must be between 1-4'}), 400

        # Feature engineering
        maker_dacia = 1 if maker.lower() == 'dacia' else 0
        maker_ford = 1 if maker.lower() == 'ford' else 0
        model_freq = model_freq_map.get(model_name, min(model_freq_map.values()))

        num_features = [[model_freq, seat_count, door_count, repair_cost, repair_hours]]
        scaled_num = scaler.transform(num_features)

        final_features = pd.DataFrame(
            data={
                'Seat_num': scaled_num[:, 1],
                'Door_num': scaled_num[:, 2],
                'repair_cost': scaled_num[:, 3],
                'repair_hours': scaled_num[:, 4],
                'Model_FreqEncoded': scaled_num[:, 0],
                'category_anomaly': [category_anomaly],
                'Maker_Ford': [maker_ford],
                'repair_complexity': [repair_complexity],
                'Maker_Dacia': [maker_dacia]
            }
        )

        # Make prediction
        proba = model.predict_proba(final_features)[0][1]
        result = 'Will Claim' if proba > 0.5 else 'Will Not Claim'

        return jsonify({
            'prediction': result,
            'probability': proba
        })

    except Exception as e:
        print('Exception', e)
        return jsonify({
            "error": f"Prediction failed: {str(e)}",
            "type": type(e).__name__,
            "debug": "Please check if input parameters meet the requirements"
        }), 500

if __name__ == '__main__':
    app.run(debug=True)