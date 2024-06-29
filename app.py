from flask import Flask, request, jsonify, render_template
import pickle
import pandas as pd
from itertools import combinations

app = Flask(__name__)

# Load model and columns
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

with open('model_columns.pkl', 'rb') as f:
    model_columns = pickle.load(f)

# Define static data (teams and venues)
teams = [
    'Royal Challengers Bengaluru', 'Punjab Kings', 'Delhi Capitals', 'Mumbai Indians',
    'Kolkata Knight Riders', 'Rajasthan Royals', 'Sunrisers Hyderabad', 'Chennai Super Kings',
    'Gujarat Titans', 'Lucknow Super Giants'
]

venues = [
    'M Chinnaswamy Stadium', 'Wankhede Stadium', 'Narendra Modi Stadium', 'Eden Gardens',
    'Arun Jaitley Stadium', 'MA Chidambaram Stadium', 'Sawai Mansingh Stadium', 
    'Punjab Cricket Association Stadium', 'Rajiv Gandhi International Stadium'
]

venue_name_mapping = {
    'M Chinnaswamy Stadium': 'M Chinnaswamy Stadium',
    'M.Chinnaswamy Stadium': 'M Chinnaswamy Stadium',
    'M Chinnaswamy Stadium, Bengaluru': 'M Chinnaswamy Stadium',
    'Punjab Cricket Association Stadium, Mohali': 'Punjab Cricket Association Stadium',
    'Punjab Cricket Association IS Bindra Stadium, Mohali': 'Punjab Cricket Association Stadium',
    'Punjab Cricket Association IS Bindra Stadium, Mohali, Chandigarh': 'Punjab Cricket Association Stadium',
    'Feroz Shah Kotla': 'Arun Jaitley Stadium',
    'Arun Jaitley Stadium': 'Arun Jaitley Stadium',
    'Arun Jaitley Stadium, Delhi': 'Arun Jaitley Stadium',
    'Wankhede Stadium': 'Wankhede Stadium',
    'Wankhede Stadium, Mumbai': 'Wankhede Stadium',
    'Eden Gardens': 'Eden Gardens',
    'Eden Gardens, Kolkata': 'Eden Gardens',
    'Sawai Mansingh Stadium': 'Sawai Mansingh Stadium',
    'Sawai Mansingh Stadium, Jaipur': 'Sawai Mansingh Stadium',
    'Rajiv Gandhi International Stadium, Uppal': 'Rajiv Gandhi International Stadium',
    'Rajiv Gandhi International Stadium': 'Rajiv Gandhi International Stadium',
    'Rajiv Gandhi International Stadium, Uppal, Hyderabad': 'Rajiv Gandhi International Stadium',
    'MA Chidambaram Stadium, Chepauk': 'MA Chidambaram Stadium',
    'MA Chidambaram Stadium': 'MA Chidambaram Stadium',
    'MA Chidambaram Stadium, Chepauk, Chennai': 'MA Chidambaram Stadium',
    'Dr DY Patil Sports Academy': 'Dr DY Patil Sports Academy',
    'Dr DY Patil Sports Academy, Mumbai': 'Dr DY Patil Sports Academy',
    'Newlands': 'Newlands',
    "St George's Park": "St George's Park",
    'Kingsmead': 'Kingsmead',
    'SuperSport Park': 'SuperSport Park',
    'Buffalo Park': 'Buffalo Park',
    'New Wanderers Stadium': 'New Wanderers Stadium',
    'De Beers Diamond Oval': 'De Beers Diamond Oval',
    'OUTsurance Oval': 'OUTsurance Oval',
    'Brabourne Stadium': 'Brabourne Stadium',
    'Brabourne Stadium, Mumbai': 'Brabourne Stadium',
    'Sardar Patel Stadium, Motera': 'Narendra Modi Stadium',
    'Narendra Modi Stadium, Ahmedabad': 'Narendra Modi Stadium',
    'Barabati Stadium': 'Barabati Stadium',
    'Vidarbha Cricket Association Stadium, Jamtha': 'Vidarbha Cricket Association Stadium',
    'Himachal Pradesh Cricket Association Stadium': 'Himachal Pradesh Cricket Association Stadium',
    'Himachal Pradesh Cricket Association Stadium, Dharamsala': 'Himachal Pradesh Cricket Association Stadium',
    'Dr. Y.S. Rajasekhara Reddy ACA-VDCA Cricket Stadium': 'Dr Y.S. Rajasekhara Reddy ACA-VDCA Cricket Stadium',
    'Dr. Y.S. Rajasekhara Reddy ACA-VDCA Cricket Stadium, Visakhapatnam': 'Dr Y.S. Rajasekhara Reddy ACA-VDCA Cricket Stadium',
    'Subrata Roy Sahara Stadium': 'Subrata Roy Sahara Stadium',
    'Shaheed Veer Narayan Singh International Stadium': 'Shaheed Veer Narayan Singh International Stadium',
    'JSCA International Stadium Complex': 'JSCA International Stadium Complex',
    'Sheikh Zayed Stadium': 'Sheikh Zayed Stadium',
    'Zayed Cricket Stadium, Abu Dhabi': 'Sheikh Zayed Stadium',
    'Sharjah Cricket Stadium': 'Sharjah Cricket Stadium',
    'Dubai International Cricket Stadium': 'Dubai International Cricket Stadium',
    'Maharashtra Cricket Association Stadium': 'Maharashtra Cricket Association Stadium',
    'Maharashtra Cricket Association Stadium, Pune': 'Maharashtra Cricket Association Stadium',
    'Saurashtra Cricket Association Stadium': 'Saurashtra Cricket Association Stadium',
    'Green Park': 'Green Park',
    'Holkar Cricket Stadium': 'Holkar Cricket Stadium',
    'Barsapara Cricket Stadium, Guwahati': 'Barsapara Cricket Stadium',
    'Maharaja Yadavindra Singh International Cricket Stadium, Mullanpur': 'Maharaja Yadavindra Singh International Cricket Stadium',
    'Bharat Ratna Shri Atal Bihari Vajpayee Ekana Cricket Stadium, Lucknow': 'Bharat Ratna Shri Atal Bihari Vajpayee Ekana Cricket Stadium'
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/champions', methods=['GET', 'POST'])
def champions():
    if request.method == 'POST':
        try:
            # Initialize counters for each team
            team_wins = {team: 0 for team in teams}
            
            # Loop through all combinations of teams and venues
            for team1, team2 in combinations(teams, 2):
                for venue in venues:
                    input_data = {col: 0 for col in model_columns}
                    input_data[f'team1_{team1}'] = 1
                    input_data[f'team2_{team2}'] = 1
                    input_data[f'venue_{venue}'] = 1
                    
                    input_df = pd.DataFrame([input_data])
                    prediction = model.predict(input_df)
                    
                    if prediction[0] == team1:
                        team_wins[team1] += 1
                    else:
                        team_wins[team2] += 1
            
            # Determine the team with the maximum wins
            winner = max(team_wins, key=team_wins.get)
            
            # Print the winner to the console for debugging
            print(f'Debug: The predicted winner is {winner}')
            
            # Return JSON response with winner
            return jsonify({'winner': winner})
        
        except Exception as e:
            return jsonify({'error': f'Server error: {str(e)}'}), 500
    
    # GET request to render the form or initial page
    return render_template('champions.html')

@app.route('/predict-ipl-2025', methods=['GET'])
def predict_ipl_2025_winner():
    try:
        # Initialize counters for each team
        team_wins = {team: 0 for team in teams}
        
        # Loop through all combinations of teams and venues
        for team1, team2 in combinations(teams, 2):
            for venue in venues:
                input_data = {col: 0 for col in model_columns}
                input_data[f'team1_{team1}'] = 1
                input_data[f'team2_{team2}'] = 1
                input_data[f'venue_{venue}'] = 1
                
                input_df = pd.DataFrame([input_data])
                prediction = model.predict(input_df)
                
                if prediction[0] == team1:
                    team_wins[team1] += 1
                else:
                    team_wins[team2] += 1
        
        # Determine the team with the maximum wins
        winner = max(team_wins, key=team_wins.get)
        
        return jsonify({'seriesWinner': winner, 'wins': team_wins[winner]})
    
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500


@app.route('/home')
def home():
    return render_template('home.html', teams=teams, venues=venues)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.form.to_dict()
        print("Received form data:", data)  # Debug statement to print received form data
        
        if not data or not all(key in data for key in ['team1', 'team2', 'venue']):
            missing_keys = [key for key in ['team1', 'team2', 'venue'] if key not in data]
            return jsonify({'error': f'Missing or invalid data fields: {", ".join(missing_keys)}'}), 400
        
        # Validate team1, team2, and venue
        if data['team1'] not in teams:
            return jsonify({'error': f'Invalid team1: {data["team1"]}. Expected one of: {", ".join(teams)}'}), 400
        
        if data['team2'] not in teams:
            return jsonify({'error': f'Invalid team2: {data["team2"]}. Expected one of: {", ".join(teams)}'}), 400
        
        if data['venue'] not in venues:
            return jsonify({'error': f'Invalid venue: {data["venue"]}. Expected one of: {", ".join(venues)}'}), 400
        
        input_data = {col: 0 for col in model_columns}
        input_data[f'team1_{data["team1"]}'] = 1
        input_data[f'team2_{data["team2"]}'] = 1
        input_data[f'venue_{data["venue"]}'] = 1
        
        input_df = pd.DataFrame([input_data])
        prediction = model.predict(input_df)
        
        return jsonify({'winner': prediction[0]})
    
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
