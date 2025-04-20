from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def initdb():
    patient_conn = sqlite3.connect('patient.db')
    doctor_conn = sqlite3.connect('doctor.db')
    comment_conn = sqlite3.connect('comment.db')
    pat_cursor = patient_conn.cursor()
    doc_cursor = doctor_conn.cursor()
    com_cursor = comment_conn.cursor()
    pat_cursor.execute('''CREATE TABLE IF NOT EXISTS patients( pat_id INTEGER PRIMARY KEY, pat_name TEXT, age INTEGER, contact TEXT, allergies TEXT, medications TEXT)''')
    doc_cursor.execute('''CREATE TABLE IF NOT EXISTS doctors( doc_id INTEGER PRIMARY KEY, doc_name TEXT, age INTEGER, contact TEXT, specialization TEXT, patients TEXT, schedule TEXT)''')
    com_cursor.execute('''CREATE TABLE IF NOT EXISTS comments( thread_id INTEGER, com_id INTEGER, content TEXT, auth_id TEXT)''')

    patient_conn.commit()
    doctor_conn.commit()
    comment_conn.commit()
    patient_conn.close()
    doctor_conn.close()
    comment_conn.close()

@app.route('/insert_patient', methods=['POST'])
def insert_patient_route():
    data = request.get_json()
    pat_id = data['pat_id']
    pat_name = data['pat_name']
    age = data['age']
    contact = data['contact']
    allergies = data['allergies']
    medications = data['medications']

    insert_patient(pat_id, pat_name, age, contact, allergies, medications)
    return jsonify({"message": "Patient inserted successfully"}), 200
@app.route('/insert_doctor', methods=['POST'])
def insert_doctor_route():
    data = request.get_json()
    doc_id = data['doc_id']
    doc_name = data['doc_name']
    age = data['age']
    contact = data['contact']
    specialization = data['specialization']
    patients = data['patients']
    schedule = data['schedule']

    insert_doctor(doc_id, doc_name, age, contact, specialization, patients, schedule)
    return jsonify({"message": "Doctor inserted successfully"}), 200
@app.route('/insert_comment', methods=['POST'])
def insert_comment_route():
    data = request.get_json()
    thread_id = data['thread_id']
    com_id = data['com_id']
    content = data['content']
    auth_id = data['auth_id']

    insert_comment(thread_id, com_id, content, auth_id)
    return jsonify({"message": "Comment inserted successfully"}), 200