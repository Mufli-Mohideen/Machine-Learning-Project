from flask import Flask, request, jsonify, render_template
import pickle
import pandas as pd
import json
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


# bowler_data = {
#     'Player': ['B Kumar', 'SP Narine', 'R Ashwin', 'YS Chahal', 'PP Chawla', 'JJ Bumrah', 'RA Jadeja', 'Rashid Khan', 'UT Yadav', 'Sandeep Sharma',
#                'HV Patel', 'MM Sharma', 'Mohammed Shami', 'AR Patel', 'TA Boult', 'K Rabada', 'AD Russell', 'SN Thakur', 'Mohammed Siraj', 'Kuldeep Yadav',
#                'CV Varun', 'DL Chahar', 'L Balaji', 'KH Pandya', 'RD Chahar', 'Avesh Khan', 'T Natarajan', 'HH Pandya', 'Ravi Bishnoi', 'Shakib Al Hasan',
#                'PJ Cummins', 'Mustafizur Rahman', 'A Nortje', 'JO Holder', 'S Gopal', 'MA Starc', 'LH Ferguson', 'VR Aaron', 'MP Stoinis', 'AJ Tye',
#                'TU Deshpande', 'MR Marsh', 'M Markande', 'MS Gony', 'GJ Maxwell', 'Washington Sundar'],
#     'Matches': [176, 177, 212, 160, 192, 133, 240, 121, 148, 127,
#                 106, 112, 110, 150, 104, 80, 127, 95, 93, 84,
#                 71, 81, 73, 127, 78, 63, 61, 137, 66, 71,
#                 58, 57, 46, 46, 52, 41, 45, 52, 96, 30,
#                 36, 42, 37, 44, 134, 60],
#     'Balls': [3910, 4075, 4524, 3521, 3850, 3053, 3829, 2859, 3050, 2822,
#               2161, 2253, 2426, 3099, 2337, 1818, 1697, 1866, 1958, 1746,
#               1588, 1669, 1513, 2122, 1664, 1335, 1337, 1418, 1411, 1484,
#               1319, 1298, 1054, 1036, 1061, 871, 1155, 1173, 1823, 550,
#               684, 744, 703, 878, 2693, 1148],
#     'Runs': [1153, 3603, 2727, 2704, 2588, 2671, 3132, 2132, 3444, 2652,
#              1898, 2050, 2388, 2980, 2151, 1564, 1830, 1747, 1827, 1771,
#              1627, 1697, 1682, 2223, 1784, 1516, 1575, 1750, 1468, 1572,
#              1236, 1255, 1041, 1037, 1062, 876, 1158, 1177, 1846, 563,
#              686, 746, 705, 880, 2693, 1151],
#     'Wickets': [171, 127, 260, 145, 160, 190, 240, 155, 153, 147,
#                 118, 125, 133, 163, 121, 85, 97, 86, 82, 76,
#                 74, 82, 76, 118, 91, 74, 82, 76, 76, 71,
#                 72, 72, 61, 63, 68, 46, 55, 60, 104, 34,
#                 40, 43, 36, 40, 115, 63]
# }




@app.route('/')
def index():
    return render_template('index.html')

@app.route('/match')
def match():
    return render_template('match.html')

@app.route('/purplecap')
def purplecap():
    return render_template('purplecap.html')

@app.route('/orangecap')
def orangecap():
    return render_template('orangecap.html')

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

# @app.route('/predict', methods=['POST'])
# def predict():
with open('bowler_data.json') as f:
    bowler_data = json.load(f)
df = pd.DataFrame(bowler_data)
predicted_purple_cap_holder = df.loc[df['Wickets'].idxmax(), 'Player']
#     try:
#         data = request.form.to_dict()
#         print("Received form data:", data)  # Debug statement to print received form data
        
#         if not data or not all(key in data for key in ['team1', 'team2', 'venue']):
#             missing_keys = [key for key in ['team1', 'team2', 'venue'] if key not in data]
#             return jsonify({'error': f'Missing or invalid data fields: {", ".join(missing_keys)}'}), 400
        
#         # Validate team1, team2, and venue
#         if data['team1'] not in teams:
#             return jsonify({'error': f'Invalid team1: {data["team1"]}. Expected one of: {", ".join(teams)}'}), 40
with open('batsman_data.json') as f:
    batsman_data = json.load(f)
batsman_df = pd.DataFrame(batsman_data)
predicted_orange_cap_holder = batsman_df.loc[batsman_df['Runs'].idxmax(), 'Player']
#         if data['team2'] not in teams:
#             return jsonify({'error': f'Invalid team2: {data["team2"]}. Expected one of: {", ".join(teams)}'}), 400
        
#         # Standardize venue name
#         standardized_venue = venue_name_mapping.get(data['venue'], data['venue'])
#         if standardized_venue not in venues:
#             return jsonify({'error': f'Invalid venue: {standardized_venue}. Expected one of: {", ".join(venues)}'}), 400
        
#         print("Standardized venue:", standardized_venue)  # Debug statement to print standardized venue
        
#         # Prepare input data
#         input_data = {col: 0 for col in model_columns}  # Initialize all columns to 0
#         input_data[f'team1_{data["team1"]}'] = 1
#         input_data[f'team2_{data["team2"]}'] = 1
#         input_data[f'venue_{standardized_venue}'] = 1
#         print("Prepared input data:", input_data)  # Debug statement to print prepared input data
        
#         # Convert to DataFrame
#         input_df = pd.DataFrame([input_data])
#         print("Input DataFrame:", input_df)  # Debug statement to print DataFrame
        
#         # Make prediction
#         prediction = model.predict(input_df)
#         print("Prediction:", prediction[0])  # Debug statement to print prediction
        
#         return jsonify({'prediction': prediction[0]})
    
#     except KeyError as e:
#         return jsonify({'error': f'Missing key in data: {str(e)}'}), 400
    
#     except Exception as e:
#         return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/predict-purple-cap')
def predict_purple_cap():
    return jsonify({'predicted_purple_cap_holder': predicted_purple_cap_holder})

@app.route('/predict-orange-cap')
def predict_orange_cap():
    return jsonify({'predicted_orange_cap_holder': predicted_orange_cap_holder})


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
        
        # Standardize venue name
        standardized_venue = venue_name_mapping.get(data['venue'], data['venue'])
        if standardized_venue not in venues:
            return jsonify({'error': f'Invalid venue: {standardized_venue}. Expected one of: {", ".join(venues)}'}), 400
        
        print("Standardized venue:", standardized_venue)  # Debug statement to print standardized venue
        
        # Prepare input data
        input_data = {col: 0 for col in model_columns}  # Initialize all columns to 0
        input_data[f'team1_{data["team1"]}'] = 1
        input_data[f'team2_{data["team2"]}'] = 1
        input_data[f'venue_{standardized_venue}'] = 1
        print("Prepared input data:", input_data)  # Debug statement to print prepared input data
        
        # Convert to DataFrame
        input_df = pd.DataFrame([input_data])
        print("Input DataFrame:", input_df)  # Debug statement to print DataFrame
        
        # Make prediction
        prediction = model.predict(input_df)
        print("Prediction:", prediction[0])  # Debug statement to print prediction
        
        return jsonify({'prediction': prediction[0]})
    
    except KeyError as e:
        return jsonify({'error': f'Missing key in data: {str(e)}'}), 400
    
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500


if __name__ == '__main__':
    app.run(debug=True)
