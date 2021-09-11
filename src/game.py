"""
Game - Class to manage games of Wikitrivia
"""
class Game:

    def __init__(self, roomID, host, players):
        self.roomID = roomID
        self.players = players
        self.host = host
        self.currentQuestion = None
        self.correctAnswer = 0
        self.playerAnswers= {}
        for player in players:
            self.playerAnswers[player] = 0
        self.scores = {}
        for player in players:
            self.scores[player] = 0

    def add_player(self, player):
        self.players[player] = 0
    
    def answer_question(self, player, answer):
        self.playerAnswers[player] = answer

    def get_next_question(self):
        pass

    def get_player_list(self):
        player_list = ""
        for player in self.players:
            player_list += '{player}:{score}<br>'.format(player=player, score=self.players[player])
        return player_list

    def update_scores(self):
        for player in self.playerAnswers:
            if self.playerAnswers[player] == self.correctAnswer:
                self.players[player] += 1
                self.playerAnswers[player] = 0
    
    def end_round(self):
        self.update_scores()
        self.get_next_question()

