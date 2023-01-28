"""CRUD operations."""

from model import db, Patient, Doctor, Appointment, PatientFeeling, DoctorSpecialty, DoctorInsurance, DoctorAvailability, connect_to_db
from geopy.geocoders import Nominatim

# do i need to pass lat and long here?


def create_patient(first_name, last_name, phone, address, email, password):
    lat_long = get_lat_long(address)
    lat = lat_long[0]
    long = lat_long[1]
    patient = Patient(first_name=first_name, last_name=last_name, phone=phone,
                      address=address, lat=lat, long=long, email=email, password=password)

    return patient


def get_patient_by_email(email):
    return Patient.query.filter(Patient.email == email).first()


def create_doctor(first_name, last_name, address, phone, photo_url, bio, email, password, gender):
    lat_long = get_lat_long(address)
    lat = lat_long[0]
    long = lat_long[1]
    doctor = Doctor(first_name=first_name, last_name=last_name,
                    address=address, lat=lat, long=long, phone=phone, photo_url=photo_url, bio=bio, email=email, password=password, gender=gender)

    return doctor


def get_doctor_by_email(email):
    return Doctor.query.filter(Doctor.email == email).first()


def get_doctor_availability(date):
    return DoctorAvailability.query.filter(DoctorAvailability.date == date).first()


def get_lat_long(address):

    geolocator = Nominatim(user_agent="catherapy")
    location = geolocator.geocode(address)

    # print((location.latitude, location.longitude))

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

    # TODO get disatances for all doctors in matching_doctors, then return a list sorted by distance

    return matching_doctors


def get_doctor_by_id(doctor_id):
    """return a doctor by  primary key"""
    return Doctor.query.get(doctor_id)
