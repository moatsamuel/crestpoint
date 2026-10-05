from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Specialty(db.Model):
    __tablename__ = "specialties"
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String(100),nullable=False,unique=True)
    description = db.Column(db.String(100),nullable=False)
    created_at = db.Column(db.DateTime,default=datetime.utcnow)
    doctors = db.relationship('Doctor',backref = 'specialties',cascade='all,delete-orphan')
    
    def __repr__(self):
        return f'{self.name}'
    
class Doctor(db.Model):
    __tablename__ = "doctors"
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    first_name = db.Column(db.String(100),nullable=False)
    last_name = db.Column(db.String(100),nullable=False)
    email = db.Column(db.String(100),nullable=False,unique=True)
    phone = db.Column(db.String(100),nullable=False)
    specialty_id = db.Column(db.Integer,db.ForeignKey('specialties.id'))
    availability = db.Column(db.Enum('available','unavailable'),default='available')
    license_no = db.Column(db.String(100),nullable=False)
    created_at = db.Column(db.DateTime,default=datetime.utcnow)
    appointments = db.relationship('Appointment',uselist = False,backref = 'doctors',cascade='all,delete-orphan')
    def __repr__(self):
        return f'{self.id}'
    
    
class Appointment(db.Model):
    __tablename__ = "appointments"
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'))
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'))
    appointment_date = db.Column(db.DateTime)
    appointment_time = db.Column(db.DateTime)
    reason = db.Column(db.Text)
    status = db.Column(db.Enum('Pending','Accepted','Rejected','Cancelled','Completed'), default='Pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    
class Patient(db.Model):
    __tablename__ = "patients"
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    first_name = db.Column(db.String(100),nullable=False)
    last_name = db.Column(db.String(100),nullable=False)
    email = db.Column(db.String(100),nullable=False,unique=True)
    phone = db.Column(db.String(100),nullable=False)
    dob = db.Column(db.DateTime)
    address = db.Column(db.Text)
    password = db.Column(db.String(255),nullable=False)
    appointments = db.relationship('Appointment',backref = 'patients',cascade='all,delete-orphan')
    
    def __repr__(self):
        return f'{self.id}'