"""Server for Catherapy app."""

from flask import Flask, render_template, request, flash, session, redirect, jsonify
from model import connect_to_db, db, Doctor
import crud
from datetime import datetime, timedelta
from jinja2 import StrictUndefined
from geopy import distance
import cloudinary.uploader
import os
import random
import argon2
from argon2 import PasswordHasher

CLOUDINARY_KEY = os.environ['CLOUDINARY_KEY']
CLOUDINARY_SECRET = os.environ['CLOUDINARY_SECRET']
CLOUD_NAME = "dvdpiblk8"

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined



@app.route("/")
def welcome_page():
    """Welcome Page"""

    if "patient_email" in session:
        return redirect("/homepage")

    elif "doctor_email" in session:
        return redirect("/homepage")

    return render_template("welcomepage.html")


@app.route("/homepage")
def home_page():
    """homepage for doctor and patients"""
    patient = None
    doctor = None

    if "patient_email" in session:
        affirmation = generate_positive_affirmation()
        patient = crud.get_patient_by_email(session["patient_email"])
        return render_template("homepage.html", patient=patient, has_patient_submitted_feeling_today=has_patient_submitted_feeling_today(), affirmation=affirmation)

    if "doctor_email" in session:
        reasons = generate_reasons_doctor_page()
        doctor = crud.get_doctor_by_email(session["doctor_email"])
        return render_template("doctor-homepage.html", doctor=doctor, reasons=reasons)



@app.route("/login", methods=['POST'])
def login():

    email = request.form.get("email")
    password = request.form.get("password")

    patient = crud.get_patient_by_email(email)
    doctor = crud.get_doctor_by_email(email)

    if patient:
       
        ph = PasswordHasher()
        try:
            ph.verify(patient.password, password)
        except:
            pass
        else:
            session["patient_email"] = patient.email
            return redirect("/homepage")

    elif doctor:
        
        ph = PasswordHasher()
        try:
            ph.verify(doctor.password, password)
        except:
            pass
        else:
            session["doctor_email"] = doctor.email
            return redirect("/homepage")

    flash("The email or password you entered was incorrect.")
    return redirect("/")


@app.route("/doc-logout")
def doctor_logout():
    if "doctor_email" in session:
        del session["doctor_email"]
    flash("You're signed out!")
    return redirect("/")


@app.route("/patient-logout")
def patient_logout():
    if "patient_email" in session:
        del session["patient_email"]
    flash("You're signed out!")
    return redirect("/")


@app.route("/patient-registration")
def patient_registration():
    """Register a new patient"""

    return render_template("patient-registration.html")


@app.route("/patient-registration-submit", methods=["POST"])
def patient_registration_submit():
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    phone = request.form.get("phone")
    address = request.form.get("address")
    email = request.form.get("email")
    password = request.form.get("password")

    patient = crud.get_patient_by_email(email)

    if patient:
        flash("Please try using a different email")
        return redirect("/patient-registration")

    else:
    
        ph = PasswordHasher()
        hashed_password = ph.hash(password)

        patient = crud.create_patient(
            first_name, last_name, phone, address, email, hashed_password)
        db.session.add(patient)
        db.session.commit()
        flash("Account created successfully! Please log in.")

        return redirect("/")


@app.route("/doctor-registration")
def doctor_registration():
    """Register a new doctor"""

    return render_template("doctor-registration.html")


@app.route("/doctor-registration-submit", methods=["POST"])
def doctor_registration_submit():
    """Submit doctors registration"""

    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    address = request.form.get("address")
    phone = request.form.get("phone")
    bio = request.form.get("bio")
    email = request.form.get("email")
    password = request.form.get("password")
    gender = request.form.get("gender")

    img_file = request.files["file_input"]
    result = cloudinary.uploader.upload(
        img_file, api_key=CLOUDINARY_KEY, api_secret=CLOUDINARY_SECRET, cloud_name=CLOUD_NAME)
    img_url = result['secure_url']
    doctor = crud.get_doctor_by_email(email)

    if doctor:
        flash("Please try using a different email")
        return redirect("/doctor-registration")

    else:
        ph = PasswordHasher()
        hashed_password = ph.hash(password)
        doctor = crud.create_doctor(
            first_name, last_name, address, phone, img_url, bio, email, hashed_password, gender)

        db.session.add(doctor)
        db.session.commit()
        flash("Account created successfully! Please log in.")

        return redirect("/")


def availabilities():

    today = datetime.now()
    time_slots = []

    for i in range(0, 7):

        day = (today + timedelta(days=i))
        start_time = datetime(day.year, day.month, day.day, 8)
        time_slots.append([])
        for hour in range(0, 9):
            time = (start_time + timedelta(hours=hour))

            time_slots[i].append(time)
    return time_slots


SPECIALTIES = sorted(["Anxiety", "Depression", "Eating Disorder",
                      "Stress", "PTSD", "ADHD", "Panic", "Grief", "OCD"])


INSURANCES = sorted(["Catto", "Doggo", "Purfect", "Meowsome", "Pawsome"])


@app.route("/update-doctor-profile")
def update_availability_page():

    return render_template("update-doctor-profile.html", time_slots=availabilities(), specialties=SPECIALTIES, insurances=INSURANCES)


@app.route("/update-doctor-profile-submit", methods=["POST"])
def update_doctor_profile():

    doctor = crud.get_doctor_by_email(session["doctor_email"])
    crud.delete_all_doctor_availabilities(doctor)
    crud.delete_all_doctor_specialties(doctor)
    crud.delete_all_doctor_insurances(doctor)

    checked_time_slots = request.form.getlist("time_slots")
    for datetime in checked_time_slots:
        availability = crud.create_doctor_availability(doctor, datetime)
        db.session.add(availability)

    checked_specialties = request.form.getlist("doctor_specialty")
    for specialty in checked_specialties:
        db.session.add(crud.create_doctor_specialty(doctor, specialty))

    checked_insurances = request.form.getlist("doctor_insurance")
    for insurance in checked_insurances:
        db.session.add(crud.create_doctor_insurance(doctor, insurance))

    db.session.commit()

    return redirect("/homepage")


@app.route("/search")
def search():

    return render_template("search.html", specialties=SPECIALTIES, insurances=INSURANCES)


@app.route("/search-submit", methods=["POST"])
def search_submit():

    patient = crud.get_patient_by_email(session["patient_email"])
    checked_specialties = request.json.get("selectedSpecialties")
    selected_insurance = request.json.get("selectedInsurance")

    search_results = crud.get_doctor_with_criteria(
        checked_specialties, selected_insurance)
    doctor_dict = {}
    doctors = []
    for doctor in search_results:
        distance_from_patient = calculate_distance(
            (doctor.lat, doctor.long), (patient.lat, patient.long))
        doctors.append(doctor.get_doctor_data_for_search_result(
            distance_from_patient))
    doctors.sort(key=lambda doctor: doctor['distance_from_patient'])

    return jsonify(
        doctors=doctors
    )


@app.route("/save-appt-database", methods=["POST"])
def save_appt_database():

    doctor_id = request.form.get("doctor_id")
    doctor = crud.get_doctor_by_id(doctor_id)
    patient = crud.get_patient_by_email(session["patient_email"])

    datetime = request.form.get("selected_availability")

    db.session.add(crud.create_appointment(doctor, patient, datetime))
    db.session.commit()
    crud.delete_doctor_availability(doctor, datetime)
    return redirect("/homepage")


@app.route("/patient-delete-appointment", methods=["POST"])
def patient_delete_appointment():

    patient = crud.get_patient_by_email(session["patient_email"])
    doctor_id = request.form.get("doctor_id")
    doctor = crud.get_doctor_by_id(doctor_id)
    datetime = request.form.get("selected_datetime")

    crud.cancel_appointment(doctor, patient, datetime)
    return redirect("/homepage")


@app.route("/doctor-delete-appointment", methods=["POST"])
def doctor_delete_appointment():

    doctor = crud.get_doctor_by_email(session["doctor_email"])
    patient_id = request.form.get("patient_id")
    patient = crud.get_patient_by_id(patient_id)
    datetime = request.form.get("selected_datetime")

    crud.cancel_appointment(doctor, patient, datetime)

    return jsonify({'doctor': doctor.get_doctor_data_for_homepage()})


def calculate_distance(doctor, patient):

    dist = distance.distance(doctor, patient).miles

    return round(dist, 1)


@app.route("/add-patient-feeling-submit", methods=["POST"])
def add_patient_feeling_submit():
    patient = crud.get_patient_by_email(session["patient_email"])
    feeling_rating = request.form.get("feeling_rating")
    feeling_comment = request.form.get("feeling_comment")
    current_datetime = datetime.now()

    db.session.add(crud.add_patient_feeling(
        patient, feeling_rating, feeling_comment, current_datetime))
    db.session.commit()

    return redirect("/homepage")


def has_patient_submitted_feeling_today():
    if "patient_email" in session:
        patient = crud.get_patient_by_email(session["patient_email"])
    else:
        return False

    has_patient_submitted_feeling_today = False
    for patient_feeling in patient.patientfeelings:
        if patient_feeling.datetime.date() == datetime.today().date():
            has_patient_submitted_feeling_today = True
    return has_patient_submitted_feeling_today
    return False


@app.route("/mood-tracker")
def mood_tracker_page():
    patient = None

    if "patient_email" in session:
        patient = crud.get_patient_by_email(session["patient_email"])

    return render_template("mood-tracker.html", patient=patient)


@app.route('/feelings', methods=['GET'])
def get_feelings():
    patient = crud.get_patient_by_email(session["patient_email"])
    feelings = crud.get_patient_feeling_rating(patient.patient_id)
    feelings_list = []
    for feeling in feelings:
        feelings_list.append(feeling.feeling_rating)

    return jsonify({'ratings': feelings_list})


@app.route('/doctor-data.json', methods=['GET'])
def get_doctor_data_json():

    doctor = crud.get_doctor_by_email(session["doctor_email"])

    return jsonify({'doctor': doctor.get_doctor_data_for_homepage()})


@app.route('/about')
def about_catherapy_template():

    return render_template("about.html")


@app.route('/adopt')
def adopt_template():

    return render_template("adopt.html")


def generate_positive_affirmation():
    affirmations = [
        "I am worthy of love and respect.",
        "I am capable of achieving my goals.",
        "I am confident and strong.",
        "I trust my intuition and make good decisions.",
        "I am grateful for all the blessings in my life.",
        "I am surrounded by positive energy and good people.",
        "I believe in myself and my abilities.",
        "I choose to let go of negativity and embrace positivity.",
        "I am deserving of happiness and fulfillment.",
        "I am loved and appreciated for who I am.",
        "I am healthy and strong in mind, body, and spirit.",
        "I am open to new opportunities and experiences.",
        "I have the power to create the life I desire.",
        "I am at peace with myself and the world around me."
    ]
    return random.choice(affirmations)


def generate_reasons_doctor_page():
    reasons = [
        'To help people overcome difficult challenges',
        'To provide support to those who are struggling',
        'To be a guide and mentor to those in need',
        'To offer hope to those who feel lost or alone',
        'To create a safe space for people to express themselves',
        'To make a positive impact in the world',
        'To empower individuals to reach their full potential',
        'To promote mental wellness and self-care',
        'To inspire change and growth in others',
        'To be a voice for those who are not heard',
    ]
    return random.choice(reasons)


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
    db.create_all()
