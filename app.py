from flask import Flask, render_template, request, send_file, redirect, url_for, flash
from flask import make_response, session, g, send_file
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
# from werkzeug.security import generate_password_hash, check_password_hash
# import psycopg2
import os

# from datetime import datetime, timedelta
# import smtplib
# import imghdr
# from email.message import EmailMessage

app = Flask(__name__)

app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/PatientCenteredDatabase'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///PatientCenteredDatabase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['USE_SESSION_FOR_NEXT'] = True

db = SQLAlchemy(app)


class Roles(db.Model):

    __tablename__ = "Roles"
    r_id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(20))
    clearance_level = db.Column(db.Integer, nullable=True)
    details = db.relationship('Users', backref='Roles')


class Users(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))

    name = db.Column(db.String(50))
    dob = db.Column(db.DateTime(50))
    city = db.Column(db.String(50))
    address = db.Column(db.String(500))
    phone = db.Column(db.Integer)
    email = db.Column(db.String(50))

    r_id = db.Column(db.Integer, db.ForeignKey('Roles.r_id'))


class PatientLab(db.Model):
    report_id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer())
    lab_id = db.Column(db.Integer())

    date_collected = db.Column(db.DateTime)
    hemoglobin = db.Column(db.Float(), nullable=True)
    platelets = db.Column(db.Float(), nullable=True)
    rbc_count = db.Column(db.Float(), nullable=True)
    pcv = db.Column(db.Float(), nullable=True)
    mcv = db.Column(db.Float(), nullable=True)
    mchc = db.Column(db.Float(), nullable=True)
    mch = db.Column(db.Float(), nullable=True)


class DoctorAppointment(db.Model):
    app_id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer)
    doc_id = db.Column(db.Integer)

    hospital = db.Column(db.String(500))
    appointment_date = db.Column(db.DateTime)
    symptoms = db.Column(db.String(500))
    medicines = db.Column(db.String(500), nullable=True)
    next_appointment_date = db.Column(db.DateTime, nullable=True)
    recommended_lab_tests = db.Column(db.String(500), nullable=True)

    allergy = db.Column(db.String(500), nullable=True)
    surgery = db.Column(db.String(500), nullable=True)
    surgery_date = db.Column(db.DateTime)


# @app.route('/')
# @app.route('/index')
# def index():
#     return render_template('index.html')


# @app.before_request
# def before_request():
#     g.user = None
#     if 'user' in session:
#         user = User.query.filter_by(id=session['user']).first()
#         g.user = user


# @app.before_request
# def make_session_permanent():
#     session.permanent = True
#     app.permanent_session_lifetime = timedelta(minutes=10)


# EMAIL_ADDRESS = 'mail@gmail.com'
# EMAIL_PASSWORD = 'mailpassword'


# def sendmail(mail_id):
#     msg = EmailMessage()
#     msg['Subject'] = 'Sucessfully Registered to Music Fiesta!'
#     msg['From'] = EMAIL_ADDRESS
#     msg['To'] = mail_id
#     msg.set_content('Thank you for Registering to Music Fiesta.')

#     f = open("templates/hello.txt", "r")
#     msg.add_alternative(f.read(), subtype='html')

#     with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
#         smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
#         smtp.send_message(msg)


# @app.route('/signup', methods=['GET', 'POST'])
# def signup():
#     if request.method == "POST":
#         name = request.form['name']
#         username = request.form['username']
#         password = request.form['password']
#         hashed_password = generate_password_hash(password, method="sha256")
#         cpassword = request.form['cpassword']
#         email = request.form['email']
#         mobno = request.form['mobno']
#         user = Users.query.filter_by(username=username).first()
#         if user:
#             flash("User with this Username Already Exists", "warning")
#             return redirect("/register")
#         else:
#             if(password == cpassword):
#             new_user = User(name=name, username=username,
#                             password=password, email=email, phone_number=mobno)
#             db.session.add(new_user)
#             db.session.commit()
#             flash("Sucessfully Registered!", "success")

#             sendmail(email)

#             return redirect('/login')
#         else:
#             flash("Passwords don't match", "danger")
#             return redirect("/signup")
#     return render_template("signup.html")


# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == "POST":
#         session.pop('user', None)
#         username = request.form['username']
#         password = request.form['password']

#         user = User.query.filter_by(username=username).first()
#         if user:
#             if check_password_hash(user.password, password):
#                 print("password is correct")
#                 session['user'] = user.id
#                 return redirect(f"/dashboard/{user.id}")
#             else:
#                 flash("Incorrect Password")
#                 return redirect(url_for('login'))
#         else:
#             flash("No such user found, Try Signing Up First", "warning")
#             return redirect("/signup")
#     return render_template("login.html")

# @app.route('/dropsession', methods=['POST', 'GET'])
# def dropsession():
#     session.pop('user', None)
#     flash("Sucessfully Logged Out")
#     return render_template('login.html')

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
