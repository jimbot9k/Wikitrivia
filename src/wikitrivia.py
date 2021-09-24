"""
"""
#Prerequisites 
import wikipedia
import random
import re
import nltk
from pytrends.request import TrendReq
from difflib import SequenceMatcher
from question import MultiQuestion
import pandas as pd

pytrend = TrendReq()
#random.seed(101)

#Download natural language packages
path = './nltk_modules'
nltk.data.path.append(path)
nltk.download('punkt', download_dir=path, quiet=True)
nltk.download('wordnet', download_dir=path, quiet=True)
nltk.download('averaged_perceptron_tagger', download_dir=path, quiet=True)
nltk.download('maxent_ne_chunker', download_dir=path, quiet=True)
nltk.download('words', download_dir=path, quiet=True)


BLANK_SPACE = "______"

SIMILAR = 0.75

TOO_LONG = 4

BAD_SUBJECTS = ['Wikipedia','Wiki', 'I Ching']

def get_wrong_answers(page):

    """
    #############################################################
    # Generating Wrong answers
    #############################################################
    #Get the page title and print it

    #Get a list of the page categories
    page_categories = question_page.categories
    good_page_categories = []
    #Get rid of any that are too long (likely bad links)
    for i,x in enumerate(page_categories):
        if len(x.split(" ")) <= 2:
            good_page_categories.append(x)
    print(good_page_categories)

    #Get the category page
    category_page = wikipedia.page(title = "Category:"+good_page_categories[0],auto_suggest=False)
    print(category_page.content)

    wrong_answers =[None, None, None]
    for i in range(3):
        alternateFound = False
        while alternateFound == False:
            potentialAnswer = random.choice(category_page.links)
            if len(potentialAnswer.split(" ")) == len(page_title.split(" ")):
                alternateFound = True
                wrong_answers[i] = (potentialAnswer)
        
    summary = remove_subject(page_title, question_page.summary)
    try:
        summary = summary.split('.')[0] + "." + summary.split('.')[1] + "." + summary.split('.')[2] + "."
    except:
        summary = summary.split('.')[0] + "." + summary.split('.')[1] + "."

    """
    pytrend.build_payload(kw_list = [page])
    related_queries = pytrend.related_queries()
    length = len(page.split(" "))
    wrong_answers = {}

    for key, value in related_queries[page].items():
        for answer in value['query']:
            answer = answer.title()

            #Test to see if subject present in answer and then score how similar its type is (e.g. 'PERSON') then send
            #that sorted list back and the top 3 will be extracted in get_question
            test = remove_subject(page, answer)
            if ((similar(test, answer) > SIMILAR) and length == len(answer.split(" "))):
                wrong_answers[answer] = is_same_type(answer, page)

            wrong_answers = {k: v for k, v in sorted(wrong_answers.items(), key=lambda item: item[1], reverse=True)}




    return list(wrong_answers.keys())
        



def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def strip_brackets(text):
    return re.sub('\(.*\)', "", text)
    #return re.sub(r"\([^()]*\)", "", text)
    #Pretty sure this other one does not work


def fetch_named_entities(text):
    names = []
    for sentence in nltk.sent_tokenize(text):
        words = nltk.word_tokenize(sentence)

        for chunk in nltk.ne_chunk(nltk.pos_tag(words)):
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
            if similar(item[1], token) > SIMILAR:
                #print(item[1], " : ", token, similar(item[1], token))
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

def is_same_type(a, b):

    named_a = fetch_named_entities(a)
    named_b = fetch_named_entities(b)
    if len(named_a) == 0 or len(named_b) == 0:
        return 0

    count = 0
    total = 0
    for word_a in named_a:
        for word_b in named_b:
            if word_a[0] == word_b[0]:
                count += 1
            total += 1

    return count / total


def is_good_title(title):
    words = nltk.word_tokenize(title)
    if len(words) < TOO_LONG:
        for word in words:
            if word in BAD_SUBJECTS:
                print("Bad subject", flush=True)
                return False
        return True
    else:
        print("Too long", flush=True)
        return False


def generate_question(question_set="top annual"):
    """
    Generates a question

    ---------------------------------------------
    Arguments:
        question set: (str)
            - "top annual" : Use the top annual views list
            - "weekly 5000" : Use the weekly top 5000 views list
            - "random" : Random Questions
            - "Artists from the 10s" Top music from the 2010s
            - "grossing animes" Top Grossing Animes
            - "Top 100 Books" Top 100 books
            - "grossing films: 50 Top Grossing Films

    -------------------------------------------
    Returns:

    Question: Question Object
                            
    """

    #Parse the argument for the question 
    if question_set == "top annual":
        page_to_use = "Wikipedia:Multiyear ranking of most viewed pages"
        list_page = wikipedia.page(title=page_to_use)
        links = list_page.links

    elif question_set == "weekly 5000":
        page_to_use = "Top 5000 weekly"
        table_top_5000 = pd.read_html('https://en.m.wikipedia.org/wiki/User:West.andrew.g/Popular_pages')
        df = table_top_5000[3]
        articles = df['Article'].to_list()
        links = articles
        
    elif question_set == "Artists from the 10s":
        page_to_use = "Billboard Year-End Hot 100 singles of 2010"
        table_top_5000 = pd.read_html('https://en.wikipedia.org/wiki/Billboard_Year-End_Hot_100_singles_of_2010')
        df = table_top_5000[0]
        articles = df['Artist(s)'].to_list()
        links = articles

    elif question_set == "grossing animes":
        page_to_use = "List of highest-grossing anime films"
        table_top_5000 = pd.read_html('https://en.wikipedia.org/wiki/List_of_highest-grossing_anime_films')
        df = table_top_5000[0]
        articles = df['Title'].to_list()
        links = articles

    elif question_set == "grossing films":
        page_to_use = "list_of_highest-grossing-films"
        table = pd.read_html('https://en.wikipedia.org/wiki/List_of_highest-grossing_films')
        df = table[0]
        articles = df['Title'].to_list()
        links = articles

    elif question_set == "Top 100 Books":
        page_to_use = "List of top book lists"
        table = pd.read_html('https://en.wikipedia.org/wiki/20th_Century%27s_Greatest_Hits:_100_English-Language_Books_of_Fiction')
        df = table[0]
        articles = df['Title'].to_list()
        links = articles

    elif question_set == "random":
        page_to_use = "Fully Random Question -Good luck"
    else:
        page_to_use = "Wikipedia:Multiyear ranking of most viewed pages"
    

    print(page_to_use)
    if not question_set == "random":
        print("Selecting from: " + question_set + " which has " + str(len(links)) + " entries")
    elif question_set == "random":
        print("Selecting from: " + question_set + " which has unlimited entries")



    #Try load a page and keep trying till you get one
    pageLoaded = False
    while pageLoaded == False:
        try:
            if not (question_set == "random"):
                random_page = random.choice(links)
                print(random_page)
            else:
                random_page = "Special:Random"
            question_page = wikipedia.page(title=random_page,auto_suggest=False)
            page_title = strip_brackets(question_page.title)
            print(page_title)
            summary = remove_subject(page_title, question_page.summary)

            splitSummary = nltk.sent_tokenize(summary)
            if len(splitSummary) < 3:
                continue

            wrong_answers = []

            #Reject a page if the title is too long
            #words = nltk.word_tokenize(question_page.title)

            if is_good_title(page_title) != True:
                pageLoaded = False
                continue

            wrong_answers = get_wrong_answers(page_title)
            if len(wrong_answers) > 2:
                wrong_answers = wrong_answers[0:3]
            else:
                pageLoaded = False
                print("Not enough answers", flush=True)
                continue

            pageLoaded = True
        except:
            pageLoaded = False




    try:
        summary = splitSummary[0] +  splitSummary[1] +  splitSummary[2]
    except:
        summary = splitSummary[0] +  splitSummary[1] 

    return MultiQuestion(question=summary, content=question_set, answer=page_title, falseAnswers=wrong_answers)

#(answer, summary) = generate_question("random")
#(answer, summary) = generate_question("top annual")
#question = generate_question("weekly 5000")
#print(question.question, " : ", question.answer, ' or ', question.falseAnswers[0], ' or ', question.falseAnswers[1], ' or ', question.falseAnswers[2])

#Maybe add some movies or actors etc pages so you can have specific categories.
