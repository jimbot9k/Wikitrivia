"""
WikiTrivia - The Free and Radnom trivia games

Backend for generating questions

"""

#Prerequisites 
import wikipedia
import random
import re
from wikipedia.wikipedia import WikipediaPage

def generate_question():
    Question = ""
    Answer = ""

    #Load the page with the list of pages
    page = wikipedia.page(title="Wikipedia:Multiyear ranking of most viewed pages")
    links = page.links

    #Try load a page and keep trying till you get one
    pageLoaded = False
    while pageLoaded == False:
        try:
            random_page = random.choice(links)
            question_page = wikipedia.page(title=random_page,auto_suggest=False)
            pageLoaded = True
        except:
            pageLoaded = False
    

    page_title = question_page.title

    summary = question_page.summary
    
    summary = summary.replace(question_page.title,"_______")
    summary = summary.split('. ')[0]

    print(question_page.title)
    print(summary)

generate_question()

