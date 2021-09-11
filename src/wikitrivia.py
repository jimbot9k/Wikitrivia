"""
"""
#Prerequisites 
import wikipedia
import random
import re
import nltk
from difflib import SequenceMatcher

#Download natural language packages
path = './nltk_modules'
nltk.data.path.append(path)
nltk.download('punkt', download_dir=path, quiet=True)
nltk.download('wordnet', download_dir=path, quiet=True)
nltk.download('averaged_perceptron_tagger', download_dir=path, quiet=True)
nltk.download('maxent_ne_chunker', download_dir=path, quiet=True)
nltk.download('words', download_dir=path, quiet=True)


BLANK_SPACE = "______"

BAD_SUBJECTS = ['Wikipedia']

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

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
    remove_list = []
    questions = strip_brackets(text)
    subject_split = nltk.word_tokenize(subject)
    for string in subject_split:
        remove_list.append(string)
        #Case sensitivity
        remove_list.append(string.lower())

    subject_labels = fetch_named_entities(subject)
    text_labels = fetch_named_entities(text)

    #Store all synonyms of subject
    subject_synsets = []
    for label in subject_labels:
        synset = nltk.corpus.wordnet.synsets(label[1])
        for syn in synset:
            subject_synsets.append(syn)

    for item in text_labels:
        #String similarity check 0.75 arbritrary number
        for token in subject_split:
            if similar(item[1], token) > 0.75:
                print(item[1], " : ", token, similar(item[1], token))
                remove_list.append(item[1])

        if item[0] == text_labels[0][0]:
            #print(item)

            #Catch all synonyms of the subject
            synset = nltk.corpus.wordnet.synsets(item[1])
            if synset:
                for syn in synset:
                    if syn in subject_synsets:
                        #print(syn, "!!!!!!")
                        remove_list.append(item[1])

    #Attempt to remove big words first
    remove_list.sort(key=len, reverse=True)
    for item in remove_list:
        questions = questions.replace(item, BLANK_SPACE)

                        
    return questions


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
            #random.seed(100)
            random_page = random.choice(links)
            question_page = wikipedia.page(title=random_page,auto_suggest=False)
            #question_page = wikipedia.page(title='Estonian Wikipedia',auto_suggest=False)
            question_page_title = question_page.title

            #Reject a page if the title is too long
            print("Got here")
            print(question_page_title)

            words = nltk.word_tokenize(question_page.title)
            if len(words) < 4:
                for word in words:
                    if word in BAD_SUBJECTS:
                        pageLoaded = False
                        break
                    pageLoaded = True
            else: 
                pageLoaded = False
        except:
            pageLoaded = False
    
    page_title = strip_brackets(question_page.title)

    summary = remove_subject(page_title, question_page.summary)
    #summary = summary.split('.')[0] + "."

    print(summary)

    return (page_title,summary)

(answer, summary) = generate_question("weekly 5000")
#(answer, summary) = generate_question("top annual")

#print(fetch_named_entities(answer))

