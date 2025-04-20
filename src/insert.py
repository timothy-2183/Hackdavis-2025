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
        
        # Create tables if they don't exist (don't drop existing tables)
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

def populate_sample_data():
    """Populate the database with sample data if tables are empty"""
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        # Check if patients table is empty
        cursor.execute("SELECT COUNT(*) FROM patients")
        patient_count = cursor.fetchone()[0]
        
        # Check if doctors table is empty
        cursor.execute("SELECT COUNT(*) FROM doctors")
        doctor_count = cursor.fetchone()[0]
        
        # Check if comments table is empty
        cursor.execute("SELECT COUNT(*) FROM comments")
        comment_count = cursor.fetchone()[0]
        
        # Only populate if tables are empty
        if patient_count == 0:
            print("Populating sample patients...")
            # Insert sample patients
            patients = [
                (1, "John Doe", 35, "555-123-4567", "Penicillin, Pollen", "Lisinopril, Metformin", "john_doe", "john@example.com", bcrypt.generate_password_hash("password123").decode('utf-8')),
                (2, "Jane Smith", 28, "555-987-6543", "Shellfish, Latex", "Zyrtec", "jane_smith", "jane@example.com", bcrypt.generate_password_hash("password123").decode('utf-8')),
                (3, "Bob Johnson", 45, "555-567-8901", "None", "Lipitor, Aspirin", "bob_johnson", "bob@example.com", bcrypt.generate_password_hash("password123").decode('utf-8'))
            ]
            
            cursor.executemany('''INSERT INTO patients 
                              (pat_id, pat_name, age, contact, allergies, medications, username, email, password_hash) 
                              VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)''', patients)
        
        if doctor_count == 0:
            print("Populating sample doctors...")
            # Insert sample doctors
            doctors = [
                (901, "Dr. Sarah Wilson", 42, "555-222-3333", json.dumps({"Cardiology": 10, "Internal Medicine": 15}), json.dumps([1, 3]), json.dumps({"Monday": ["9:00", "10:00", "11:00"], "Wednesday": ["13:00", "14:00", "15:00"]}), "dr_wilson", "sarah@example.com", bcrypt.generate_password_hash("password123").decode('utf-8')),
                (902, "Dr. Michael Chen", 38, "555-444-5555", json.dumps({"Pediatrics": 8, "Family Medicine": 12}), json.dumps([2]), json.dumps({"Tuesday": ["9:00", "10:00", "11:00"], "Thursday": ["13:00", "14:00", "15:00"]}), "dr_chen", "michael@example.com", bcrypt.generate_password_hash("password123").decode('utf-8'))
            ]
            
            cursor.executemany('''INSERT INTO doctors 
                              (doc_id, doc_name, age, contact, specialization, patients, schedule, username, email, password_hash) 
                              VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''', doctors)
        
        if comment_count == 0:
            print("Populating sample conversations...")
            # Insert sample conversations
            
            # Conversation 1: Chest pain
            conversation1 = [
                (1, 1, "I've been experiencing chest pain when I exercise. It feels like pressure and sometimes radiates to my left arm. It usually goes away after I rest for a few minutes.", json.dumps([0, 1])),
                (1, 2, "I appreciate you reaching out about these symptoms. Chest pain that radiates to the arm and is triggered by exertion could indicate a cardiovascular issue. Have you noticed any shortness of breath, dizziness, or sweating when this happens?", json.dumps([1, 901])),
                (1, 3, "Yes, I do get a bit short of breath and sometimes feel lightheaded. It's been happening more frequently over the past two weeks.", json.dumps([0, 1])),
                (1, 4, "This should be evaluated promptly. Please schedule an appointment with me this week. In the meantime, avoid strenuous exercise, and if the pain becomes severe, lasts longer than usual, or occurs at rest, please go to the emergency room immediately.", json.dumps([1, 901]))
            ]
            
            # Conversation 2: Skin rash
            conversation2 = [
                (2, 1, "I've developed an itchy rash on my arms and neck after starting a new medication for allergies. It's red and bumpy.", json.dumps([0, 2])),
                (2, 2, "Thank you for letting me know. This sounds like it could be an allergic reaction to your new medication. What's the name of the medication, and when did you start taking it?", json.dumps([1, 902])),
                (2, 3, "It's called Allerdryl. I started it 3 days ago, and the rash appeared yesterday.", json.dumps([0, 2])),
                (2, 4, "Please stop taking Allerdryl immediately. This is likely an allergic reaction. Take an over-the-counter antihistamine like Benadryl to help with the itching, and apply a hydrocortisone cream to the affected areas. If you develop any difficulty breathing or swelling of your face or throat, go to the emergency room right away. Let's schedule an appointment for next week to check on your condition and discuss alternative allergy medications.", json.dumps([1, 902]))
            ]
            
            # Conversation 3: Headaches
            conversation3 = [
                (3, 1, "I've been having frequent headaches, almost daily for the past month. They're usually worse in the afternoon and feel like pressure around my temples and forehead.", json.dumps([0, 3])),
                (3, 2, "I'm sorry to hear you're experiencing these frequent headaches. Let's gather more information to understand what might be causing them. Are you experiencing any other symptoms like vision changes, nausea, or sensitivity to light? Also, have you noticed any particular triggers?", json.dumps([1, 901])),
                (3, 3, "No vision changes or nausea, but I do notice they get worse when I've been looking at my computer screen for a long time. I've also been sleeping poorly lately due to stress at work.", json.dumps([0, 3])),
                (3, 4, "Based on your description, these could be tension headaches, possibly exacerbated by eye strain and stress. Try the following: Take regular breaks from screen time (follow the 20-20-20 rule: every 20 minutes, look at something 20 feet away for 20 seconds), improve your sleep hygiene, and consider stress-reduction techniques like meditation or gentle exercise. Over-the-counter pain relievers like ibuprofen may help when needed. If these measures don't provide relief within two weeks, or if your headaches worsen, please schedule an appointment for a more thorough evaluation.", json.dumps([1, 901]))
            ]
            
            all_conversations = conversation1 + conversation2 + conversation3
            cursor.executemany('''INSERT INTO comments 
                               (thread_id, com_id, content, auth_id) 
                               VALUES (%s, %s, %s, %s)''', all_conversations)
        
        conn.commit()
        cursor.close()
        conn.close()
        print("Sample data population completed")
    except mysql.connector.Error as err:
        print(f"Error populating sample data: {err}")

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

def insert_comment(id, content, auth_id):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        com_id = 1

        if id == 0:
            # If the thread is new, set the thread_id to the next available id
            cursor.execute("SELECT MAX(thread_id) FROM comments")
            # Get the maximum thread_id from the comments table
            # If no comments exist, set thread_id to 1
            max_thread_id = cursor.fetchone()[0]
            thread_id = 1 if max_thread_id is None else max_thread_id + 1
        else:
            thread_id = id 
            # Insert the comment into the comments table
            cursor.execute("SELECT MAX(com_id) FROM comments WHERE thread_id = %s", (id))
            # Get the maximum com_id for the specified thread_id
            max_com_id = cursor.fetchone()[0]
            # If no comments exist for this thread, set com_id to 1
            com_id = 1 if max_com_id is None else max_com_id + 1
            # Insert the comment into the comments table
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
    pat_id = '0'+ data['pat_id']
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
    doc_id = '9'+ data['doc_id']
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
    # If the thread is new, the id getting passed will be 0 and the comment id will be 1, otherwise it will correspondend to the thread id
    data = request.get_json()
    id = data['id']
    content = data['content']
    auth_id = data['auth_id']

    # The json here is a bit change, the it takes ID, content and the id of the patient,

    # this way we have less variables to pass around
    success = insert_comment(id, content, auth_id)
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
populate_sample_data()

if __name__ == "__main__":
    print("Starting Flask server on http://localhost:5000")
    app.run(debug=True, host='0.0.0.0')


def view_patient(id):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        
        # Fetch patient details
        cursor.execute("SELECT * FROM patients WHERE pat_id = %s", (id,))
        patient = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if patient:
            return jsonify(patient), 200
        else:
            return jsonify({"message": "Patient not found"}), 404
    except mysql.connector.Error as err:
        print(f"Database error while fetching patient: {err}")
        return jsonify({"message": f"Database error: {str(err)}"}), 500
    
def view_doctor(id):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        
        # Fetch doctor details
        cursor.execute("SELECT * FROM doctors WHERE doc_id = %s", (id,))
        doctor = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if doctor:
            return jsonify(doctor), 200
        else:
            return jsonify({"message": "Doctor not found"}), 404
    except mysql.connector.Error as err:
        print(f"Database error while fetching doctor: {err}")
        return jsonify({"message": f"Database error: {str(err)}"}), 500

def get_doctor_name(id):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        
        # Fetch doctor name
        cursor.execute("SELECT doc_name FROM doctors WHERE doc_id = %s", (id,))
        result = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if result:
            return result['doc_name']
        else:
            return ''
    except mysql.connector.Error as err:
        print(f"Database error while fetching doctor name: {err}")
        return ''
def get_patient_name(id):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
                
        # Fetch patient name
        cursor.execute("SELECT pat_name FROM patients WHERE pat_id = %s", (id,))
        result = cursor.fetchone()
                
        cursor.close()
        conn.close()
        if result:
            return result['pat_name']
        else:
            return ''
    except mysql.connector.Error as err:
        print(f"Database error while fetching patient name: {err}")
        return ''
# Different function, returns a super long string instead of a json object
def view_conversation(id):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        
        # Fetch conversation details
        cursor.execute("SELECT * FROM comments WHERE thread_id = %s", (id,))
        conversation = cursor.fetchall()

        
        string_ret = ""
        patientname = ""
        doctorname = ""
        if conversation:
            for comment in conversation:
                if json.loads(comment['auth_id'])[0]==0:
                    patientname = get_patient_name(json.loads(comment['auth_id'])[1])
                if json.loads(comment['auth_id'])[0]==1:
                    doctorname = get_doctor_name(json.loads(comment['auth_id'])[1])

            for comment in conversation:
            # Convert JSON strings back to Python objects
                if json.loads(comment['auth_id'])[0]==0:
                    string_ret += f"Patient {patientname}: {comment['content']}\n"
                elif json.loads(comment['auth_id'])[0]==1:
                    string_ret += f"Doctor {doctorname}: {comment['content']}\n"
                else:
                    string_ret += f"AI: {comment['content']}\n"

            cursor.close()
            conn.close()
        
            return conversation
        else:
            cursor.close()
            conn.close()
        
            return "message Conversation not found"
        # Iterate through the conversation and format the output
        
    except mysql.connector.Error as err:
        print(f"Database error while fetching conversation: {err}")
        return jsonify({"message": f"Database error: {str(err)}"}), 500

@app.route('/api/patient/medical/<int:patient_id>', methods=['GET'])
def get_patient_medical_data(patient_id):
    """Get a patient's medical data including allergies and medications"""
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        
        # Fetch patient details
        cursor.execute("SELECT pat_id, pat_name, age, allergies, medications FROM patients WHERE pat_id = %s", (patient_id,))
        patient = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if patient:
            return jsonify(patient), 200
        else:
            return jsonify({"message": "Patient not found"}), 404
    except mysql.connector.Error as err:
        print(f"Database error while fetching patient medical data: {err}")
        return jsonify({"message": f"Database error: {str(err)}"}), 500

@app.route('/api/conversation/<int:thread_id>', methods=['GET'])
def get_conversation(thread_id):
    """Get a conversation thread with messages"""
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        
        # Fetch conversation details
        cursor.execute("SELECT * FROM comments WHERE thread_id = %s ORDER BY com_id", (thread_id,))
        conversation = cursor.fetchall()
        
        if not conversation:
            cursor.close()
            conn.close()
            return jsonify({"message": "Conversation not found"}), 404
        
        cursor.close()
        conn.close()
        return jsonify({
            "thread_id": thread_id,
            "conversation": conversation
        }), 200
        
    except mysql.connector.Error as err:
        print(f"Database error while fetching conversation: {err}")
        return jsonify({"message": f"Database error: {str(err)}"}), 500

@app.route('/api/conversation/<int:thread_id>/analyze', methods=['POST'])
def analyze_conversation(thread_id):
    """Analyze a conversation thread with Claude's importance() function"""
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        
        # Fetch conversation details
        cursor.execute("SELECT * FROM comments WHERE thread_id = %s ORDER BY com_id", (thread_id,))
        conversation = cursor.fetchall()
        
        if not conversation:
            cursor.close()
            conn.close()
            return jsonify({"message": "Conversation not found"}), 404
        
        # Format the conversation for AI processing
        conversation_text = ""
        for comment in conversation:
            auth_id = json.loads(comment['auth_id'])
            if auth_id[0] == 0:  # Patient
                patient_name = get_patient_name(auth_id[1])
                conversation_text += f"Patient {patient_name}: {comment['content']}\n"
            elif auth_id[0] == 1:  # Doctor
                doctor_name = get_doctor_name(auth_id[1])
                conversation_text += f"Doctor {doctor_name}: {comment['content']}\n"
            else:  # AI
                conversation_text += f"AI: {comment['content']}\n"
        
        # Generate AI summary and tags using Claude
        from headers.prompter import importance
        ai_analysis = importance(conversation_text)
        
        # Get the next comment ID for this thread
        cursor.execute("SELECT MAX(com_id) FROM comments WHERE thread_id = %s", (thread_id,))
        max_com_id = cursor.fetchone()['MAX(com_id)']
        next_com_id = 1 if max_com_id is None else max_com_id + 1
        
        # Add the analysis as a comment in the thread
        ai_auth_id = json.dumps([2])  # 2 indicates AI
        cursor.execute(
            "INSERT INTO comments (thread_id, com_id, content, auth_id) VALUES (%s, %s, %s, %s)",
            (thread_id, next_com_id, f"ANALYSIS: {ai_analysis}", ai_auth_id)
        )
        conn.commit()
        
        # Format the response
        response = {
            "thread_id": thread_id,
            "conversation": conversation,
            "ai_analysis": ai_analysis
        }
        
        cursor.close()
        conn.close()
        return jsonify(response), 200
        
    except mysql.connector.Error as err:
        print(f"Database error while analyzing conversation: {err}")
        return jsonify({"message": f"Database error: {str(err)}"}), 500

@app.route('/api/patient/symptoms', methods=['POST'])
def submit_patient_symptoms():
    """Submit patient symptoms and get AI analysis"""
    data = request.get_json()
    patient_id = data.get('patient_id')
    allergies = data.get('allergies', '')
    medications = data.get('medications', '')
    symptoms = data.get('symptoms', '')
    
    if not patient_id:
        return jsonify({"message": "Patient ID is required"}), 400
    
    try:
        # Update patient allergies and medications if provided
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        if allergies or medications:
            update_query = "UPDATE patients SET"
            update_params = []
            
            if allergies:
                update_query += " allergies = %s"
                update_params.append(allergies)
                
            if medications:
                if allergies:  # If we already added allergies, add a comma
                    update_query += ","
                update_query += " medications = %s"
                update_params.append(medications)
                
            update_query += " WHERE pat_id = %s"
            update_params.append(patient_id)
            
            cursor.execute(update_query, update_params)
            conn.commit()
        
        # Create a new conversation thread with the symptoms
        prompt = f"Patient allergies: {allergies}\nPatient medications: {medications}\nPatient symptoms: {symptoms}"
        
        # Get AI analysis
        from headers.prompter import ask_claude
        ai_response = ask_claude(prompt)
        
        # Create a new thread for this conversation
        cursor.execute("SELECT MAX(thread_id) FROM comments")
        max_thread_id = cursor.fetchone()[0]
        thread_id = 1 if max_thread_id is None else max_thread_id + 1
        
        # Insert patient symptom as first comment (com_id=1)
        # auth_id format: [0, patient_id] where 0 indicates patient
        patient_auth_id = json.dumps([0, int(patient_id)])
        cursor.execute(
            "INSERT INTO comments (thread_id, com_id, content, auth_id) VALUES (%s, %s, %s, %s)",
            (thread_id, 1, symptoms, patient_auth_id)
        )
        
        # Insert AI response as second comment (com_id=2)
        # auth_id format: [2] where 2 indicates AI
        ai_auth_id = json.dumps([2])
        cursor.execute(
            "INSERT INTO comments (thread_id, com_id, content, auth_id) VALUES (%s, %s, %s, %s)",
            (thread_id, 2, ai_response, ai_auth_id)
        )
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({
            "message": "Symptoms submitted successfully",
            "thread_id": thread_id,
            "ai_response": ai_response
        }), 201
        
    except mysql.connector.Error as err:
        print(f"Database error during symptom submission: {err}")
        return jsonify({"message": f"Database error: {str(err)}"}), 500
    except Exception as e:
        print(f"Error submitting symptoms: {e}")
        return jsonify({"message": f"Error: {str(e)}"}), 500

