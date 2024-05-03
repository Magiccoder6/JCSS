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
        print(e.__str__())
        return jsonify({"message": e.__str__()}), 400
    
    return jsonify({}), 200