from flask import Flask, render_template, redirect, url_for
from functions import create_daily, list

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/print_overview")
def print_overview():
    create_daily().show()
    return redirect(url_for("home"))

@app.route("/print_list")
def print_list():
    list().show()
    return redirect(url_for("home"))

app.run(port=5001)