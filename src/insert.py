from flask import Flask, request, jsonify
import mysql.connector
from flask_bcrypt import Bcrypt
from flask_cors import CORS  # Import CORS
import json
from headers.people import Patient, Doctor
from headers.comments import Comment, Response

app = Flask(__name__)
bcrypt = Bcrypt(app)
CORS(app)  # Enable CORS for all routes

# Database configuration
db_config = {
    'host': 'localhost',
#    'user': 'root',
#    'password': 'password',
#    'database': 'health' 
    'user': 'charles',
    'password': 'supersecret',
    'database': 'health'
}
def initdb():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        # Drop existing tables to ensure schema changes are applied
        cursor.execute("DROP TABLE IF EXISTS patients")
        cursor.execute("DROP TABLE IF EXISTS doctors")
        cursor.execute("DROP TABLE IF EXISTS comments")
        
        # Create patients table with authentication fields
        cursor.execute('''CREATE TABLE IF NOT EXISTS patients(
            pat_id INT PRIMARY KEY,
            pat_name VARCHAR(255),
            age INT,
            contact VARCHAR(255),
            allergies TEXT,
            medications TEXT,
            username VARCHAR(255) UNIQUE,
            email VARCHAR(255) UNIQUE,
            password_hash VARCHAR(255)
        )''')
        
        # Create doctors table with authentication fields
        cursor.execute('''CREATE TABLE IF NOT EXISTS doctors(
            doc_id INT PRIMARY KEY,
            doc_name VARCHAR(255),
            age INT,
            contact VARCHAR(255),
            specialization TEXT,
            patients TEXT,
            schedule TEXT,
            username VARCHAR(255) UNIQUE,
            email VARCHAR(255) UNIQUE,
            password_hash VARCHAR(255)
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

def insert_patient(pat_id, pat_name, age, contact, allergies, medications, username=None, email=None, password=None):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        # Hash password if provided
        password_hash = None
        if password:
            password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
            
        cursor.execute('''INSERT INTO patients 
                        (pat_id, pat_name, age, contact, allergies, medications, username, email, password_hash) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)''', 
                        (pat_id, pat_name, age, contact, allergies, medications, username, email, password_hash))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return False

def insert_doctor(doc_id, doc_name, age, contact, specialization, patients, schedule, username=None, email=None, password=None):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        # Hash password if provided
        password_hash = None
        if password:
            password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
            
        cursor.execute('''INSERT INTO doctors 
                        (doc_id, doc_name, age, contact, specialization, patients, schedule, username, email, password_hash) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''', 
                        (doc_id, doc_name, age, contact, specialization, patients, schedule, username, email, password_hash))
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

@app.route('/api/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    user_type = data.get('user_type')  # 'patient' or 'doctor'
    
    # Validate required fields
    if not all([username, email, password, user_type]):
        return jsonify({"message": "Missing required fields"}), 400
        
    if user_type not in ['patient', 'doctor']:
        return jsonify({"message": "Invalid user type. Must be 'patient' or 'doctor'"}), 400
    
    # Check if username or email already exists
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        # Check in patients table
        cursor.execute("SELECT * FROM patients WHERE username = %s OR email = %s", (username, email))
        patient_result = cursor.fetchone()
        
        # Check in doctors table
        cursor.execute("SELECT * FROM doctors WHERE username = %s OR email = %s", (username, email))
        doctor_result = cursor.fetchone()
        
        if patient_result or doctor_result:
            cursor.close()
            conn.close()
            return jsonify({"message": "Username or email already exists"}), 409
        
        # Create a new user
        if user_type == 'patient':
            # Generate a new pat_id (you might want a better strategy)
            cursor.execute("SELECT MAX(pat_id) FROM patients")
            max_id = cursor.fetchone()[0]
            new_id = 1 if max_id is None else max_id + 1
            
            # Insert new patient
            success = insert_patient(
                pat_id=new_id,
                pat_name=data.get('name', f"User_{username}"),
                age=data.get('age', 0),
                contact=data.get('contact', ''),
                allergies=data.get('allergies', ''),
                medications=data.get('medications', ''),
                username=username,
                email=email,
                password=password
            )
        else:  # doctor
            # Generate a new doc_id
            cursor.execute("SELECT MAX(doc_id) FROM doctors")
            max_id = cursor.fetchone()[0]
            new_id = 1 if max_id is None else max_id + 1
            
            # Insert new doctor
            success = insert_doctor(
                doc_id=new_id,
                doc_name=data.get('name', f"Dr_{username}"),
                age=data.get('age', 0),
                contact=data.get('contact', ''),
                specialization=json.dumps(data.get('specialization', {})),
                patients=json.dumps([]),
                schedule=json.dumps({}),
                username=username,
                email=email,
                password=password
            )
        
        cursor.close()
        conn.close()
        
        if success:
            return jsonify({
                "message": f"{user_type.capitalize()} account created successfully",
                "user_id": new_id
            }), 201
        else:
            return jsonify({"message": f"Failed to create {user_type} account"}), 500
            
    except mysql.connector.Error as err:
        print(f"Database error during signup: {err}")
        return jsonify({"message": f"Database error: {str(err)}"}), 500

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not all([username, password]):
        return jsonify({"message": "Username and password are required"}), 400
        
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        
        # Check patients table first
        cursor.execute("SELECT * FROM patients WHERE username = %s", (username,))
        user = cursor.fetchone()
        user_type = 'patient'
        
        # If not found in patients, check doctors table
        if not user:
            cursor.execute("SELECT * FROM doctors WHERE username = %s", (username,))
            user = cursor.fetchone()
            user_type = 'doctor'
            
        cursor.close()
        conn.close()
        
        if not user:
            return jsonify({"message": "Invalid username or password"}), 401
            
        # Verify password
        if bcrypt.check_password_hash(user['password_hash'], password):
            # Authentication successful, create a simplified user response
            user_response = {
                "id": user['pat_id'] if user_type == 'patient' else user['doc_id'],
                "username": user['username'],
                "email": user['email'],
                "user_type": user_type,
                "name": user['pat_name'] if user_type == 'patient' else user['doc_name']
            }
            
            return jsonify({
                "message": "Login successful",
                "user": user_response
            }), 200
        else:
            return jsonify({"message": "Invalid username or password"}), 401
            
    except mysql.connector.Error as err:
        print(f"Database error during login: {err}")
        return jsonify({"message": f"Database error: {str(err)}"}), 500

@app.route('/api/users', methods=['GET'])
def list_users():
    """Endpoint to list all users for verification purposes"""
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        
        # Get patients
        cursor.execute("SELECT pat_id, pat_name, username, email FROM patients")
        patients = cursor.fetchall()
        
        # Get doctors
        cursor.execute("SELECT doc_id, doc_name, username, email FROM doctors")
        doctors = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return jsonify({
            "patients": patients,
            "doctors": doctors
        }), 200
    except mysql.connector.Error as err:
        print(f"Database error while listing users: {err}")
        return jsonify({"message": f"Database error: {str(err)}"}), 500

@app.route('/', methods=['GET'])
def index():
    """Homepage route to confirm the server is running"""
    return jsonify({
        "status": "ok",
        "message": "Flask API server is running",
        "endpoints": {
            "insert_patient": "/insert_patient",
            "insert_doctor": "/insert_doctor", 
            "insert_comment": "/insert_comment",
            "signup": "/api/signup",
            "login": "/api/login"
        }
    })

# Initialize database on startup
initdb()

if __name__ == "__main__":
    print("Starting Flask server on http://localhost:5000")
    app.run(debug=True, host='0.0.0.0')