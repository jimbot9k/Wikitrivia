from flask import Flask, request, render_template, Blueprint, render_template, redirect, url_for, request, flash
import sqlite3

app = Flask(__name__)

# Main home page
@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template("index.html")

# Create lobby page
@app.route("/create", methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
        return render_template("create.html")

# Join game page
@app.route("/join", methods=['GET', 'POST'])
def join():
    if request.method == 'GET':
        return render_template("join.html")

# Play game page
@app.route("/play", methods=['GET', 'POST'])
def play():
    if request.method == 'GET':
        return render_template("play.html")

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
    app.run()