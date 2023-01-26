"""CRUD operations."""

from model import db, Patient, Doctor, Appointment, PatientFeeling, DoctorSpecialty, Specialty, DoctorInsurance, DoctorAvailability , connect_to_db
from geopy.geocoders import Nominatim

#do i need to pass lat and long here? 

def create_patient(first_name, last_name, phone, address, email, password):
    lat_long = get_lat_long(address)
    lat = lat_long[0]
    long = lat_long[1]
    patient = Patient(first_name=first_name, last_name=last_name, phone=phone, 
    address=address, lat=lat , long=long, email=email, password=password)

    return patient

def get_patient_by_email(email):
     return Patient.query.filter(Patient.email == email).first()


def create_doctor(first_name, last_name, address, phone, photo_url, bio, email, password):
    lat_long = get_lat_long(address)
    lat = lat_long[0]
    long = lat_long[1]
    doctor = Doctor(first_name=first_name, last_name=last_name, 
    address=address, lat=lat , long=long, phone=phone, photo_url=photo_url, bio=bio,email=email, password=password)

    return doctor


def get_doctor_by_email(email):
     return Doctor.query.filter(Doctor.email == email).first()


def get_doctor_availability(date):
     return DoctorAvailability.query.filter(DoctorAvailability.date == date).first()


def get_lat_long(address):

     geolocator = Nominatim(user_agent="catherapy")
     location = geolocator.geocode(address)
     
     #print((location.latitude, location.longitude))

     return (location.raw['lat'], location.raw['lon'])

def create_doctor_availability(doctor, date):

     doctoravailability = DoctorAvailability(doctor=doctor, date=date)
     return doctoravailability

def get_doctor_by_id(doctor_id):
     """return a doctor by  primary key"""
     return Doctor.query.get(doctor_id)

