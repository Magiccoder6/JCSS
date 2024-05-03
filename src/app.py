from flask import Flask, g, jsonify, redirect, render_template, request, session, url_for

from db import get_db, init_app
from api_routes import api_auth, api_dasboard

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

app.register_blueprint(api_auth.bp)
app.register_blueprint(api_dasboard.bp)

init_app(app)

@app.route("/index")
def index():
    db = get_db()
    users = db.execute("SELECT * FROM users").fetchall()
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
    return render_template("index.html", data=data)

@app.route("/")
def signin():
    return render_template("auth-signin.html")

@app.route("/register", methods=('GET', 'POST'))
def register():
    return render_template("signup.html")

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('signin'))

if __name__ == "__main__":
    app.run(debug=True)