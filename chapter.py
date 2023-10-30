class Chapter:
    '''
    Class: Chapter
    Attributes:
        pgn                 : string, pgn of the chapter
        name                : string, name of the chapter
    '''

    def __init__(self, pgn, name):
        self.pgn = pgn
        self.name = name

    def get_pgn(self):
        return self.pgn

    def get_name(self):
        return self.name