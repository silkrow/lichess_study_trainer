import requests
import re
import chess.pgn
import io
import json

from study import Study
from chapter import Chapter

class Trainer:
    '''
    Class: Trainer
    Attributes: 
        personal_token      : string, to access private studies
        studies             : list of Study objects, candidates for training
        study               : Study object, the study that is being worked on
        study_game          : chess.pgn.Game, the game that is currently being worked on   
    '''

    def __init__(self, personal_token=None):
        self.base_url = "https://lichess.org/api/"
        self.headers = {
            "Accept": "application/json",
        }
        if personal_token:
            self.set_personal_token(personal_token)

        self.studies = []
        self.study = None
        self.study_game = None

    def set_personal_token(self, personal_token):
        self.headers["Authorization"] = f"Bearer {personal_token}"

    def fetch_studies(self, username):
        '''
        This function will fetch all the studies owned by a user, and append the Study objects
        to the self.studies list. But the Study objects will only be initiated with study id, 
        study name, and author info, no pgn fetch will be done. 
        Return the number of studies loaded. 
        Return None on failure.
        '''
        studies_url = f"{self.base_url}study/by/{username}"
        response = requests.get(studies_url, headers=self.headers)
        if response.status_code == 200:
            json_objects = response.text.strip().split("\n")
            ids = [json.loads(obj)["id"] for obj in json_objects]
            names = [json.loads(obj)["name"] for obj in json_objects]

            for i in range(len(ids)):
                new_study = Study(ids[i], username, names[i])
                self.studies.append(new_study)

            return len(ids)
        else: # Error in fetching studies of the user
            return None

    def update_study(self, study_id):
        '''
        Update a Study object in self.studies list, fill in its chapters array, initialize each
        Chapter object in it with the pgn.
        Return the number of chapters loaded.
        Return None on failure.
        '''
        for study_i in self.studies:
            if study_i.get_id() == study_id:
                study_url = f"{self.base_url}study/{study_id}.pgn"
                response = requests.get(study_url, headers=self.headers)

                if response.status_code == 200:
                    raw_pgn = response.text
                    # Split the raw PGN into individual games
                    pgn_games = re.split(r'\n\n\n', raw_pgn)[:-1]
                    # pgn_info = []
                    # pgn_moves = []
                    # for pgn_game in pgn_games:
                    #     temp = pgn_game.split('\n\n')
                    #     pgn_info.append(temp[0])
                    #     pgn_moves.append(temp[-1])
                    # return pgn_info, pgn_moves

                    study_i.clear_chapters()
                    for pgn_i in pgn_games:
                        new_chapter = Chapter(pgn_i)
                        study_i.add_chapter(new_chapter)

                    return study_i.total_chapters()

                else:
                    return None

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