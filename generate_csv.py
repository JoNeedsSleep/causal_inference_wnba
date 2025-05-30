import json
import csv
import os
import glob

def convert_minutes_to_decimal(time_str):
    """Convert MM:SS format to decimal minutes (e.g., '25:30' -> 25.5)"""
    if not time_str or time_str == "":
        return 0.0
    try:
        parts = time_str.split(":")
        if len(parts) == 2:
            minutes = int(parts[0])
            seconds = int(parts[1])
            return round(minutes + (seconds / 60.0), 2)
        else:
            return 0.0
    except (ValueError, IndexError):
        return 0.0

# Define the output CSV file name
output_file = "wnba_player_game_data.csv"

# Define the CSV columns
columns = [
    "id", "scheduled", "player_full_name", "player_id", "player_starter", 
    "player_rebounds", "player_position", "player_steals", "player_blocks",
    "minutes_on_court",
    "home_name", "home_alias", "away_name", "away_alias",
    "referee_1_full_name", "referee_2_full_name", "referee_3_full_name"
]

# Create a list to store all the data
all_data = []

# Get all JSON files in the game_data directory
game_files = glob.glob("game_data/*.json")

# Process each game file
for file_path in game_files:
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        # Get game ID and scheduled date
        game_id = data.get("id", "")
        scheduled = data.get("scheduled", "")
        
        # Get home and away team information
        home_name = data.get("home", {}).get("name", "")
        home_alias = data.get("home", {}).get("alias", "")
        away_name = data.get("away", {}).get("name", "")
        away_alias = data.get("away", {}).get("alias", "")
        
        # Get referee information
        referees = data.get("officials", [])
        referee_1_full_name = referees[0].get("full_name", "") if len(referees) > 0 else ""
        referee_2_full_name = referees[1].get("full_name", "") if len(referees) > 1 else ""
        referee_3_full_name = referees[2].get("full_name", "") if len(referees) > 2 else ""
        
        # Get all players from home and away teams
        if "home" in data and "players" in data["home"] and "away" in data and "players" in data["away"]:
            all_players = data["home"]["players"] + data["away"]["players"]
            
            for player in all_players:
                player_full_name = player.get("full_name", "")
                player_id = player.get("id", "")
                player_starter = "Yes" if player.get("starter", False) else "No"
                player_position = player.get("position", "")
                
                # Get statistics
                stats = player.get("statistics", {})
                player_rebounds = stats.get("rebounds", 0)
                player_steals = stats.get("steals", 0)
                player_blocks = stats.get("blocks", 0)
                
                # Get minutes and convert to decimal
                minutes_str = stats.get("minutes", "")
                minutes_on_court = convert_minutes_to_decimal(minutes_str)
                
                # Add player data to the list
                player_data = [
                    game_id, scheduled, player_full_name, player_id, player_starter,
                    player_rebounds, player_position, player_steals, player_blocks,
                    minutes_on_court,
                    home_name, home_alias, away_name, away_alias,
                    referee_1_full_name, referee_2_full_name, referee_3_full_name
                ]
                
                all_data.append(player_data)
        else:
            print(f"Warning: Missing player data in {file_path}")
            
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

# Write data to CSV file
with open(output_file, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    
    # Write the header
    writer.writerow(columns)
    
    # Write the data
    writer.writerows(all_data)

print(f"Data has been successfully written to {output_file}")
print(f"Total records: {len(all_data)}")