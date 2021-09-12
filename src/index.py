from flask import Flask, request, render_template, Blueprint, render_template, redirect, url_for, request, flash, make_response
import sqlite3
from flask_assets import Environment
from flask_socketio import SocketIO, emit, join_room, send
from game import Game
import json as JSON

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
assets = Environment(app)

games = {}

# Main home page
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html")    
    else:
        type = request.form["type"]
        playerName = request.form["name"]
        roomID = request.form["room"]
        if (type == "Join"):
            resp = make_response(render_template("play.html", playerName = playerName))
        elif (type == "Create"):
            resp = make_response(render_template("host.html", playerName = playerName))
        resp.set_cookie("roomID", roomID)
        resp.set_cookie("playerName", playerName)
        resp.set_cookie("type", type)
        return resp     

# Play game page
@app.route("/play", methods=["GET", "POST"])
def play():
    if request.method == "GET":
        resp = make_response(render_template("play.html"))
        resp.set_cookie("type", "Join")
        return resp     

    if request.method == "POST":
        pass

@socketio.on("connect")
def on_connect():
    print("connection attempted.")

@socketio.on("createGame")
def create_game(json):
    host = json["playerName"]
    players = {}
    players[host] = 0
    roomID = json["roomID"]
    join_room(roomID)
    games[roomID] = Game(roomID, host, players)
    join_room(roomID)
    print("Game Created:{roomID}".format(roomID=roomID))
    msg = {}
    msg["players"] = games[roomID].get_player_list()
    emit('updatePlayers', JSON.dumps(msg), to=roomID)
    msg = {}
    msg["question"] = games[roomID].get_question().get_question()
    for answer in games[roomID].get_answers():
        msg["answer{i}".format(i=answer)] = games[roomID].get_answers()[answer]
    emit('updateQuestion', JSON.dumps(msg), to=roomID)

@socketio.on('message')
def handle_message(data):
    print('received message: ' + data)


@socketio.on("joinGame")
def join_game(json):
    roomID = json["roomID"]
    playerName = json["playerName"]
    msg = {}
    games[roomID].add_player(playerName)
    msg["players"] = games[roomID].get_player_list()
    join_room(roomID)
    emit('updatePlayers', JSON.dumps(msg), to=roomID)
    msg = {}
    msg["question"] = games[roomID].get_question().get_question()
    for answer in games[roomID].get_answers():
        msg["answer{i}".format(i=answer)] = games[roomID].get_answers()[answer]
    emit('updateQuestion', JSON.dumps(msg), to=roomID)

@socketio.on("getPlayers")
def getPlayers(json):
    roomID = json["roomID"]
    msg = {}
    if not games[roomID] == None:
        msg["players"] = games[roomID].get_player_list()
        emit('updatePlayers', JSON.dumps(msg), to=roomID)

@socketio.on("getQuestion")
def getQuestion(json):
    print(json["roomID"])
    print(json["playerName"])

@socketio.on("sendAnswer")
def sendAnswer(json):
    roomID = json["roomID"]
    playerName = json["playerName"]
    answer = json["answer"]
    if not games[roomID] == None:
        games[roomID].answer_question(playerName, answer)

@socketio.on("endRound")
def endRound(json):
    roomID = json["roomID"]
    questionSet = json["questionSet"]
    print(questionSet)
    if not games[roomID] == None:
        games[roomID].end_round(questionSet)
        msg = {}
        msg["players"] = games[roomID].get_player_list()
        emit('updatePlayers', JSON.dumps(msg), to=roomID)
        msg = {}
        msg["question"] = games[roomID].get_question().get_question()
        for answer in games[roomID].get_answers():
            msg["answer{i}".format(i=answer)] = games[roomID].get_answers()[answer]
        msg["previousAnswer"] = games[roomID].get_question().get_answer()
        emit('updateQuestion', JSON.dumps(msg), to=roomID)





if __name__ == "__main__":
    socketio.run(app, debug=True)
