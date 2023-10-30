import requests
import re
import chess.pgn
import io
import json
import random

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
        side                : int, the side to train on. 0 = white, 1 = black
        study_game          : chess.pgn.Game, the game that is currently being worked on 
        training_line       : list of moves, the line that is being worked on
        move_index          : int, the index of the move in training_line that is being worked on
        total_moves         : int, total number of moves made 
        total_correct       : int, number of correct moves made
        move_accuracy       : float, ratio of total_correct/total_moves
        training_board      : Board, the current board that is being worked on
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
        # Clean up whenever a new crnt_study is set 
        self.study_game = None
        self.chapters_set = set()
        self.side = 0
        self.training_line = []
        self.move_index = 0
        self.total_moves = 0
        self.total_correct = 0
        self.move_accuracy = 0.0
        self.training_board = chess.Board()

    def set_personal_token(self, personal_token):
        self.headers["Authorization"] = f"Bearer {personal_token}"


    def list_study_names(self):
        names = []
        for study_i in self.studies:
            names.append(study_i.get_name())

        return names

    def set_side(self, choice):
        if choice == 0:
            self.side = 0
        else:
            self.side = 1

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

        # Clean up
        self.study_game = None
        self.chapters_set = set()
        self.side = 0
        self.training_line = []
        self.move_index = 0
        self.total_moves = 0
        self.total_correct = 0
        self.move_accuracy = 0.0
        self.training_board = chess.Board()

        self.crnt_study = self.studies[index]
        for chapter_i in self.crnt_study.get_chapters():
            self.chapters_set.add(chapter_i)
        return index


    def delete_variation(self, node):
        '''
        Recursively delete the parent nodes of a given node, until the parent node has 
        more than one child.
        Set self.study_game to None if the node is root.
        '''
        par_node = node.parent
        if par_node == None:
            # Now we're at the root
            self.study_game = None
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

        # Check if the current line has been fully trained
        if len(self.training_line) == 0:
            if self.study_game == None: 
                # Fetch a new chapter to study if the last one runs out
                if len(self.chapters_set) == 0:
                    return None # Training is done!
            
                # next_chapter = self.chapters_set.pop()
                next_chapter = random.choice(list(self.chapters_set))
                self.chapters_set.remove(next_chapter)
                self.study_game = chess.pgn.read_game(io.StringIO(next_chapter.get_pgn()))
            
            # Randomly pick a line to train, store it in self.training_line, delete it from the study_game
            node_ptr = self.study_game
            while not node_ptr.is_end():
                list_cont = node_ptr.variations;
                node_ptr = random.choice(list_cont)
                self.training_line.append(node_ptr.move)
            self.delete_variation(node_ptr)
            self.move_index = 0
            self.training_board = chess.Board()

        # Now return the board for next position, also check if there're still moves left
        # self.move_index will be updated
        if self.move_index >= len(self.training_line):
            # Means this line has been done
            self.training_line = []
            # self.training_board = chess.Board()
            # self.move_index = 0
            return self.get_position() # Get the next line

        if self.move_index % 2 != self.side: # This check is critical when starting
            self.training_board.push(self.training_line[self.move_index])
            self.move_index += 1

        return self.training_board

    def answer(self, move):
        '''
        Check if the move provided by user is correct, and update self.training_line, 
        self.training_board, self.move_index accordingly. The parameter passed in is
        in uci format.
        Return True / False 
        '''

        self.total_moves += 1

        if self.training_line[self.move_index] == move:
            self.training_board.push(self.training_line[self.move_index])
            self.move_index += 1
            self.total_correct += 1
            self.move_accuracy = self.total_correct / self.total_moves
            return True
        else:
            self.move_accuracy = self.total_correct / self.total_moves
            return False
        
    def training(self):
        '''
        Main training function.
        '''
        self.set_side(int(input("Pick your side for training (0 for white, 1 for black): ")))

        board = self.get_position()
        while board != None:
            if self.side == 0:
                print(board.unicode())
            else:
                print(board.transform(chess.flip_vertical).transform(chess.flip_horizontal).unicode())
            result = self.answer(chess.Move.from_uci(input("Move: ")))
            print(f"total moves: {self.total_moves}, accuracy: {self.move_accuracy * 100:.2f}%")
            while not result:
                result = self.answer(chess.Move.from_uci(input("Move: ")))
                print(f"total moves: {self.total_moves}, accuracy: {self.move_accuracy * 100:.2f}%")
            board = self.get_position()

