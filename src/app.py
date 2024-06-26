from flask import Flask, g, jsonify, redirect, render_template, request, session, url_for

from db import get_db, init_app
from api_routes import api_auth, api_dasboard
from helper import calculate_age

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

app.register_blueprint(api_auth.bp)
app.register_blueprint(api_dasboard.bp)

init_app(app)

@app.route("/index")
def index():
    db = get_db()
    users = db.execute("SELECT * FROM users").fetchall()
    notifications = db.execute(f"SELECT * FROM notifications WHERE user_id = '{g.user['id']}'").fetchall()
    data = {'patients': 0, 'doctors': 0, 'nurses': 0, 'doctors_data':[], 'patients_data': [], 'rooms':db.execute("SELECT * FROM rooms").fetchall()}

    for user in users:
        if user['user_role'] == 'DOCTOR':
            data['doctors']+=1
            data['doctors_data'].append(user)
        elif user['user_role'] == 'NURSE':
            data['nurses']+=1
        elif user['user_role'] == 'PATIENT':
            data['patients']+=1
            data['patients_data'].append(user)
    return render_template("index.html", data=data, notifications=notifications)

@app.route("/")
def signin():
    return render_template("auth-signin.html")

@app.route("/add-health-professional")
def add_health_professional():
    return render_template("add-health-professional.html")

@app.route("/patients", methods=('GET', 'POST'))
def patients():
    users = get_db().execute("SELECT * FROM users WHERE user_role == 'PATIENT'").fetchall()
    return render_template("patients.html", data=users)

@app.route("/register", methods=('GET', 'POST'))
def register():
    return render_template("signup.html")

@app.route("/doctors", methods=('GET', 'POST'))
def doctors():
    db = get_db()
    notifications = db.execute(f"SELECT * FROM notifications WHERE user_id = '{g.user['id']}'").fetchall()
    users = db.execute("SELECT * FROM users WHERE user_role != 'PATIENT' and user_role != 'ADMINISTRATOR'").fetchall()
    return render_template("doctors.html", data=users, notifications=notifications)

@app.route("/schedule", methods=('GET', 'POST'))
def schedule():
    db=get_db()
    notifications = db.execute(f"SELECT * FROM notifications WHERE user_id = '{g.user['id']}'").fetchall()
    return render_template("schedule.html", notifications=notifications)

@app.route("/appointments", methods=('GET', 'POST'))
def appointments():
    user_id = str(g.user['id'])
    data = []

    db = get_db()
    appointments = db.execute("SELECT * FROM appointments").fetchall()
    notifications = db.execute(f"SELECT * FROM notifications WHERE user_id = '{g.user['id']}'").fetchall()
    for a in appointments:
        user = db.execute(f"SELECT * FROM users where id = {a['patient_id']}").fetchone()
        temp = {'user_id':user['id'],'doctor_id': a['doctor_id'], 'id': a['id'],'age': calculate_age(user['dob']), 'patient_name': f"{user['first_name']} {user['last_name']}", 'date_admitted': a['date_admitted'], 'date_discharged': a['date_dischared'], 'status': a['status'],'progress': a['progress'],'schedule_date': a['date'], 'style_width': f"style=width: {a['progress']}%;"}
        data.append(temp)
    
    if g.user['user_role'] == 'PATIENT':
        data = [x for x in data if str(x['user_id']) == user_id]
    else:
        if g.user['user_role'] != 'ADMINISTRATOR':
            data = [v for v in data if str(v['doctor_id']) == user_id]

    return render_template("appointments.html", data=data, notifications=notifications)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('signin'))

if __name__ == "__main__":
    app.run(debug=True)