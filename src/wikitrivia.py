"""
WikiTrivia - The Free and Radnom trivia games

Backend for generating questions

"""
#Prerequisites 
import wikipedia
import re
import nltk

#Download natural language packages
path = './nltk_modules'
nltk.data.path.append(path)
nltk.download('punkt', download_dir=path)
nltk.download('wordnet', download_dir=path)
nltk.download('averaged_perceptron_tagger', download_dir=path)
nltk.download('maxent_ne_chunker', download_dir=path)
nltk.download('words', download_dir=path)


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
                text = text.replace(item[1], BLANK_SPACE)
                    
    subject_split = subject.split(" ")
    for token in subject_split:
        text = text.replace(token, BLANK_SPACE)
        
    return text


def generate_question():
    Question = ""
    Answer = ""

    #pageName = wikipedia.random()

    page = wikipedia.page(title='Tupac Shakur')
    title = page.title

    title = re.sub('\(.*\)', "", title)
    print(title)
    

    summary = page.summary
    
    #summary = summary.replace(page.title, BLANK_SPACE)

    summary = remove_subject(title, summary)
    print(summary)

generate_question()

