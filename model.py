from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#what do i need fstring for in the return???

class Patient(db.Model):
    """Data model for patients"""
    __tablename__ = "patients"

    patient_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    phone = db.Column(db.String(30), nullable=True)
    address = db.Column(db.String(30), nullable=True)
    #add lat long floats
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(20), nullable=True)

    appointments = db.relationship("Appointment", back_populates="patient")
    patientfeelings = db.relationship("PatientFeelings", back_populates="patient")

    def __repr__(self):
        return f"<Patient first_name={self.first_name} last_name={self.last_name} email={self.email}"

class Doctor(db.Model):
    """Data model for doctors"""
    __tablename__ = "doctors"

    doctor_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    address = db.Column(db.String(30), nullable=True)
    #add lat long floats
    phone = db.Column(db.String(30), nullable=True)
    photo_url = db.Column(db.String(100), nullable=True)
    bio = db.Column(db.Text , nullable=True)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(20), nullable=True)

    appointments = db.relationship("Appointment", back_populates="doctor")
    doctorspecialties = db.relationship("DoctorSpecialties", back_populates="doctor")
    doctoravailability = db.relationship("DoctorAvailabilities", back_populates="doctor")
    doctorinsurances = db.relationship("DoctorInsurances", back_populates="doctor")

    def __repr__(self):
        return f"<Doctor first_name={self.first_name} last_name={self.last_name} email={self.email}>"

1
class Appointment(db.Model):
    """Data model for appointments"""
    __tablename__ = "appointments"

    appointment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey("doctors.doctor_id"),nullable=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("patients.patient_id"),nullable=True)
    date = db.Column(db.DateTime , nullable=False)

    patient = db.relationship("Patient" , back_populates="appointments")
    doctor = db.relationship("Doctor" , back_populates="appointments")
    def __repr__(self):
        return f"<Appointment date={self.date}>"

class PatientFeelings(db.Model):
    """Data model for patient feelings"""
    __tablename__ = "patient_feelings"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("patients.patient_id"),nullable=True)
    # do i need to autoincrement when patient rate their feeling?
    feeling_rating = db.Column(db.Integer, autoincrement=False)
    feeling_comment = db.Column(db.Text , nullable=True)
    date = db.Column(db.DateTime , nullable=False)
#do i callthis patient_id or patient????

    patient = db.relationship("Patient", back_populates="patientfeelings")

    def __repr__(self):
        return f"<PatientFeeling feeling_rating={self.feeling_rating} date={self.date}>"

class DoctorSpecialties(db.Model):
    """Connects specialties to doctors table"""
    __tablename__ = "doctor_specialties"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    specialty_name = db.Column(db.String(30), db.ForeignKey("specialties.specialty_name"), nullable=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey("doctors.doctor_id"),nullable=True)

    doctor = db.relationship("Doctor", back_populates="doctorspecialties")
    specialty = db.relationship("Specialties", back_populates="doctorspecialties")

    def __repr__(self):
        return f"<DoctorSpecialties id={self.id}>"

class Specialties(db.Model):
    """Data model for Docto's Specialties"""
    __tablename__ = "specialties"

    specialty_name = db.Column(db.String(30), primary_key=True, nullable=False)

    doctorspecialties = db.relationship("DoctorSpecialties", back_populates="specialty")

    def __repr__(self):
        return f"<Specialties specialty_name={self.specialty_name}>"

class DoctorInsurances(db.Model):
    """Connects specialties to doctors table"""
    __tablename__ = "doctor_insurances"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    insurance_name = db.Column(db.String(30), nullable=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey("doctors.doctor_id"),nullable=True)

    doctor = db.relationship("Doctor", back_populates="doctorinsurances")

    def __repr__(self):
        return f"<DoctorSpecialties id={self.id}>"


class DoctorAvailabilities(db.Model):

    __tablename__ = "doctor_availability"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey("doctors.doctor_id"),nullable=True)
    date = db.Column(db.DateTime , nullable=False)

    doctor = db.relationship("Doctor", back_populates="doctoravailability")

    def __repr__(self):
        return f"<DoctorAvailabilities date={self.date}>"




def connect_to_db(app):
    """Connect the database to our Flask app."""

    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///catherapy"
    app.config["SQLALCHEMY_ECHO"] = False
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    print("Connected to db!")


if __name__ == "__main__":
    from flask import Flask

    app = Flask(__name__)
    connect_to_db(app)
