"""Server for Catherapy app."""

from flask import Flask, render_template, request, flash, session, redirect
from model import connect_to_db, db
import crud
from datetime import datetime, timedelta
from jinja2 import StrictUndefined

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
    patient = None
    doctor = None


    if "patient_email" in session:
        patient = crud.get_patient_by_email(session["patient_email"])

    if "doctor_email" in session:
        doctor = crud.get_doctor_by_email(session["doctor_email"])

    return render_template("homepage.html", doctor=doctor, patient=patient)

#need to work on homepage for doctors page 

        


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

@app.route("/logout", methods=['POST'])
def logout():
        if "doctor_email" in session:
            del session["doctor_email"]
        flash("You're signed out!")
        return redirect("/")

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
        patient = crud.create_patient(first_name, last_name, phone, address, email, password)  
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

    
    doctor = crud.get_doctor_by_email(email)

    if doctor:
        flash("Please try using a different email")
        return redirect("/doctor-registration")

    else:
        doctor = crud.create_doctor(first_name, last_name, address, phone, photo_url, bio, email, password)  

        db.session.add(doctor)
        db.session.commit()
        flash("Account created successfully! Please log in.")

        return redirect("/")


def availabilities():

    today = datetime.now()
    time_slots = []

    
    for i in range(0,7):

        day = (today + timedelta(days = i))
        start_time = datetime(day.year, day.month, day.day, 8)
        time_slots.append([])
        for hour in range(0,9):
            time = (start_time + timedelta(hours = hour))

            time_slots[i].append(time)
    print(time_slots)
    return time_slots
    

@app.route("/doctor-availability")
def update_availability_page():

    return render_template("doctor-availability.html", time_slots=availabilities())


@app.route("/select-dates" , methods=["POST"])
def select_dates():

#     # doc_id = crud.get_doctor_by_id(doctor_id)
#      selected_dates = request.json.get("time_slots")
#     # dates = cud.create_doctor_availabilities(date, doctor)
#     # db.session.add()
#     # logged_in_email = session.get("doctor_email")
    checked_time_slots = request.form.getlist("time_slots")
    print(checked_time_slots)
#     # #loop through values
#     # for value in values:

    doctor = crud.get_doctor_by_email(session["doctor_email"])
#     doctor_id = doctor.doctor_id

    for datetime in checked_time_slots:


        availability = crud.create_doctor_availability(doctor, datetime)
        db.session.add(availability)
    db.session.commit()             
        #return redirect("/homepage")
        
    return redirect("/homepage")
#     #create availabily
#     #get doctor from session





    


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
    db.create_all()
