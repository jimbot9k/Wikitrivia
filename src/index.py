from flask import Flask, request, render_template, Blueprint, render_template, redirect, url_for, request, flash, make_response
import sqlite3
from flask_assets import Environment
from flask_socketio import SocketIO, emit, join_room, send

app = Flask(__name__)
socketio = SocketIO(app)
assets = Environment(app)

# Main home page
@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template("index.html")    
    else:
        playerName = request.form['name']
        if ((request.form['type']) == 'Join'):
            resp = make_response(render_template("play.html", playerName = playerName))
        elif ((request.form['type']) == 'Create'):
            resp = make_response(render_template("create.html", playerName = playerName))
        resp.set_cookie('playerName', playerName)
        return resp


# Create lobby page
@app.route("/create", methods=['GET', 'POST'])
def create():
    playerName = request.cookies.get('playerName')
    if request.method == 'GET':
        return render_template("create.html", playerName=playerName)
    else:
        if ((request.form['type']) == 'Host'):
            return render_template("play.html")
        elif ((request.form['type']) == 'Solo'):
            return render_template("play.html")      

# Play game page
@app.route("/play", methods=['GET', 'POST'])
def play():
    if request.method == 'GET':
        return render_template("play.html")
    if request.method == 'POST':
        pass

if __name__ == '__main__':
    socketio.run(app, debug=True)
