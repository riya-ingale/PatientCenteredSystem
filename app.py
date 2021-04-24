from flask import Flask, render_template, request, send_file, redirect, url_for, flash
from flask import make_response, session, g, send_file
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
from werkzeug.security import generate_password_hash, check_password_hash
# import psycopg2
import os
from datetime import datetime, timedelta
from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.resources import INLINE
from bokeh.util.string import encode_utf8
from bokeh.models import ColumnDataSource, HoverTool
from flask import Flask, render_template
from bokeh.io import curdoc, gridplot
import pandas as pd
import numpy as np
# import smtplib
# import imghdr
# from email.message import EmailMessage

app = Flask(__name__)

app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:mnir@postgresql123@localhost/PatientCenteredDatabase'
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


class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(500), unique=True)
    password = db.Column(db.String(500))

    name = db.Column(db.String(500))
    dob = db.Column(db.Date)
    city = db.Column(db.String(500))
    phone = db.Column(db.String(500))
    email = db.Column(db.String(500))

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
    appointment_date = db.Column(db.Date)
    symptoms = db.Column(db.String(500))
    medicines = db.Column(db.String(500), nullable=True)
    next_appointment_date = db.Column(db.DateTime, nullable=True)
    recommended_lab_tests = db.Column(db.String(500), nullable=True)

    allergy = db.Column(db.String(500), nullable=True)
    surgery = db.Column(db.String(500), nullable=True)
    surgery_date = db.Column(db.Date)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = "You need to Login first"


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


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


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        name = request.form['name']
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method="sha256")
        cpassword = request.form['cpassword']
        email = request.form['email']
        mobno = request.form['mobno']
        dob = request.form['dob']
        date_time_obj = datetime.strptime(dob, '%Y-%m-%d')
        city = request.form['city']
        role = request.form['roles']
        if role == "admin":
            r_id = 0
        elif role == 'Doctor':
            r_id = 1
        elif role == 'Lab':
            r_id = 2
        else:
            r_id = 3
        user = Users.query.filter_by(user_name=username).first()
        if user:
            flash("User with this Username Already Exists", "warning")
            return redirect("/register")
        else:
            if(password == cpassword):
                new_user = Users(name=name, user_name=username,
                                 password=hashed_password, email=email, phone=mobno, dob=date_time_obj, city=city, r_id=r_id)
                db.session.add(new_user)
                db.session.commit()
                flash("Sucessfully Registered!", "success")
                # sendmail(email)
                return redirect('/login')
            else:
                flash("Passwords don't match", "danger")
                return redirect("/signup")
    return render_template("signup.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        session.pop('user', None)
        username = request.form['username']
        password = request.form['password']
        print("Data collected")
        user = Users.query.filter_by(user_name=username).first()
        if user:
            if check_password_hash(user.password, password):
                print("password is correct")
                login_user(user)
                if current_user.r_id == 1:
                    return redirect(f'/dashboard/doctor/{current_user.id}')
                if current_user.r_id == 2:
                    return redirect(f'/dashboard/lab/{current_user.id}')
                if current_user.r_id == 3:
                    return redirect(f'/dashboard/patient/{current_user.id}')
            else:
                flash("Incorrect Password")
                return redirect(url_for('login'))
        else:
            flash("No such user found, Try Signing Up First", "warning")
            return redirect("/signup")
    return render_template("login.html")


@app.route('/logout')
def logout():
    logout_user()
    flash("Successfully Logged out!")
    return redirect('/login')


# # DASHBOARD - PATIENT

@app.route('/dashboard/patient/<int:user_id>', methods=['GET'])
def patient_dash(user_id):
    user_reports = PatientLab.query.filter_by(patient_id=user_id).all()
    user_apps = DoctorAppointment.query.filter_by(patient_id=user_id).all()

    df = pd.DataFrame(columns=['dates', 'hemoglobin',
                               'platelets', 'rbc_count', 'pcv', 'mcv', 'mchc'])
    for user in user_reports:
        print(user.hemoglobin)
        df = df.append({'dates': user.date_collected, 'hemoglobin': user.hemoglobin, 'platelets': user.platelets, 'rbc_count': user.rbc_count,
                        'pcv': user.pcv, 'mcv': user.mcv, 'mchc': user.mchc}, ignore_index=True)

    fig = figure(title='hemoglobin', plot_width=400,
                 plot_height=300, x_axis_type="datetime", responsive=True)
    df['dates'] = pd.to_datetime(df['dates'])
    print(df['hemoglobin'])
    source = ColumnDataSource(df)
    fig.line(
        x='dates',
        y='hemoglobin',
        source=source,
        line_width=2,
        line_color='#17252A'
    )
    fig.circle(x='dates', y='hemoglobin', source=source,
               fill_color="#DEF2F1", size=8)
    fig.add_tools(HoverTool(tooltips=[("Y", "@hemoglobin")]))
    fig.border_fill_color = "#DEF2F1"
    fig.min_border_right = 80
    s2 = figure(title='platelets', plot_width=400, plot_height=300,
                x_axis_type="datetime", responsive=True)
    source = ColumnDataSource(df)
    s2.line(
        x='dates',
        y='platelets',
        source=source,
        line_width=2,
        line_color='#17252A'
    )
    s2.circle(x='dates', y='platelets', source=source,
              fill_color="#DEF2F1", size=8)
    s2.add_tools(HoverTool(tooltips=[("Y", "@platelets")]))
    s2.border_fill_color = "#DEF2F1"
    s2.min_border_right = 80
    # create and another
    s3 = figure(title='rbc_count', plot_width=400, plot_height=300,
                x_axis_type="datetime", responsive=True)
    source = ColumnDataSource(df)
    s3.line(
        x='dates',
        y='rbc_count',
        source=source,
        line_width=2,
        line_color='#17252A'
    )
    s3.circle(x='dates', y='rbc_count', source=source,
              fill_color="#DEF2F1", size=8)
    s3.add_tools(HoverTool(tooltips=[("Y", "@rbc_count")]))
    s3.border_fill_color = "#DEF2F1"
    s3.min_border_right = 80
    s4 = figure(title='pcv', plot_width=400, plot_height=300,
                x_axis_type="datetime", responsive=True)
    source = ColumnDataSource(df)
    s4.line(
        x='dates',
        y='pcv',
        source=source,
        line_width=2,
        line_color='#17252A'
    )
    s4.circle(x='dates', y='pcv', source=source, fill_color="#DEF2F1", size=8)
    s4.add_tools(HoverTool(tooltips=[("Y", "@pcv")]))
    s4.border_fill_color = "#DEF2F1"
    s4.min_border_right = 80
    s5 = figure(title='mcv', plot_width=400, plot_height=300,
                x_axis_type="datetime", responsive=True)
    source = ColumnDataSource(df)
    s5.line(
        x='dates',
        y='mcv',
        source=source,
        line_width=2,
        line_color='#17252A'
    )
    s5.circle(x='dates', y='mcv', source=source, fill_color="#DEF2F1", size=8)
    s5.add_tools(HoverTool(tooltips=[("Y", "@mcv")]))
    s5.border_fill_color = "#DEF2F1"
    s5.min_border_right = 80
    s6 = figure(title='mchc', plot_width=400, plot_height=300,
                x_axis_type="datetime", responsive=True)
    source = ColumnDataSource(df)
    s6.line(
        x='dates',
        y='mchc',
        source=source,
        line_width=2,
        line_color='#17252A'
    )
    s6.circle(x='dates', y='mchc', source=source, fill_color="#DEF2F1", size=8)
    s6.add_tools(HoverTool(tooltips=[("Y", "@mchc")]))
    s6.border_fill_color = "#DEF2F1"
    s6.min_border_right = 80

    p = gridplot([[fig, s2], [s3, s4], [s5, s6]])
    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()

    # render template
    script, div = components(p)
    html = render_template(
        'patients.html',
        plot_script=script,
        plot_div=div,
        js_resources=js_resources,
        css_resources=css_resources,
        user_apps=user_apps,
        current_user=current_user,
        patient_id=user_id
    )
    return encode_utf8(html)

# # DASHBOARD - LAB


@app.route('/dashboard/lab/<int:user_id>', methods=['GET', 'POST'])
def lab_dash(user_id):
    if request.method == 'GET':
        return 'dashboard asking patient no'
    else:
        patient_no = request.form['patient_no']
        patient_entries = PatientLab.query.filter_by(
            lab_id=user_id, patient_id=patient_no).all()
        return 'direct to the information of pateints taken by the lab keep the ability to update and add'
        'Basically show template'


@app.route('/lab/add/<int:user_id>/<int:patient_id>', methods=["GET", "POST"])
def lab_add(user_id, patient_id):
    if request.method == "GET":
        return render_template('add_lab_results.html', current_user=current_user, pid=patient_id)
    else:
        # take data from and then commit
        date_collected = request.form.get('date_collected')
        date_collected_obj = datetime.strptime(date_collected, '%Y-%m-%d')
        hemoglobin = request.form.get('hemoglobin')
        platelets = request.form.get('platelets')
        rbc_count = request.form.get('rbc_count')
        pcv = request.form.get('pcv')
        mcv = request.form.get('mcv')
        mchc = request.form.get('mchc')
        new_entry = PatientLab(patient_id=patient_id, lab_id=user_id, date_collected=date_collected_obj,
                               hemoglobin=hemoglobin, platelets=platelets, rbc_count=rbc_count, pcv=pcv, mcv=mcv, mchc=mchc)
        db.session.add(new_entry)
        db.session.commit()

        # retrive data from db
        return 'show template'


@app.route('/lab/update/<int:user_id>/<int:patient_id>/<int:report_id>', methods=["GET", "POST"])
def lab_edit(user_id, patient_id, report_id):
    patient = PatientLab.query.filter_by(report_id=report_id).first()
    if request.method == 'GET':
        return render_template('update_lab_results.html', patient=patient)
    else:
        # take data from form and then edit in db
        patient.date_collected = datetime.strptime(
            request.form.get('date_collected'), '%Y-%m-%d')
        patient.hemoglobin = request.form.get('hemoglobin')
        patient.platelets = request.form.get('platelets')
        patient.rbc_count = request.form.get('rbc_count')
        patient.pcv = request.form.get('pcv')
        patient.mcv = request.form.get('mcv')
        patient.mchc = request.form.get('mchc')
        db.session.commit()

        # retrive data from db
        return 'show template'


# # DASHBOARD - DOCTOR


@app.route('/dashboard/doctor/<int:user_id>', methods=['GET', 'POST'])
def doctor_dash(user_id):
    if request.method == "GET":
        doc_appointments = DoctorAppointment.query.filter_by(
            doc_id=user_id).all()
        doc_info = Users.query.filter_by(id=user_id).first()

        return render_template('doctor.html', doc_appointments=doc_appointments, doc_info=doc_info, current_user=current_user)
    else:
        patient_no = request.form['patient_no']
        print(patient_no, user_id)
        patient_lab_results = PatientLab.query.filter_by(
            patient_id=patient_no).all()
        patient_prev_appointments = DoctorAppointment.query.filter_by(
            patient_id=patient_no).all()
        return redirect('/dashboard/patient/'+str(patient_no))


@app.route('/doctor/add/<int:user_id>/<int:patient_id>', methods=["GET", "POST"])
def doctor_add(user_id, patient_id):
    if request.method == "GET":
        return render_template('add_appointment_details.html', pid=patient_id)
    else:
        # take data from and then commit
        hospital = request.form.get('hospital')
        appointment_date = request.form.get('appointment_date')
        appointment_date_obj = datetime.strptime(appointment_date, '%Y-%m-%d')
        symptoms = request.form.get('symptoms')
        medicines = request.form.get('medicines')
        next_appointment_date = request.form.get('next_appointment_date')
        next_appointment_date_obj = datetime.strptime(
            next_appointment_date, '%Y-%m-%d')
        recommended_lab_tests = request.form.get('recommended_lab_tests')

        allergy = request.form.get('allergy')
        surgery = request.form.get('surgery')
        surgery_date = request.form.get('surgery_date')
        if surgery_date != "":
            surgery_date_obj = datetime.strptime(surgery_date, '%Y-%m-%d')
        else:
            surgery_date_obj = None

        new_entry = DoctorAppointment(patient_id=patient_id, doc_id=user_id, hospital=hospital, appointment_date=appointment_date_obj, symptoms=symptoms, medicines=medicines,
                                      next_appointment_date=next_appointment_date_obj, recommended_lab_tests=recommended_lab_tests, allergy=allergy, surgery=surgery, surgery_date=surgery_date_obj)
        db.session.add(new_entry)
        db.session.commit()

        patient_lab_results = PatientLab.query.filter_by(
            patient_id=patient_id).all()
        patient_prev_appointments = DoctorAppointment.query.filter_by(
            patient_id=patient_id).all()
        return redirect('/dashboard/patient/'+str(patient_id))


@app.route('/doctor/update/<int:user_id>/<int:patient_id>/<int:app_id>', methods=["GET", "POST"])
# user_id==doctor_id
def doc_edit(user_id, patient_id, app_id):
    patient = DoctorAppointment.query.filter_by(app_id=app_id).first()

    if request.method == 'GET':
        return render_template('update_appointment_details.html', patient=patient)
    else:
        # take data from form and then edit in db
        patient.hospital = request.form.get('hospital')
        patient.appointment_date = request.form.get('appointment_date')
        patient.symptoms = request.form.get('symptoms')
        patient.medicines = request.form.get('medicines')
        if request.form.get('next_appointment_date') != "":
            patient.next_appointment_date = datetime.strptime(
                request.form.get('next_appointment_date'), '%Y-%m-%d')
        else:
            patient.next_appointment_date = None
        patient.recommended_lab_tests = request.form.get(
            'recommended_lab_tests')
        patient.allergy = request.form.get('allergy')
        patient.surgery = request.form.get('surgery')
        if request.form.get('surgery_date') != "":
            patient.surgery_date = datetime.strptime(
                request.form.get('surgery_date'), '%Y-%m-%d')
        else:
            patient.surgery_date = None
        db.session.commit()

        # retrive data from db
        appointments = DoctorAppointment.query.filter_by(
            doc_id=user_id, patient_id=patient_id).all()

        return 'show template with all appointments'


# @app.route('/doctor/update/<int:user_id>/<int:patient_id>/<int:app_id>', methods=["GET", "POST"])
# def doc_delete(user_id,patient_id,app_id):
#     patient = DoctorAppointment.query.filter_by(app_id=app_id).first()
#     db.session.delete(patient)
#     db.session.commit()
#     return redirect('pati')


@app.route('/lab', methods=["GET", "POST"])
def bokeh():
    fig = figure(title='Hemoglobin', plot_width=400,
                 plot_height=300, x_axis_type="datetime", responsive=True)
    df = pd.DataFrame.from_dict({'dates': ["1-1-2019", "2-1-2019", "3-1-2019", "4-1-2019", "5-1-2019", "6-1-2019", "7-1-2019", "8-1-2019", "9-1-2019", "10-1-2019"],
                                 'x': [10, 15, 16, 17, 15, 15, 15, 20, 15, 19]})
    df['dates'] = pd.to_datetime(df['dates'])
    source = ColumnDataSource(df)
    fig.line(
        x='dates',
        y='x',
        source=source,
        line_width=2,
        line_color='#17252A'
    )
    fig.circle(x='dates', y='x', source=source, fill_color="#DEF2F1", size=8)
    fig.add_tools(HoverTool(tooltips=[("Y", "@x")]))
    fig.border_fill_color = "#DEF2F1"
    fig.min_border_right = 80
    s2 = figure(title='Hemoglobin', plot_width=400, plot_height=300,
                x_axis_type="datetime", responsive=True)
    source = ColumnDataSource(df)
    s2.line(
        x='dates',
        y='x',
        source=source,
        line_width=2,
        line_color='#17252A'
    )
    s2.circle(x='dates', y='x', source=source, fill_color="#DEF2F1", size=8)
    s2.add_tools(HoverTool(tooltips=[("Y", "@x")]))
    s2.border_fill_color = "#DEF2F1"
    s2.min_border_right = 80
    # create and another
    s3 = figure(title='Hemoglobin', plot_width=400, plot_height=300,
                x_axis_type="datetime", responsive=True)
    source = ColumnDataSource(df)
    s3.line(
        x='dates',
        y='x',
        source=source,
        line_width=2,
        line_color='#17252A'
    )
    s3.circle(x='dates', y='x', source=source, fill_color="#DEF2F1", size=8)
    s3.add_tools(HoverTool(tooltips=[("Y", "@x")]))
    s3.border_fill_color = "#DEF2F1"
    s3.min_border_right = 80
    s4 = figure(title='Hemoglobin', plot_width=400, plot_height=300,
                x_axis_type="datetime", responsive=True)
    source = ColumnDataSource(df)
    s4.line(
        x='dates',
        y='x',
        source=source,
        line_width=2,
        line_color='#17252A'
    )
    s4.circle(x='dates', y='x', source=source, fill_color="#DEF2F1", size=8)
    s4.add_tools(HoverTool(tooltips=[("Y", "@x")]))
    s4.border_fill_color = "#DEF2F1"
    s4.min_border_right = 80
    s5 = figure(title='Hemoglobin', plot_width=400, plot_height=300,
                x_axis_type="datetime", responsive=True)
    source = ColumnDataSource(df)
    s5.line(
        x='dates',
        y='x',
        source=source,
        line_width=2,
        line_color='#17252A'
    )
    s5.circle(x='dates', y='x', source=source, fill_color="#DEF2F1", size=8)
    s5.add_tools(HoverTool(tooltips=[("Y", "@x")]))
    s5.border_fill_color = "#DEF2F1"
    s5.min_border_right = 80
    s6 = figure(title='Hemoglobin', plot_width=400, plot_height=300,
                x_axis_type="datetime", responsive=True)
    source = ColumnDataSource(df)
    s6.line(
        x='dates',
        y='x',
        source=source,
        line_width=2,
        line_color='#17252A'
    )
    s6.circle(x='dates', y='x', source=source, fill_color="#DEF2F1", size=8)
    s6.add_tools(HoverTool(tooltips=[("Y", "@x")]))
    s6.border_fill_color = "#DEF2F1"
    s6.min_border_right = 80
    p = gridplot([[fig, s2], [s3, s4], [s5, s6]])
    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()
    # render template
    script, div = components(p)
    html = render_template(
        'patients.html',
        plot_script=script,
        plot_div=div,
        js_resources=js_resources,
        css_resources=css_resources,
    )
    return encode_utf8(html)


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
