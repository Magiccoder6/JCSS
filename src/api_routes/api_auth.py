from werkzeug.security import check_password_hash, generate_password_hash
from flask import Blueprint, g, jsonify, request, session
from db import get_db

bp = Blueprint('auth', __name__, url_prefix='/api')

@bp.route('/auth/signin', methods=('GET', 'POST'))
def login():
    email = request.form['email']
    password = request.form['password']
    db = get_db()
    error = None
    user = db.execute(
        f"SELECT * FROM users WHERE email = '{email}'"
    ).fetchone()

    if user is None:
        error = 'Incorrect email.'
    elif not check_password_hash(user['passcode'], password):
        error = 'Incorrect password.'

    if error is None:
        session.clear()
        session['user_id'] = user['id']
        return jsonify({"message": 'OK'}), 200
    
    return jsonify({"message": error}), 400

@bp.route("/auth/register", methods=('GET', 'POST'))
def api_register():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    phone_number = request.form['phone_number']
    gender = request.form['gender']
    dob = request.form['dob']
    password = request.form['passcode']
    user_role = "PATIENT"
    db = get_db()

    try:
        db.execute(
            "INSERT INTO users (first_name, last_name, email, phone_number, gender, dob, passcode, user_role) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (first_name, last_name, email, phone_number, gender, dob, generate_password_hash(password), user_role),
        )
        db.commit()
    except Exception as e:
        return jsonify({"message": e.__str__()}), 400
        
    return jsonify({"message": "You were registered successfully!!"}), 200

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM users WHERE id = ?', (user_id,)
        ).fetchone()