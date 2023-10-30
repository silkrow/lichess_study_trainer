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
        study_ind           : dictionary, mappings between study name and index in studies
        crnt_study          : Study object, the study that is being worked on
        chapters_set        : set, a set containing all the chapters in crnt_study that hasn't been worked on
        side                : int, the side to train on. 0 = black, 1 = white
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
        self.study_ind = {}
        self.crnt_study = None
        self.study_game = None
        self.chapters_set = set()
        self.side = 1

    def set_personal_token(self, personal_token):
        self.headers["Authorization"] = f"Bearer {personal_token}"


    def list_study_names(self):
        names = []
        for study_i in self.studies:
            names.append(study_i.get_name())

        return names

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
                index = len(self.studies)
                self.study_ind[names[i]] = index # Mapping of name -> index
                self.studies.append(new_study)
                self.studies[-1].assign_index(index)

            return len(ids)
        else: # Error in fetching studies of the user
            return None

    def get_study_index(self, name):
        '''
        Return an index in self.studies at where the study with this name
        is stored.
        Return None if no study with such name exists.
        '''
        return self.study_ind.get(name)

    def update_study(self, name):
        '''
        Update a Study object in self.studies list, fill in its chapters array, initialize each
        Chapter object in it with the pgn.
        Return the number of chapters loaded.
        Return None on failure.
        '''
        index = self.get_study_index(name)

        if index == None:
            return None

        study_id = self.studies[index].get_id()

        for study_i in self.studies:
            if study_i.get_id() == study_id:
                study_url = f"{self.base_url}study/{study_id}.pgn"
                response = requests.get(study_url, headers=self.headers)

                if response.status_code == 200:
                    raw_pgn = response.text
                    # Split the raw PGN into individual games
                    pgn_games = re.split(r'\n\n\n', raw_pgn)[:-1]
                    study_i.clear_chapters()
                    for pgn_i in pgn_games:
                        # Here we assume all chapters have a name (in Event field)
                        # TODO: Grabing the Event can also be done with chess.pgn.read_headers
                        pattern = r'\[Event "(.*?)"\]'
                        match = re.search(pattern, pgn_i)
                        event_name = match.group(1)
                        new_chapter = Chapter(pgn_i, event_name)
                        study_i.add_chapter(new_chapter)

                    return study_i.total_chapters()

                else:
                    return None

    def set_crnt_study(self, name):
        '''
        Set the current study by its name, update self.crnt_study.
        Set self.chapters_set.
        Return the index of this study in self.studies.
        Return None if this study doesn't exist.
        '''
        index = self.get_study_index(name)
        if index == None:
            return None

        self.update_study(name) # Update the study here before setting it to crnt

        self.crnt_study = self.studies[index]
        for chapter_i in self.crnt_study.get_chapters():
            self.chapters_set.add(chapter_i)
        return index


    def delete_variation(self, node):
        par_node = node.parent
        if par_node == None:
            return
        par_node.remove_variation(node)
        if par_node.is_end():
            self.delete_variation(par_node)
        return

    def get_position(self):
        '''
        Get the next position to work on.
        If the study_game is empty, update it with a new chapter. 
        Whenever a study_game is out of move, reset it to None.
        Return a Board.
        Return None if no more chapter available.
        '''

        if self.study_game == None: # Fetch a new chapter to study
            if len(self.chapters_set) == 0:
                return None # Training is done!
            next_chapter = self.chapters_set.pop()
            self.study_game = chess.pgn.read_game(io.StringIO(next_chapter.get_pgn()))

        game2 = self.study_game.end()
        print(game2.board())

        self.delete_variation(game2)

        board = self.study_game.board()
        for move in self.study_game.mainline_moves():
            board.push(move)
        return board

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