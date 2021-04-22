# from flask import Flask, render_template, request, send_file, redirect, url_for, flash
# from flask import make_response, session, g, send_file
# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import or_
# from werkzeug.security import generate_password_hash, check_password_hash
# import psycopg2
# import os

# from datetime import datetime, timedelta
# import smtplib
# import imghdr
# from email.message import EmailMessage

# app = Flask(__name__)

# app.config['SECRET_KEY'] = os.urandom(24)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///NEWDATABASE.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# app.config['USE_SESSION_FOR_NEXT'] = True

# db = SQLAlchemy(app)


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
