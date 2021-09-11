"""
WikiTrivia - The Free and Radnom trivia games

Backend for generating questions

"""
#Prerequisites 
import wikipedia
import random
import re
import nltk
import contextlib

with contextlib.redirect_stdout(None):
    #Download natural language packages
    path = './nltk_modules'
    nltk.data.path.append(path)
    nltk.download('punkt', download_dir=path,quiet=True)
    nltk.download('wordnet', download_dir=path,quiet=True)
    nltk.download('averaged_perceptron_tagger', download_dir=path,quiet=True)
    nltk.download('maxent_ne_chunker', download_dir=path,quiet=True)
    nltk.download('words', download_dir=path,quiet=True)


BLANK_SPACE = "______"


def strip_brackets(text):
    return re.sub('\(.*\)', "", text)


def fetch_named_entities(text):
    names = []
    for sentence in nltk.sent_tokenize(text):
        for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sentence))):
            if hasattr(chunk, 'label'):
                #print(chunk.label(), ' '.join(c[0] for c in chunk))
                names.append((chunk.label(), chunk[0][0]))

    return names


def remove_subject(subject, text):
    text = strip_brackets(text)

    subject_list = fetch_named_entities(text)

    for item in subject_list:
        if item[0] == 'PERSON': #TODO: Generalise to all types
            if nltk.corpus.wordnet.synsets(item[1]):
                #print(item, "!!!!!!!")
                text = text.replace(item[1], BLANK_SPACE)
                    
    subject_split = subject.split(" ")
    for token in subject_split:
        text = text.replace(token, BLANK_SPACE)
        
    return text


def generate_question(question_set="top annual"):
    """
    Generates a question

    ---------------------------------------------
    Arguments:
        question set: (str)
            - "top annual" : Use the top annual views list
            - "weekly 5000" : Use the weekly top 5000 views list

    -------------------------------------------
    Returns:

    (answer (str), question (str)) : tuple of answer and question 
                                     stored as strings
    """
    Question = ""
    Answer = ""

    #Parse the argument for the question 
    if question_set == "top annual":
        page_to_use = "Wikipedia:Multiyear ranking of most viewed pages"
    elif question_set == "weekly 5000":
        page_to_use = "https://en.m.wikipedia.org/wiki/User:West.andrew.g/Popular_pages"
    else:
        page_to_use = "Wikipedia:Multiyear ranking of most viewed pages"
    
    #Load the page with the list of pages
    list_page = wikipedia.page(title=page_to_use)
    links = list_page.links
    print("Selecting from : " + list_page.title)

    #Try load a page and keep trying till you get one
    pageLoaded = False
    while pageLoaded == False:
        try:
            random_page = random.choice(links)
            # question_page = wikipedia.page(title=random_page,auto_suggest=False)
            question_page = wikipedia.page(title=random_page,auto_suggest=False)
            question_page_title = question_page.title

            #Reject a page if the title is too long
            print("Got here")
            print(question_page_title)

            if len(question_page.title.split(" ")) < 4:
                pageLoaded = True
            else: 
                pageLoaded = False
        except:
            pageLoaded = False
    
    page_title = strip_brackets(question_page.title)
    print(page_title)


    summary = remove_subject(page_title, question_page.summary)
    summary = summary.split('.')[0] + "."

    print(summary)

    return (page_title,summary)

(answer, summary) = generate_question("weekly 5000")
#(answer, summary) = generate_question("top annual")

#print(fetch_named_entities(answer))

