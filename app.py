from flask import Flask, request, jsonify, render_template
import pandas as pd
import joblib

# Initialize the Flask application
app = Flask(__name__)

# Load the pre-trained model and scalers
rfc = joblib.load('random_forest_model.pkl')
standard = joblib.load('standard_scaler.pkl')
q_transformer = joblib.load('quantile_transformer.pkl')

# Load original data for expected loss calculation (make sure this path is correct)
df = pd.read_csv('./data/Loan_Data.csv')

# Define the features used in the model
features = ['credit_lines_outstanding', 'loan_amt_outstanding', 'total_debt_outstanding', 'income', 'years_employed', 'fico_score']

def expected_loss_estimate(rfc, X_test_df, input_df, recovery_rate=0.1):
    prob_default = rfc.predict_proba(X_test_df)[:, 1]  # Get probability of default (second column)
    exposure_at_def = input_df['total_debt_outstanding'].values[0]  # Assuming single entry for prediction
    estimated_loss = exposure_at_def * prob_default * (1 - recovery_rate)
    return prob_default[0], estimated_loss[0]  # Return single values

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json(force=True)
    recovery_rate = data["recovery_rate"]
    input_df = pd.DataFrame(data["data"], index=[0])
    
    # Scale and transform input data
    scaled_data = standard.transform(input_df[features])
    transformed_data = q_transformer.transform(scaled_data)
    
    # Create a DataFrame with transformed data for prediction
    X_test_df = pd.DataFrame(transformed_data, columns=features)
    
    # Calculate prediction and expected loss
    prediction = rfc.predict(X_test_df)
    prob_default, expected_loss = expected_loss_estimate(rfc, X_test_df, input_df, recovery_rate)

    # Results
    pred = int(prediction[0])
    result = "Yes" if pred == 1 else "No"
    
    return jsonify({
        'prediction': result,
        'expected_loss': expected_loss,
        'probability_of_default': prob_default
    })

if __name__ == '__main__':
    app.run(debug=True)