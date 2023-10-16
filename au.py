import requests
import re
import chess.pgn
import io

class Study:
    '''
    Class: Study
    Attributes: 
        personal_token      : string, to access private studies
        study_id            : string, the study that is currently being worked on
        study_game          : Game, the game that is currently being worked on   
    '''

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
            pgn_moves = []
            for pgn_game in pgn_games:
                temp = pgn_game.split('\n\n')
                pgn_info.append(temp[0])
                pgn_moves.append(temp[-1])
            return pgn_info, pgn_moves
        else:
            return None, f"Failed to retrieve PGN for study {study_id}. Status Code: {response.status_code}"

    def display_lines(self, pgn):
        game = chess.pgn.read_game(io.StringIO(pgn))
        if game:
            board = game.board()
            print('Mainline')
            for move in game.mainline_moves():
                board.push(move)
                print(board)
                print()
            print('Sidelines')
            side_cnt = 0
            for sideline in game.variations:
                side_cnt = side_cnt + 1
                print(f'sideline {side_cnt}')
                print(sideline)
        else:
            return None

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
info_parts, pgn_moves = study.get_study_pgn(valid_study_id)

print("Information Parts:")
print(info_parts)
print("\nPGN Moves:")
print(pgn_moves)

# Analyze and display the board for the first game in the study
if pgn_moves:
    board = study.display_lines(pgn_moves[0])
