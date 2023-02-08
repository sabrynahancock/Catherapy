"""Server for Catherapy app."""

from flask import Flask, render_template, request, flash, session, redirect, jsonify
from model import connect_to_db, db, Doctor
import crud
from datetime import datetime, timedelta
from jinja2 import StrictUndefined
from geopy import distance

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

#add docstrings


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
    patient = None
    doctor = None

    if "patient_email" in session:
        patient = crud.get_patient_by_email(session["patient_email"])

    if "doctor_email" in session:
        doctor = crud.get_doctor_by_email(session["doctor_email"])

    return render_template("homepage.html", doctor=doctor, patient=patient)




@app.route("/login", methods=['POST'])
def login():

    email = request.form.get("email")
    password = request.form.get("password")

    patient = crud.get_patient_by_email(email)
    doctor = crud.get_doctor_by_email(email)

    if patient and patient.password == password:
        session["patient_email"] = patient.email
        return redirect("/homepage")

    elif doctor and doctor.password == password:
        session["doctor_email"] = doctor.email
        return redirect("/homepage")

    else:
        flash("The email or password you entered was incorrect.")

        return redirect("/")


@app.route("/doc-logout", methods=['POST'])
def doctor_logout():
    if "doctor_email" in session:
        del session["doctor_email"]
    flash("You're signed out!")
    return redirect("/")


@app.route("/patient-logout", methods=['POST'])
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
        patient = crud.create_patient(
            first_name, last_name, phone, address, email, password)
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
    photo_url = request.form.get("photo_url")
    bio = request.form.get("bio")
    email = request.form.get("email")
    password = request.form.get("password")
    gender = request.form.get("gender")

    doctor = crud.get_doctor_by_email(email)

    if doctor:
        flash("Please try using a different email")
        return redirect("/doctor-registration")

    else:
        doctor = crud.create_doctor(
            first_name, last_name, address, phone, photo_url, bio, email, password, gender)

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
    print(time_slots)
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
        distance_from_patient = calculate_distance((doctor.lat, doctor.long) , (patient.lat, patient.long))
        doctors.append(doctor.get_doctor_data_for_search_result(distance_from_patient))
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

    return redirect("/homepage")

def calculate_distance(doctor, patient):

    dist = distance.distance(doctor , patient).miles
    
    return round(dist, 1)

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
    db.create_all()
