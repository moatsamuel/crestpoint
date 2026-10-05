from flask import render_template, request, redirect, url_for, flash,session
from pkg import app
from pkg.models import db, Doctor, Specialty, Patient, Appointment
from werkzeug.security import check_password_hash, generate_password_hash


# @app.route('/createdoc')
# def createdoc():
#     first_name = input("Enter FirstName: ")
#     last_name = input("Enter LastName: ")
#     email = input("Enter Email: ")
#     phone = input("Enter Phone No: ")
#     specialty_id = input("Enter SpecialtyID: ")
#     availability = input("Availability: ")
#     license_no = input("Input Lincense No")
#     doctor = Doctor(first_name=first_name, last_name=last_name, email=email, phone=phone, specialty_id=specialty_id, availability=availability, license_no=license_no)
#     db.session.add(doctor)
#     db.session.commit()
#     # return redirect(url_for('doctors'))
#     return 'Added'

# @app.route('/createspec')
# def createspec():
#     name = input("Name: ")
#     description = input("Description: ")
#     spec = Specialty(name=name, description=description)
#     db.session.add(spec)
#     db.session.commit()
#     # return redirect(url_for('specialties'))
#     return 'Added'

@app.route("/")
def index():
    doctor = db.session.query(Doctor).outerjoin(Doctor.specialties).all()
    specialty = db.session.query(Specialty).all()
    return render_template("index.html",d = doctor,s=specialty)

@app.route("/contact")
def about():
    return render_template("contact.html")

@app.route("/doctors")
def doctors():
    # doctors = [{"name":"Dr David","special":"Surgeon","availability":"Available"},
    #            {"name":"Dr David Ani","special":"Dentist","availability":"Available"},
    #            {"name":"Dr Hassan","special":"Dermatology","availability":"Available"}]
    # doctor = db.session.query(Doctor).all()
    # doctor = db.session.query(Doctor).join(Doctor.specialties).all()
    doctor = db.session.query(Doctor).outerjoin(Doctor.specialties).all()
    return render_template("doctors.html", d=doctor)

@app.route("/specialties")
def specialties():
    # doctors = [{"name":"Dr David","special":"Surgeon","availability":"Available"},
    #            {"name":"Dr David Ani","special":"Dentist","availability":"Available"},
    #            {"name":"Dr Hassan","special":"Dermatology","availability":"Available"}]
    # spec = db.session.query(Specialty).all()
    spec = Specialty.query.all()
    return render_template("specialties.html", s=spec)

@app.route("/admin")
@app.route("/admin/doctors")
def admin_doctors():
    doctors_list = Doctor.query.order_by(Doctor.id.desc()).all()
    specialties_list = Specialty.query.order_by(Specialty.name.asc()).all()

    total_doctors = len(doctors_list)
    available_doctors = sum(1 for d in doctors_list if d.availability == 'available')
    unavailable_doctors = total_doctors - available_doctors
    specialties_count = len(specialties_list)

    return render_template(
        "admin_doctors.html",
        doctors=doctors_list,
        specialties=specialties_list,
        total_doctors=total_doctors,
        available_doctors=available_doctors,
        unavailable_doctors=unavailable_doctors,
        specialties_count=specialties_count
    )

@app.route("/admin/doctor/add", methods=["POST"])
def admin_add_doctor():
    first_name = request.form.get("first_name", "").strip()
    last_name = request.form.get("last_name", "").strip()
    email = request.form.get("email", "").strip()
    phone = request.form.get("phone", "").strip()
    specialty_id = request.form.get("specialty_id")
    availability = request.form.get("availability", "available")
    license_no = request.form.get("license_no", "").strip()

    if not all([first_name, last_name, email, phone, specialty_id, license_no]):
        flash("Please fill in all required fields.", "danger")
        return redirect(url_for("admin_doctors"))

    if Doctor.query.filter_by(email=email).first():
        flash(f"A doctor with email '{email}' already exists.", "danger")
        return redirect(url_for("admin_doctors"))

    try:
        new_doctor = Doctor(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            specialty_id=int(specialty_id),
            availability=availability,
            license_no=license_no
        )
        db.session.add(new_doctor)
        db.session.commit()
        flash(f"Dr. {first_name} {last_name} has been added successfully!", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error adding doctor: {str(e)}", "danger")

    return redirect(url_for("admin_doctors"))

@app.route("/admin/doctor/update/<int:id>", methods=["POST"])
def admin_update_doctor(id):
    doctor = Doctor.query.get_or_404(id)

    first_name = request.form.get("first_name", "").strip()
    last_name = request.form.get("last_name", "").strip()
    email = request.form.get("email", "").strip()
    phone = request.form.get("phone", "").strip()
    specialty_id = request.form.get("specialty_id")
    availability = request.form.get("availability", "available")
    license_no = request.form.get("license_no", "").strip()

    if not all([first_name, last_name, email, phone, specialty_id, license_no]):
        flash("Please fill in all required fields.", "danger")
        return redirect(url_for("admin_doctors"))

    # Check duplicate email
    existing = Doctor.query.filter(Doctor.email == email, Doctor.id != id).first()
    if existing:
        flash(f"The email '{email}' is already in use by another doctor.", "danger")
        return redirect(url_for("admin_doctors"))

    try:
        doctor.first_name = first_name
        doctor.last_name = last_name
        doctor.email = email
        doctor.phone = phone
        doctor.specialty_id = int(specialty_id)
        doctor.availability = availability
        doctor.license_no = license_no

        db.session.commit()
        flash(f"Dr. {first_name} {last_name}'s details were updated successfully!", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error updating doctor: {str(e)}", "danger")

    return redirect(url_for("admin_doctors"))

@app.route("/admin/doctor/delete/<int:id>", methods=["POST"])
def admin_delete_doctor(id):
    doctor = Doctor.query.get_or_404(id)
    doc_name = f"Dr. {doctor.first_name} {doctor.last_name}"

    try:
        db.session.delete(doctor)
        db.session.commit()
        flash(f"{doc_name} has been deleted successfully.", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error deleting doctor: {str(e)}", "danger")

    return redirect(url_for("admin_doctors"))

@app.route("/appointments" ,methods=['GET','POST'])
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
    return render_template('appointments.html',s=spec,d=doc)

@app.route('/patients')
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

@app.route('/signup' , methods = ['GET','POST'])
def signup():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        address = request.form.get('address')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        if password == confirm_password:
            password_hash = generate_password_hash(password)
            patient = Patient(first_name=first_name,last_name=last_name,email=email,phone=phone,address=address
                              ,password=password_hash)
            db.session.add(patient)
            db.session.commit()   
    return render_template("signup.html")


@app.route("/login/" , methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email').strip()
        password = request.form.get('password')
        if not email or not password:
            return redirect(url_for('login'))

        patient = Patient.query.filter_by(email=email).first()
        if patient and check_password_hash(patient.password, password):
            # session.clear()
            session['useronline'] = patient.id
            return redirect(url_for('index'))

        return redirect(url_for('login'))
    return render_template('login.html')

@app.post('/logout/')
def logout():
    if session.get('useronline') != None:
        session.pop('useronline',None)
        session.clear()
        return redirect(url_for('_login'))
