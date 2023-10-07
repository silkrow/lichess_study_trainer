import requests
import re

class Study:
    def __init__(self, personal_token=None):
        self.base_url = "https://lichess.org/api/"
        self.headers = {
            "Accept": "application/json",
        }
        if personal_token:
            self.set_personal_token(personal_token)

    def set_personal_token(self, personal_token):
        self.headers["Authorization"] = f"Bearer {personal_token}"

    def list_studies(self, username):
        studies_url = f"{self.base_url}study/by/{username}"
        response = requests.get(studies_url, headers=self.headers)

        if response.status_code == 200:
            return response.text
        else:
            return f"Failed to list studies. Status Code: {response.status_code}"

    def get_study_pgn(self, study_id):
        study_url = f"{self.base_url}study/{study_id}.pgn"
        response = requests.get(study_url, headers=self.headers)

        if response.status_code == 200:
            raw_pgn = response.text
            # Split the raw PGN into individual games
            pgn_games = re.split(r'\n\n\n', raw_pgn)[:-1]
            pgn_info = []
            pgn_move = []
            for pgn_game in pgn_games:
                temp = pgn_game.split('\n\n')
                pgn_info.append(temp[0])
                pgn_move.append(temp[-1])
            return pgn_info, pgn_move
        else:
            return None, f"Failed to retrieve PGN for study {study_id}. Status Code: {response.status_code}"

# Example usage:
study = Study()  # Initialize without a token
# Authenticate later using a personal access token
personal_token = "lip_EOEhmhXG2MsPWuBiDFI7"
study.set_personal_token(personal_token)

# Ask the user for inputs interactively
valid_username = input("Enter a valid Lichess username: ")
study_list_result = study.list_studies(valid_username)
print(study_list_result)

valid_study_id = input("Enter a valid study ID: ")
info_parts, raw_pgn = study.get_study_pgn(valid_study_id)

print("Information Parts:")
print(info_parts)
print("\nRaw PGN:")
print(raw_pgn)

