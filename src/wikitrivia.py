"""
WikiTrivia - The Free and Radnom trivia games

Backend for generating questions

"""

#Prerequisites 
import wikipedia

def generate_question():
    Question = ""
    Answer = ""

    pageName = wikipedia.random()

    page = wikipedia.page(title=pageName)
    print(page.title)

    summary = page.summary
    
    summary = summary.replace(page.title,"_______")

    print(summary)

generate_question()

