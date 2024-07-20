from flask import Flask, render_template, redirect, url_for, request
from Prints import create_daily, create_tasklist
from Snippets import create_message
from Settings import update_settings, read_settings
from Google import get_tasklists

app = Flask(__name__)


@app.route("/", methods=["POST", "GET"])
def home():

    if request.method == "POST":
        message, sender = request.form["message"], request.form["sender"]
        create_message(message, sender).show()

    return render_template("index.html", set=read_settings(), tasklist=get_tasklists())


@app.route("/settings", methods=["POST", "GET"])
def settings():

    if request.method == "POST":
        enableList = ["jokeEnable", "factEnable", "quoteEnable", "imageEnable", "historyEnable", "dogEnable"]
        settings_dict = {"triviaList": [el for el in enableList if request.form.get(el) == "on"]}
        settings_dict.update({"APINinjasKey": request.form.get("APINinjasKey"), "prefList": request.form.get("prefList")})
        update_settings(settings_dict)

    return redirect(url_for("home"))


@app.route("/print_overview")
def print_overview():
    create_daily().show()
    return redirect(url_for("home"))


@app.route("/print_list")
def print_list():
    create_tasklist().show()
    return redirect(url_for("home"))


app.run(port=5002)
