import cs50
import csv

from flask import Flask, jsonify, redirect, render_template, request

# Configure application
app = Flask(__name__)

# Reload templates when they are changed
app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.after_request
def after_request(response):
    """Disable caching"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET"])
def get_index():
    return redirect("/form")


@app.route("/form", methods=["GET"])
def get_form():
    return render_template("form.html")


@app.route("/form", methods=["POST"])
def post_form():
    if not request.form.get("Name") or not request.form.get("Email") or not request.form.get("Select") or not request.form.get("Radio"):
        return render_template("error.html", message="One or more of the input fields was empty")
    else:
        name = request.form['Name']
        email = request.form['Email']
        age = request.form['Select']
        interest = request.form['Radio']

    with open('survey.csv', 'a') as file:
        entrywriter = csv.writer(file)
        entrywriter.writerow([name, email, age, interest])
    return redirect("/sheet")


@app.route("/sheet", methods=["GET"])
def get_sheet():
    with open('survey.csv', 'r') as file:
        reader = csv.reader(file)
        registered = list(reader)
    return render_template("sheet.html", registered=registered)
