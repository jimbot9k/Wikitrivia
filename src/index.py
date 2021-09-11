from flask import Flask, request, render_template, Blueprint, render_template, redirect, url_for, request, flash, make_response
import sqlite3
from flask_assets import Environment
from flask_socketio import SocketIO, emit, join_room, send

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
assets = Environment(app)

# Main home page
@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template("index.html")    
    else:
        type = request.form['type']
        playerName = request.form['name']
        roomID = request.form['room']
        if (type == 'Join'):
            resp = make_response(render_template("play.html", playerName = playerName))
        elif (type == 'Create'):
            resp = make_response(render_template("play.html", playerName = playerName))
        resp.set_cookie('roomID', roomID)
        resp.set_cookie('playerName', playerName)
        resp.set_cookie('type', type)
        return resp     

# Play game page
@app.route("/play", methods=['GET', 'POST'])
def play():
    if request.method == 'GET':
        return render_template("play.html")
    if request.method == 'POST':
        pass

@socketio.on("connect")
def on_connect():
    print("connection attempted.")

@socketio.on('createRoom')
def create_room(json):
    print(str(json))
    send(str(json))

@socketio.on('joinGame')
def join_game(json):
    print(json['roomID'])
    print(json['playerName'])
    print("done")
    send(str(json))


if __name__ == '__main__':
    socketio.run(app, debug=True)
