"""CRUD operations."""

from model import db, Patient, Doctor, Appointment, PatientFeeling, DoctorSpecialty, DoctorInsurance, DoctorAvailability, connect_to_db
from geopy.geocoders import Nominatim


# add docstrigns on each function 

def create_patient(first_name, last_name, phone, address, email, password):
    """Creates a Patient"""
    lat_long = get_lat_long(address)
    lat = lat_long[0]
    long = lat_long[1]
    patient = Patient(first_name=first_name, last_name=last_name, phone=phone,
                      address=address, lat=lat, long=long, email=email, password=password)

    return patient


def get_patient_by_email(email):
    """Get patient by email"""
    return Patient.query.filter(Patient.email == email).first()


def create_doctor(first_name, last_name, address, phone, photo_url, bio, email, password, gender):
    """Creates a doctor"""
    lat_long = get_lat_long(address)
    lat = lat_long[0]
    long = lat_long[1]
    doctor = Doctor(first_name=first_name, last_name=last_name,
                    address=address, lat=lat, long=long, phone=phone, photo_url=photo_url, bio=bio, email=email, password=password, gender=gender)

    return doctor


def get_doctor_by_email(email):
    """Get a doctor by email"""
    return Doctor.query.filter(Doctor.email == email).first()


def get_doctor_availability(date):
    return DoctorAvailability.query.filter(DoctorAvailability.date == date).first()


def get_lat_long(address):

    geolocator = Nominatim(user_agent="catherapy")
    location = geolocator.geocode(address)



    return (location.raw['lat'], location.raw['lon'])


def create_doctor_availability(doctor, datetime):

    doctoravailability = DoctorAvailability(doctor=doctor, datetime=datetime)
    return doctoravailability


def create_doctor_insurance(doctor, insurance_name):

    return DoctorInsurance(doctor=doctor, insurance_name=insurance_name)


def create_doctor_specialty(doctor, specialty_name):

    return DoctorSpecialty(doctor=doctor, specialty_name=specialty_name)


def get_doctor_with_criteria(specialties, insurance):

    matching_doctors = set()
    all_doctors = Doctor.query.all()

    doctors_with_selected_insurance = set()

    for doctor in all_doctors:

        for doctor_insurance in doctor.doctorinsurances:
            if doctor_insurance.insurance_name == insurance:
                doctors_with_selected_insurance.add(doctor)

    for doctor in doctors_with_selected_insurance:
        doctors_specialty_names = set()
        for specialty in doctor.doctorspecialties:
            doctors_specialty_names.add(specialty.specialty_name)
        if set(specialties) <= doctors_specialty_names:
            matching_doctors.add(doctor)

    # print(calculate_distance(matching_doctors[0], patient))


    return matching_doctors

         
def create_appointment(doctor, patient, datetime):
    return Appointment(doctor=doctor, patient=patient, datetime=datetime)


def get_doctor_by_id(doctor_id):
    """return a doctor by  primary key"""
    return Doctor.query.get(doctor_id)

def get_patient_by_id(patient_id):
    """return a doctor by  primary key"""
    return Patient.query.get(patient_id)

def delete_doctor_availability(doctor, datetime):

    record = DoctorAvailability.query.filter(DoctorAvailability.datetime == datetime , DoctorAvailability.doctor_id == doctor.doctor_id).first()

    db.session.delete(record)
    db.session.commit()

def cancel_appointment(doctor, patient, datetime):

    record = Appointment.query.filter(Appointment.datetime == datetime , Appointment.doctor_id == doctor.doctor_id , Appointment.patient_id == patient.patient_id).first()
    db.session.delete(record)
    db.session.commit()

def delete_all_doctor_availabilities(doctor):
    delete_q = DoctorAvailability.__table__.delete().where(DoctorAvailability.doctor_id == doctor.doctor_id)
    db.session.execute(delete_q)
    db.session.commit()

def delete_all_doctor_specialties(doctor):
    delete_q = DoctorSpecialty.__table__.delete().where(DoctorSpecialty.doctor_id == doctor.doctor_id)
    db.session.execute(delete_q)
    db.session.commit()

def delete_all_doctor_insurances(doctor):
    delete_q = DoctorInsurance.__table__.delete().where(DoctorInsurance.doctor_id == doctor.doctor_id)
    db.session.execute(delete_q)
    db.session.commit()
 
def add_patient_feeling(patient, feeling_rating, feeling_comment, datetime):
    return PatientFeeling(patient=patient, feeling_rating=feeling_rating, feeling_comment=feeling_comment, datetime=datetime)
    
def get_patient_feeling_rating(patient_id):
    return PatientFeeling.query.filter_by(patient_id=patient_id).all()

# def get_doctor_lat_long(doctor):

#     return Doctor.query.filter(Doctor.lat == lat , Doctor.long == long).first()


# def get_patient_lat_long(patient):

#     return Patient.query.filter(Patient.lat == lat , Patient.long == long).first()

# def calculate_distance(doctor, patient):



