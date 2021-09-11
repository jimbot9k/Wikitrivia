"""
Game - Class to manage games of Wikitrivia
"""
class Game:

    def __init__(self, roomID, players):
        self.roomID = roomID
        self.players = players
        self.currentQuestion = None
        self.nextQuestion = None

        self.scores = {}
        for player in players:
            self.scores[player] = 0

    def get_room_id(self):
        return self.roomID

    def get_players(self):
        return self.players
    
    def answer_question(self):
        pass

    def get_next_question(self):
        pass

    def get_player_score(self, player):
        return self.scores[player]

    def add_player_score(self, player, score):
        self.scores[player] += score

