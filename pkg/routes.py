from flask import render_template, request, redirect, url_for, flash
from pkg import app
from pkg.models import db, Doctor, Specialty

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/contact")
def about():
    return render_template("contact.html")

@app.route("/doctors")
def doctors():
    doctor = db.session.query(Doctor).outerjoin(Doctor.specialties).all()
    return render_template("doctors.html", d=doctor)

@app.route("/specialties")
def specialties():
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

