from flask import Blueprint,render_template,request,redirect,url_for,session

doctors = Blueprint('doctors',__name__,template_folder='templates',static_folder='static')

@doctors.route("/")
def doctors_dashboard():
    if session.get('role') == 'doctor':
        return render_template('doctor/dashboard.html')
    return redirect(url_for('main.login'))

