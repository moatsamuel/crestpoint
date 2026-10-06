from flask import Blueprint,render_template,request,redirect,url_for
# from pkg import app
from pkg.models import db, Doctor, Specialty, Patient, Appointment,User
from werkzeug.security import check_password_hash, generate_password_hash
import re



patients = Blueprint('patients',__name__,template_folder='templates',static_folder='static')

@patients.route("/")
def patients_home():
    return render_template('main.main/index.html')

@patients.route("/appointments" ,methods=['GET','POST'])
def appointment():
    if request.method == "POST":
        first_name = request.form.get('first_name').strip()
        last_name = request.form.get('last_name').strip()
        # email = request.form.get('email')
        doctor = request.form.get('doctor')
        splitname = doctor.split('.')
        name = splitname[1]
        namesplit = name.split(' ')
        date = request.form.get('date')
        time = request.form.get('time')
        notes = request.form.get('notes')
        pat = Patient.query.filter(Patient.first_name == first_name, Patient.last_name== last_name ).first()
        print(pat)
        docid = Doctor.query.filter(Doctor.first_name == namesplit[1], Doctor.last_name== namesplit[2] ).first()
        print(docid)
        appoint = Appointment(patient_id=pat.id,doctor_id=docid.id,appointment_date=date,appointment_time=time,reason=notes)
        db.session.add(appoint)
        db.session.commit()
    spec = Specialty.query.all()
    doc = Doctor.query.all()   
    return render_template('patients/appointments.html',s=spec,d=doc)

@patients.route('/patients')
def patient():
    first_name = input("Enter FirstName: ")
    last_name = input("Enter LastName: ")
    email = input("Enter Email: ")
    phone = input("Enter PhoneNo: ")
    address = input("Address: ")
    patient = Patient(first_name=first_name,last_name=last_name,email=email,phone=phone,address=address)
    db.session.add(patient)
    db.session.commit()
    return 'Patient Added'

@patients.route('/signup' , methods = ['GET','POST'])
def signup():
    if request.method != 'POST':
        return render_template("patients/signup.html", signup_error=None)

    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    address = request.form.get('address')
    password = request.form.get('password', '')
    confirm_password = request.form.get('confirm_password', '')

    if not re.search(r'[A-Z]', password) or not re.search(r'[^A-Za-z0-9\s]', password):
        return render_template(
            "patients/signup.html",
            signup_error="Password must contain at least one uppercase letter and one special character."
        )

    if password != confirm_password:
        return render_template("patients/signup.html", signup_error="Passwords do not match.")

    password_hash = generate_password_hash(password)
    patient = Patient(first_name=first_name, last_name=last_name, email=email, phone=phone,
                      address=address, password=password_hash)
    user = User(email=email, password=password_hash, role='patient')
    db.session.add(patient)
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('main.login'))