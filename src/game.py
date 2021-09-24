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
        self.correctAnswer = random.randint(1,4)

        self.currentQuestion = generate_question()
        self.oldAnswer = "First Question"
        print(self.currentQuestion.get_question())
        print(self.correctAnswer)
        print(self.currentQuestion.get_answer())
        print(self.currentQuestion.get_falseAnswers())


    def add_player(self, player):
        self.players[player] = 0

    def get_question(self):
        return self.currentQuestion

    def get_answers(self):
        answers = {1: "Apple", 2:"Pear", 3:"Orange", 4:"UQCS"}
        j = 0
        for i in range(1, 5):
            if ((not (i == self.correctAnswer))):
                answers[i] = self.get_question().get_falseAnswers()[j % 4]
                j += 1
        answers[self.correctAnswer] = self.get_question().get_answer()
        return answers
    
    def answer_question(self, player, answer):
        self.playerAnswers[player] = answer

    def get_next_question(self, questionSet):
        self.currentQuestion = generate_question(questionSet)
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

    def get_old_answer(self):
        return self.oldAnswer
    
    def end_round(self, questionSet):
        self.oldAnswer = self.get_question().get_answer()
        self.update_scores()
        self.get_next_question(questionSet)

