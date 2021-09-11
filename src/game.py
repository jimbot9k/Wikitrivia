from question import MultiQuestion
from wikitrivia import generate_question
import random
"""
Game - Class to manage games of Wikitrivia
"""
class Game:

    def __init__(self, roomID, host, players):
        self.roomID = roomID
        self.players = players
        self.host = host

        self.playerAnswers= {}
        for player in players:
            self.playerAnswers[player] = 0
        self.scores = {}
        for player in players:
            self.scores[player] = 0

        self.currentQuestion = generate_question()
        print(self.currentQuestion.get_question())
        print(self.currentQuestion.get_answer())
        print(self.currentQuestion.get_falseAnswers())

        self.correctAnswer = random.randint(1,5)

    def add_player(self, player):
        self.players[player] = 0

    def get_question(self):
        return self.currentQuestion

    def get_answers(self):
        answers = {}
        answers[self.correctAnswer] = self.get_question().get_answer()
        j = 0
        for i in range(1, 5):
            if (not (i == self.correctAnswer)):
                print("{x}:{y}".format(x=j,y=self.get_question().get_falseAnswers()[j]))
                answers[i] = self.get_question().get_falseAnswers()[j]
                j += 1
        return answers
    
    def answer_question(self, player, answer):
        self.playerAnswers[player] = answer

    def get_next_question(self):
        self.currentQuestion = generate_question()
        print(self.currentQuestion.get_question())
        print(self.currentQuestion.get_answer())
        print(self.currentQuestion.get_falseAnswers())

        self.correctAnswer = random.randint(1,5)

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

