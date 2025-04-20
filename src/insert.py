from flask import Flask, request, jsonify
import mysql.connector
from headers.people import Patient, Doctor
from headers.comments import Comment, Response

app = Flask(__name__)

# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'your_username',
    'password': 'your_password',
    'database': 'your_database'
}

def initdb():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        # Create patients table
        cursor.execute('''CREATE TABLE IF NOT EXISTS patients(
            pat_id INT PRIMARY KEY,
            pat_name VARCHAR(255),
            age INT,
            contact VARCHAR(255),
            allergies TEXT,
            medications TEXT
        )''')
        
        # Create doctors table
        cursor.execute('''CREATE TABLE IF NOT EXISTS doctors(
            doc_id INT PRIMARY KEY,
            doc_name VARCHAR(255),
            age INT,
            contact VARCHAR(255),
            specialization TEXT,
            patients TEXT,
            schedule TEXT
        )''')
        
        # Create comments table
        cursor.execute('''CREATE TABLE IF NOT EXISTS comments(
            thread_id INT,
            com_id INT,
            content TEXT,
            auth_id VARCHAR(255)
        )''')
        
        conn.commit()
        cursor.close()
        conn.close()
        print("Database initialized successfully")
    except mysql.connector.Error as err:
        print(f"Error initializing database: {err}")

def insert_patient(pat_id, pat_name, age, contact, allergies, medications):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO patients (pat_id, pat_name, age, contact, allergies, medications) 
                        VALUES (%s, %s, %s, %s, %s, %s)''', 
                        (pat_id, pat_name, age, contact, allergies, medications))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return False

def insert_doctor(doc_id, doc_name, age, contact, specialization, patients, schedule):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO doctors (doc_id, doc_name, age, contact, specialization, patients, schedule) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s)''', 
                        (doc_id, doc_name, age, contact, specialization, patients, schedule))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return False

def insert_comment(thread_id, com_id, content, auth_id):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO comments (thread_id, com_id, content, auth_id) 
                        VALUES (%s, %s, %s, %s)''', 
                        (thread_id, com_id, content, auth_id))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return False

@app.route('/insert_patient', methods=['POST'])
def insert_patient_route():
    data = request.get_json()
    pat_id = data['pat_id']
    pat_name = data['pat_name']
    age = data['age']
    contact = data['contact']
    allergies = data['allergies']
    medications = data['medications']

    success = insert_patient(pat_id, pat_name, age, contact, allergies, medications)
    if success:
        return jsonify({"message": "Patient inserted successfully"}), 200
    else:
        return jsonify({"message": "Failed to insert patient"}), 500

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

    success = insert_doctor(doc_id, doc_name, age, contact, specialization, patients, schedule)
    if success:
        return jsonify({"message": "Doctor inserted successfully"}), 200
    else:
        return jsonify({"message": "Failed to insert doctor"}), 500

@app.route('/insert_comment', methods=['POST'])
def insert_comment_route():
    data = request.get_json()
    thread_id = data['thread_id']
    com_id = data['com_id']
    content = data['content']
    auth_id = data['auth_id']

    success = insert_comment(thread_id, com_id, content, auth_id)
    if success:
        return jsonify({"message": "Comment inserted successfully"}), 200
    else:
        return jsonify({"message": "Failed to insert comment"}), 500

# Initialize database on startup
initdb()

if __name__ == "__main__":
    app.run(debug=True)