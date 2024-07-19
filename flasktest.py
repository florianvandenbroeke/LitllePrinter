from flask import Flask, render_template, redirect, url_for, request
from functions import create_daily, list
from Snippets import create_message

app = Flask(__name__)


@app.route("/", methods=["POST", "GET"])
def home():

    if request.method == "POST":
        message, sender = request.form["message"], request.form["sender"]
        create_message(message, sender).show()

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