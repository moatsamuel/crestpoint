from flask import render_template,request
from pkg import app

doctors = [{"name":"Dr David","special":"Surgeon","availability":"Available"},
               {"name":"Dr David Ani","special":"Dentist","availability":"Available"},
               {"name":"Dr Hassan","special":"Dermatology","availability":"Available"}]
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/contact")
def about():
    return render_template("contact.html")

@app.route("/doctors")
def doctors():
    doctors = [{"name":"Dr David","special":"Surgeon","availability":"Available"},
               {"name":"Dr David Ani","special":"Dentist","availability":"Available"},
               {"name":"Dr Hassan","special":"Dermatology","availability":"Available"}]
    return render_template("doctors.html",d = doctors)

@app.route("/specialties")
def specialties():
    doctors = [{"name":"Dr David","special":"Surgeon","availability":"Available"},
               {"name":"Dr David Ani","special":"Dentist","availability":"Available"},
               {"name":"Dr Hassan","special":"Dermatology","availability":"Available"}]
    return render_template("specialties.html",d = doctors)
