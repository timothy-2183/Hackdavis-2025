import requests
import json

def test_flask_app():
    base_url = "http://localhost:5000"
    
    print("Testing Flask API with MySQL backend")
    print("Make sure MySQL is running and configured properly in src/insert.py")
    print("Ensure database credentials are correct before running this test\n")
    
    
    # Test patient insertion
    patient_data = {
        "pat_id": 1,
        "pat_name": "John Doe",
        "age": 35,
        "contact": "john.doe@example.com",
        "allergies": "Penicillin",
        "medications": "None"
    }
    
    # Test doctor insertion
    doctor_data = {
        "doc_id": 1,
        "doc_name": "Dr. Jane Smith",
        "age": 45,
        "contact": "dr.smith@example.com",
        "specialization": "Cardiology",
        "patients": "[]",
        "schedule": "{}"
    }
    
    # Test comment insertion
    comment_data = {
        "thread_id": 1,
        "com_id": 1,
        "content": "Patient reports chest pain",
        "auth_id": "1"
    }
    
    try:
        # Test patient insertion
        print("Testing patient insertion...")
        patient_response = requests.post(
            f"{base_url}/insert_patient", 
            json=patient_data, 
            headers={"Content-Type": "application/json"}
        )
        print(f"Patient insertion response: {patient_response.status_code}")
        print(f"Response: {patient_response.json()}")
        
        # Test doctor insertion
        print("\nTesting doctor insertion...")
        doctor_response = requests.post(
            f"{base_url}/insert_doctor", 
            json=doctor_data, 
            headers={"Content-Type": "application/json"}
        )
        print(f"Doctor insertion response: {doctor_response.status_code}")
        print(f"Response: {doctor_response.json()}")
        
        # Test comment insertion
        print("\nTesting comment insertion...")
        comment_response = requests.post(
            f"{base_url}/insert_comment", 
            json=comment_data, 
            headers={"Content-Type": "application/json"}
        )
        print(f"Comment insertion response: {comment_response.status_code}")
        print(f"Response: {comment_response.json()}")
        
        print("\nAll tests completed successfully!")
        
    except Exception as e:
        print(f"Error during testing: {e}")
        
if __name__ == "__main__":
    test_flask_app() 