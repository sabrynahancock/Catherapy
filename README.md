# Catherapy

Catherapy is a  full stack web application that connects mental health patients with doctors. The app is designed to help patients find the right mental care provider and help doctors manage their practice effectively.

<iframe width="560" height="315" src="https://www.youtube.com/embed/U4-HLFf7qtM" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

## Features

- Patients can track their mood and search for doctors using filters such as distance, accepted insurances, and specialties.
- Doctors can update their profile with availability, accepted insurances, and specialties.
- The app integrates Maps JavaScript API and Chart.js for location and data visualization.
- Security is ensured using Argon2 for password hashing.

## Technologies Used

The application was developed using the following technologies:

- Python
- Flask
- JavaScript (AJAX, JSON)
- React
- Bootstrap
- Jinja
- HTML
- CSS
- SQL


## Installation

To install and run the app, follow these steps:

1. Clone the repository to your local machine
2. Create and activate a virtual environment
 `$ virtualenv env`
` $source env/bin/activate`
3. Install the necessary dependencies using `$ pip install -r requirements.txt`
4. Run the secrets.sh file ` $ source secrets.sh`
5. Run model.py to create the database models `$ python3 model.py`
6. Create database `$ createdb catherapy`
7. Run the app from the command line
`$ python3 server.py`

## Credits

This app was developed by Sabryna Hancock. If you have any questions or suggestions, please feel free to connect with me on [Linkedin](https://www.linkedin.com/in/sabryna-hancock/)
