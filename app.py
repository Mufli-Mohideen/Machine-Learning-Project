from flask import Flask, request, jsonify, render_template
import pickle
import pandas as pd

app = Flask(__name__)

# Load model and columns
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

with open('model_columns.pkl', 'rb') as f:
    model_columns = pickle.load(f)

# Example list of teams (replace with actual team names)
teams = ['Team A', 'Team B', 'Team C']  # You should fetch actual team names dynamically

@app.route('/')
def home():
    return render_template('index.html', teams=teams)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.form.to_dict()
    input_data = pd.DataFrame([data], columns=model_columns)
    prediction = model.predict(input_data)
    return jsonify({'prediction': prediction[0]})

if __name__ == '__main__':
    app.run(debug=True)
