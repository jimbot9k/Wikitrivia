from flask import Flask, request, render_template, Blueprint, render_template, redirect, url_for, request, flash
import sqlite3

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template("index.html")

@app.route("/create", methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
        return render_template("create.html")

@app.route("/join", methods=['GET', 'POST'])
def join():
    if request.method == 'GET':
        return render_template("join.html")

@app.route("/play", methods=['GET', 'POST'])
def play():
    if request.method == 'GET':
        return render_template("play.html")

if __name__ == '__main__':
    app.run()