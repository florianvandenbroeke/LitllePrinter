from flask import Flask, render_template, redirect, url_for, request
from Prints import print_daily, print_message, print_list, print_label
from Settings import update_settings, read_settings
from Google import get_tasklists
from GPIO import gpio
from multiprocessing import Process

app = Flask(__name__)


@app.route("/", methods=["POST", "GET"])
def home():

    if request.method == "POST":
        message, sender = request.form["message"], request.form["sender"]
        print_message(message, sender)

    return render_template("index.html", set=read_settings(), tasklist=get_tasklists())


@app.route("/settings", methods=["POST", "GET"])
def settings():

    if request.method == "POST":
        enableList = ["jokeEnable", "factEnable", "quoteEnable", "imageEnable", "historyEnable", "dogEnable"]
        settings_dict = {"triviaList": [el for el in enableList if request.form.get(el) == "on"]}
        debug_mode = True if request.form.get("debugMode") else False
        settings_dict.update({"APINinjasKey": request.form.get("APINinjasKey"), "prefList": request.form.get("prefList"), "debugMode": debug_mode})
        update_settings(settings_dict)

    return redirect(url_for("home"))

@app.route("/label", methods=["POST", "GET"])
def label():

    if request.method == "POST":
        label_text = request.form["label_text"]
        print_label(label_text)

    return redirect(url_for("home"))

@app.route("/print_overview")
def print_overview():
    print_daily()
    return redirect(url_for("home"))


@app.route("/print_list")
def print_tasklist():
    print_list()
    return redirect(url_for("home"))


p = Process(target=gpio)
p.start()

app.run(port=5005, host="192.168.50.123")
