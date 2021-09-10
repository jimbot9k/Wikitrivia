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

    page = wikipedia.page(title="Wikipedia:Multiyear ranking of most viewed pages")
    links = page.links

    random_page = random.choice(links)

    search_results = wikipedia.search(random_page)
    
    print(search_results[0])
    question_page = wikipedia.page(title=search_results[0])

    page_title = question_page.title

    summary = question_page.summary
    
    summary = summary.replace(question_page.title,"_______")

    print(question_page.title)
    print(summary)


generate_question()

