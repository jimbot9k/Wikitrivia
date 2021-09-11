from flask import Flask, request, render_template, Blueprint, render_template, redirect, url_for, request, flash
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
            return render_template("join.html", playerName = playerName)
        elif ((request.form['type']) == 'Create'):
            return render_template("create.html", playerName = playerName)


# Create lobby page
@app.route("/create", methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
        return render_template("create.html")
    else:
        if ((request.form['type']) == 'Host'):
            return render_template("createWait.html")
        elif ((request.form['type']) == 'Solo'):
            return render_template("solo.html")

# Join game page
@app.route("/join", methods=['GET', 'POST'])
def join():
    if request.method == 'GET':
        return render_template("join.html")
    else:
        print(request.form)
        return render_template("joinWait.html", roomID = request.form['room'])

# Play game page
@app.route("/play", methods=['GET', 'POST'])
def play():
    if request.method == 'GET':
        return render_template("play.html")
    if request.method == 'POST':
        return redirect(url_for('create'))

# Play solo page
@app.route("/solo", methods=['GET', 'POST'])
def solo():
    if request.method == 'GET':
        return render_template("solo.html")
    

# Joining wait for host page
@app.route("/joinWait", methods=['GET', 'POST'])
def joinWait():
    if request.method == 'GET':
        return render_template("joinWait.html")
#  Hosting waiting for players page
@app.route("/hostWait", methods=['GET', 'POST'])
def hostWait():
    if request.method == 'GET':
        return render_template("hostWait.html")

if __name__ == '__main__':
    socketio.run(app, debug=True)
