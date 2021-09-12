# UQCS-Hackathon-2021 - An Automatic Trivia Question Generator

The aim of the project is to create and automatic trivia question gerator that uses data from wikipedia to generate random questions on demand. 

## Backend 

Python based code that uses the wikipedia python package to generate questions.

The user can choose to pull questions form a series of lists of wikipedia pages, from which a random page will be selected and a question will be generated from that page. The code will generate a series of wrong answers for the question and won't give the user a question unless it thinks that question is good enough (enough close answers and sufficient info). The available options for the lists are 

- "top annual" (most viewed pages annually on wikipedia)
- "weekly 5000" (5000 most viewed pages, updated weekly)
- "grossing films", top grossing films 
- "grossing animes", top grossing animes (WIP)
- "Top 100 Books"
- "Artists from the 10s", musical artist from the 2010's
- "random", a totally random page (WIP)

Passing any of these arguments to the generate_question() function will generate a question of the selected topic. 

Random and grossing animes are currently WIP due to the difficulty of generating appropriate wrong answers for the questions. 

## Frontend

I dunno James, you can put something here. 

James: yeah flask lol. HTML templates. SocketIO to update game state.

## Setup
pip install -r pip.txt or run in pipenv to start server.
Connect to server in a browser (cookies enabled), put in name and roomID, then click create.
Once room has started and the first question has loaded, users can join by entering a name and roomID, then clicking join.
Dark Souls Mode does not work.

