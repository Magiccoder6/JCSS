from datetime import datetime, timedelta
from flask import Blueprint, g, jsonify, request, session
from db import get_db
from helper import result_to_dict

bp = Blueprint('dashboard', __name__, url_prefix='/api')

@bp.route('/dashboard/add_room', methods=('GET', 'POST'))
def load_dashboard():
    db = get_db()
    room_id = request.form['room_id']
    try:
        db.execute("INSERT INTO rooms (room_id) VALUES (?)", (room_id,))
        db.commit()
    except Exception as e:
        return jsonify({"message": e.__str__()}), 400
    
    return jsonify({}), 200

@bp.route('/dashboard/add_appoinment', methods=('GET', 'POST'))
def add_appoinment():
    doctor_id = request.form['doctor_id']
    date = request.form['date']
    db = get_db()
    
    appointments = db.execute(f"SELECT * FROM appointments WHERE doctor_id = '{doctor_id}'").fetchall()
    previous_appointment = db.execute(f"SELECT * FROM appointments WHERE patient_id = {session['user_id']}").fetchone()

    if previous_appointment is not None: # if there are previous appointment remove it and free up the room
        db.execute(f"DELETE FROM appointments WHERE patient_id = '{session['user_id']}'")

        if previous_appointment['room_id'] is not None:
            db.execute(f"UPDATE rooms SET is_occupied = false WHERE id = {previous_appointment['room_id']};")
        

    #Check if there is a clash with other dates
    
    for appointment in appointments:
        temp_date = datetime.strptime(appointment['date'], '%Y/%m/%d %H:%M %Z') 
        requested_date = datetime.strptime(date, '%Y/%m/%d %H:%M %Z')

        if requested_date == temp_date:
            return jsonify({'message': 'This requested date was already taken, please try again.'}), 400
            

    try:
        db.execute("INSERT INTO appointments (doctor_id, patient_id, date) VALUES (?,?,?)", (doctor_id, session['user_id'], date,))
        db.execute("INSERT INTO notifications (user_id, note, date) VALUES (?,?,?)", (doctor_id, f"{g.user['first_name']} {g.user['last_name']} Requested an appointment with you.", date,))
        
        db.commit()

        return jsonify({"message": "Appointment was requested successfully."}), 200
    except Exception as e:
        return jsonify({"message": e.__str__()}), 400
        
@bp.route('/dashboard/get_schedules', methods=('GET', 'POST'))
def get_schedules():
    user_id = g.user["id"]
    db = get_db()
    
    schedules = db.execute(f"SELECT * FROM appointments WHERE doctor_id = '{user_id}'").fetchall()

    if g.user['user_role'] == "ADMINISTRATOR":
        schedules = db.execute(f"SELECT * FROM appointments").fetchall()

    for schedule in schedules:
        user = db.execute(f"SELECT * FROM users WHERE id = '{schedule['patient_id']}'").fetchone()
        if user is not None:
            schedule['patient'] = f"{user['first_name']} {user['last_name']}"
    
    return jsonify({"message": schedules}), 200

