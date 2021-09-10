from flask import Flask, request, render_template, Blueprint, render_template, redirect, url_for, request, flash

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == '__main__':
    app.run()