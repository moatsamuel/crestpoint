from flask import Blueprint,render_template,request,redirect,url_for,flash,session
# from pkg import app
from pkg.models import db, Doctor, Specialty, Patient, Appointment,User
from werkzeug.security import check_password_hash, generate_password_hash

admin = Blueprint('admin',__name__,template_folder='templates',static_folder='static')

@admin.route("/dashboard")
def admin_home():
    if session.get('role') == 'admin':
        return render_template("admin/dashboard.html")
    return redirect(url_for("main.login"))
    
@admin.route("/patients")
def admin_patients():
    patients_list = Patient.query.order_by(Patient.id.desc()).all()
    total_patients = len(patients_list)
    return render_template("admin/patients.html", patients=patients_list, total_patients=total_patients)

@admin.route("/appointments")
def appointments():
    appointments_list = Appointment.query.order_by(Appointment.id.desc()).all()
    total_appointments = len(appointments_list)
    return render_template("admin/appointments.html", appointments=appointments_list, total_appointments=total_appointments)

@admin.route("/doctors")
def admin_doctors():
    
    if session.get('role') == 'admin':
        session.clear()
        # if not session.get("admin_online"):          # adjust to your admin login
        #     return redirect(url_for("admin.admin_login"))

        doctors_list = Doctor.query.order_by(Doctor.id.desc()).all()
        specialties_list = Specialty.query.order_by(Specialty.name.asc()).all()

        total_doctors = len(doctors_list)
        available_doctors = sum(
            1 for d in doctors_list
            if (d.availability or "").strip().lower() == "available"
        )

        return render_template(
            "admin/admin_doctors.html",
            doctors=doctors_list,
            specialties=specialties_list,
            total_doctors=total_doctors,
            available_doctors=available_doctors,
            unavailable_doctors=total_doctors - available_doctors,
            specialties_count=len(specialties_list),
        )
    return redirect(url_for('main.login'))
@admin.route("/admin/doctor/add", methods=["POST","GET"])
def admin_add_doctor():
    if request.method == 'POST':
        first_name = request.form.get("first_name", "").strip()
        last_name = request.form.get("last_name", "").strip()
        email = request.form.get("email", "").strip()
        phone = request.form.get("phone", "").strip()
        specialty_id = request.form.get("specialty_id")
        availability = request.form.get("availability", "available")
        license_no = request.form.get("license_no", "").strip()
        # temp_password = secrets.token_hex(5)
        password = license_no  # Using license number as password for simplicity; consider hashing in production
        password_hash = generate_password_hash(password)

        if not all([first_name, last_name, email, phone, specialty_id, license_no]):
            flash("Please fill in all required fields.", "danger")
            return redirect(url_for("admin.admin_doctors"))

        if Doctor.query.filter_by(email=email).first():
            flash(f"A doctor with email '{email}' already exists.", "danger")
            return redirect(url_for("admin.admin_doctors"))

        try:
            new_doctor = Doctor(
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=phone,
                specialty_id=int(specialty_id),
                availability=availability,
                license_no=license_no,
                password=password_hash
            )
            user_doc = User(email=email,password=password_hash,role='doctor')
            db.session.add(new_doctor)
            db.session.add(user_doc)
            db.session.commit()
            flash(f"Dr. {first_name} {last_name} has been added successfully!", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"Error adding doctor: {str(e)}", "danger")

        return redirect(url_for("admin.admin_doctors"))
    return redirect(url_for("admin.admin_doctors"))

@admin.route("/admin/doctor/update/<int:id>", methods=["POST"])
def admin_update_doctor(id):
    doctor = User.query.get_or_404(id)

    first_name = request.form.get("first_name", "").strip()
    last_name = request.form.get("last_name", "").strip()
    email = request.form.get("email", "").strip()
    phone = request.form.get("phone", "").strip()
    specialty_id = request.form.get("specialty_id")
    availability = request.form.get("availability", "available")
    license_no = request.form.get("license_no", "").strip()

    if not all([first_name, last_name, email, phone, specialty_id, license_no]):
        flash("Please fill in all required fields.", "danger")
        return redirect(url_for("admin.admin_doctors"))

    # Check duplicate email
    existing = User.query.filter(User.email == email, User.id != id).first()
    if existing:
        flash(f"The email '{email}' is already in use by another doctor.", "danger")
        return redirect(url_for("admin.admin_doctors"))

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

    return redirect(url_for("admin.admin_doctors"))

@admin.route("/admin/doctor/delete/<int:id>", methods=["POST"])
def admin_delete_doctor(id):
    doctor = User.query.get_or_404(id)
    doc_name = f"Dr. {doctor.first_name} {doctor.last_name}"

    try:
        db.session.delete(doctor)
        db.session.commit()
        flash(f"{doc_name} has been deleted successfully.", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error deleting doctor: {str(e)}", "danger")

    return redirect(url_for("admin.admin_doctors"))

