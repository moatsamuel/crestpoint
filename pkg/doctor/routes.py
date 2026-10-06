from flask import Blueprint,render_template,request,redirect,url_for

doctors = Blueprint('doctors',__name__,template_folder='templates',static_folder='static')

@doctors.route("/")
def doctors_dashboard():
    return render_template('doctor/dashboard.html')

