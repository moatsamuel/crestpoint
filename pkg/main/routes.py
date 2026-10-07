from flask import Blueprint,render_template,request,redirect,url_for,session
# from pkg import app
from pkg.models import db, Doctor, Specialty, Patient, Appointment,User
from werkzeug.security import check_password_hash, generate_password_hash



main = Blueprint('main',__name__,template_folder='templates',static_folder='static')

@main.route("/")
def index():
    doctor = db.session.query(Doctor).outerjoin(Doctor.specialties).all()
    specialty = db.session.query(Specialty).all()
    return render_template("main/index.html",d = doctor,s=specialty)

@main.route("/contact")
def about():
    return render_template("main/contact.html")

@main.route("/doctors")
def doctors():
    # doctors = [{"name":"Dr David","special":"Surgeon","availability":"Available"},
    #            {"name":"Dr David Ani","special":"Dentist","availability":"Available"},
    #            {"name":"Dr Hassan","special":"Dermatology","availability":"Available"}]
    # doctor = db.session.query(Doctor).all()
    # doctor = db.session.query(Doctor).join(Doctor.specialties).all()
    doctor = db.session.query(Doctor).outerjoin(Doctor.specialties).all()
    return render_template("main/doctors.html", d=doctor)

@main.route("/specialties")
def specialties():
    # doctors = [{"name":"Dr David","special":"Surgeon","availability":"Available"},
    #            {"name":"Dr David Ani","special":"Dentist","availability":"Available"},
    #            {"name":"Dr Hassan","special":"Dermatology","availability":"Available"}]
    # spec = db.session.query(Specialty).all()
    spec = Specialty.query.all()
    return render_template("main/specialties.html", s=spec)

@main.route("/login/" , methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email').strip()
        password = request.form.get('password')
        role = request.form.get('role')
        if not email or not password:
            return redirect(url_for('login'))

        user = User.query.filter_by(email=email, role=role).first()
        if user and check_password_hash(user.password, password):
            session.clear()
            # session['useronline'] = user.id
            if role == 'doctor':
                session["role"] = "doctor"
                return redirect(url_for('doctors.doctors_dashboard'))
            if role == 'patient':
                session["role"] = "patient"
                return redirect(url_for('patients.patients_home'))
            if role == 'admin':
                session["role"] = "admin"
                return redirect(url_for('admin.admin_home'))
            return redirect(url_for('main.index'))

    #return redirect(url_for('main.login'))
    return render_template('main/login.html')

@main.post('/logout/')
def logout():
    if session.get('useronline') != None:
        session.pop('useronline',None)
        session.clear()
        return redirect(url_for('main.login'))
    return redirect(url_for('main.login'))
