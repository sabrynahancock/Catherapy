from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#what do i need fstring for in the return???

class Patient(db.Model):
    """Data model for patients"""
    __tablename__ = "patients"

    patient_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(30))
    last_name = db.Column(db.String(30))
    phone = db.Column(db.String(30))
    address = db.Column(db.String(100))
    #add lat long floats
    lat = db.Column(db.Float, nullable=True)
    long = db.Column(db.Float, nullable=True)
    email = db.Column(db.String(50))
    password = db.Column(db.String(20))

    appointments = db.relationship("Appointment", back_populates="patient")
    patientfeelings = db.relationship("PatientFeeling", back_populates="patient")

    def __repr__(self):
        return f"<Patient first_name={self.first_name} last_name={self.last_name} email={self.email}"

class Doctor(db.Model):
    """Data model for doctors"""
    __tablename__ = "doctors"

    doctor_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(30))
    last_name = db.Column(db.String(30))
    address = db.Column(db.String(100))
    #add lat long floats
    lat = db.Column(db.Float, nullable=True)
    long = db.Column(db.Float, nullable=True)
    phone = db.Column(db.String(30))
    photo_url = db.Column(db.String(100))
    bio = db.Column(db.Text)
    email = db.Column(db.String(50))
    password = db.Column(db.String(20))

    appointments = db.relationship("Appointment", back_populates="doctor")
    doctorspecialties = db.relationship("DoctorSpecialty", back_populates="doctor")
    doctoravailabilities = db.relationship("DoctorAvailability", back_populates="doctor")
    doctorinsurances = db.relationship("DoctorInsurance", back_populates="doctor")

    def __repr__(self):
        return f"<Doctor first_name={self.first_name} last_name={self.last_name} email={self.email}>"


class Appointment(db.Model):
    """Data model for appointments"""
    __tablename__ = "appointments"

    appointment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey("doctors.doctor_id"),nullable=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("patients.patient_id"),nullable=True)
    datetime = db.Column(db.DateTime , nullable=False)

    patient = db.relationship("Patient" , back_populates="appointments")
    doctor = db.relationship("Doctor" , back_populates="appointments")
    def __repr__(self):
        return f"<Appointment date={self.date}>"

class PatientFeeling(db.Model):
    """Data model for patient feelings"""
    __tablename__ = "patient_feelings"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("patients.patient_id"),nullable=True)
    feeling_rating = db.Column(db.Integer)
    feeling_comment = db.Column(db.Text)
    datetime = db.Column(db.DateTime)


    patient = db.relationship("Patient", back_populates="patientfeelings")

    def __repr__(self):
        return f"<PatientFeeling feeling_rating={self.feeling_rating} date={self.date}>"

class DoctorSpecialty(db.Model):
    """Connects specialties to doctors table"""
    __tablename__ = "doctor_specialties"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    specialty_name = db.Column(db.String(30), db.ForeignKey("specialties.specialty_name"), nullable=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey("doctors.doctor_id"),nullable=True)

    doctor = db.relationship("Doctor", back_populates="doctorspecialties")
    specialty = db.relationship("Specialty", back_populates="doctorspecialties")

    def __repr__(self):
        return f"<DoctorSpecialty id={self.id}>"

class Specialty(db.Model):
    """Data model for Doctor's Specialties"""
    __tablename__ = "specialties"

    specialty_name = db.Column(db.String(30), primary_key=True)

    doctorspecialties = db.relationship("DoctorSpecialty", back_populates="specialty")

    def __repr__(self):
        return f"<Specialty specialty_name={self.specialty_name}>"

class DoctorInsurance(db.Model):
    """Connects specialties to doctors table"""
    __tablename__ = "doctor_insurances"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    insurance_name = db.Column(db.String(30), nullable=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey("doctors.doctor_id"))

    doctor = db.relationship("Doctor", back_populates="doctorinsurances")

    def __repr__(self):
        return f"<DoctorInsurance id={self.id}>"


class DoctorAvailability(db.Model):

    __tablename__ = "doctor_availabilities"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey("doctors.doctor_id"))
    datetime = db.Column(db.DateTime , nullable=False)

    doctor = db.relationship("Doctor", back_populates="doctoravailabilities")

    def __repr__(self):
        return f"<DoctorAvailability date={self.date}>"




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
    
