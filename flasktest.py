from flask import Flask, render_template, redirect, url_for, request
from functions import create_daily, list
from Snippets import create_message
from Settings import update_settings, getAPINinjasKey

app = Flask(__name__)


@app.route("/", methods=["POST", "GET"])
def home():

    if request.method == "POST":
        message, sender = request.form["message"], request.form["sender"]
        create_message(message, sender).show()

    return render_template("index.html", key=getAPINinjasKey())

@app.route("/settings", methods=["POST", "GET"])
def settings():

    if request.method == "POST":
        enableList = ["jokeEnable", "factEnable", "quoteEnable", "imageEnable", "historyEnable", "dogEnable"]
        settings_dict = {el:(True if request.form.get(el) == "on" else False) for el in enableList}
        settings_dict.update({"APINinjasKey":request.form.get("APINinjasKey"), "prefList":request.form.get("prefList")})
        update_settings(settings_dict)

    return redirect(url_for("home"))


@app.route("/print_overview")
def print_overview():
    create_daily().show()
    return redirect(url_for("home"))


@app.route("/print_list")
def print_list():
    list().show()
    return redirect(url_for("home"))

app.run(port=5001)