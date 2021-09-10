"""
WikiTrivia - The Free and Radnom trivia games

Backend for generating questions

"""

#Prerequisites 
import wikipedia

def generate_question():
    Question = ""
    Answer = ""

    page = wikipedia.random()

    print("Page")

