# Flask Patient Management System with MySQL

This application provides a RESTful API using Flask for managing patients, doctors, and comments in a medical system. Data is stored in a MySQL database.

## Prerequisites

- Python 3.x
- MySQL server
- Required Python packages:
  - Flask
  - mysql-connector-python
  - requests (for testing)

## Setup

1. Install required packages:
   ```
   pip install flask mysql-connector-python requests
   ```

2. Configure your MySQL database:
   - Create a new database for the application
   - Update the database configuration in `src/insert.py`:
     ```python
     db_config = {
         'host': 'localhost',
         'user': 'your_username',  # Replace with your MySQL username
         'password': 'your_password',  # Replace with your MySQL password
         'database': 'your_database'  # Replace with your database name
     }
     ```

## Running the Application

1. Start the Flask server:
   ```
   cd src
   python insert.py
   ```
   
   The server will run on http://localhost:5000 by default.

2. Test the API (optional):
   ```
   python test_flask_app.py
   ```

## API Endpoints

- **POST /insert_patient** - Add a new patient
- **POST /insert_doctor** - Add a new doctor
- **POST /insert_comment** - Add a new comment

## Sample Requests

### Add a Patient
```
POST /insert_patient
Content-Type: application/json

{
  "pat_id": 1,
  "pat_name": "John Doe",
  "age": 35,
  "contact": "john.doe@example.com",
  "allergies": "Penicillin",
  "medications": "None"
}
```

### Add a Doctor
```
POST /insert_doctor
Content-Type: application/json

{
  "doc_id": 1,
  "doc_name": "Dr. Jane Smith",
  "age": 45,
  "contact": "dr.smith@example.com",
  "specialization": "Cardiology",
  "patients": "[]",
  "schedule": "{}"
}
```

### Add a Comment
```
POST /insert_comment
Content-Type: application/json

{
  "thread_id": 1,
  "com_id": 1,
  "content": "Patient reports chest pain",
  "auth_id": "1"
}
``` 