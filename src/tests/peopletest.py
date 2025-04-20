import unittest
from io import StringIO
import sys
from people import Patient, Doctor
# Assuming your classes are in a file called healthcare.py
# from healthcare import Patient, Doctor

class Patient():
    def __init__(self, name, age, contact, allergies, medications):
        self.name = name
        self.age = age
        self.contact = contact
        self.medical_history = []
        self.allergies = allergies
        self.medications = medications
        self.diagnosis = None

    def add_diagnosis(self, diagnosis):
        self.diagnosis = diagnosis

class Doctor():
    def __init__(self, name, age, contact, specialization, patients, schedule):
        self.name = name
        self.contact = contact
        self.specialization = specialization
        self.patients = patients
        self.schedule = schedule

    def add_patient(self, patient):
        self.patients.append(patient)

    def add_medical_record(self, patient, date, diagnosis, treatment):
        if patient in self.patients:
            record = {
                'date': date,
                'diagnosis': diagnosis,
                'treatment': treatment
            }
            patient.medical_history.append(record)

    def view_medical_history(self, patient):
        if patient in self.patients:
            for record in patient.medical_history:
                print(f"Date: {record['date']}, Diagnosis: {record['diagnosis']}, Treatment: {record['treatment']}")
        else:
            print("Patient not found.")


class TestHealthSystem(unittest.TestCase):

    def setUp(self):
        self.patient1 = Patient("John Doe", 30, "123456789", ["Peanuts"], ["Aspirin"])
        self.doctor1 = Doctor("Dr. Smith", 45, "987654321", {"Cardiology": 10}, [], {})
        self.doctor1.add_patient(self.patient1)

    def test_add_diagnosis(self):
        self.patient1.add_diagnosis("Hypertension")
        self.assertEqual(self.patient1.diagnosis, "Hypertension")

    def test_add_medical_record(self):
        self.doctor1.add_medical_record(self.patient1, "2024-04-10", "Flu", "Rest + Hydration")
        self.assertEqual(len(self.patient1.medical_history), 1)
        self.assertEqual(self.patient1.medical_history[0]['diagnosis'], "Flu")

    def test_view_medical_history_output(self):
        self.doctor1.add_medical_record(self.patient1, "2024-04-10", "Flu", "Rest + Hydration")
        captured_output = StringIO()
        sys.stdout = captured_output
        self.doctor1.view_medical_history(self.patient1)
        sys.stdout = sys.__stdout__
        self.assertIn("Diagnosis: Flu", captured_output.getvalue())

    def test_patient_not_found(self):
        new_patient = Patient("Jane Doe", 28, "999888777", [], [])
        captured_output = StringIO()
        sys.stdout = captured_output
        self.doctor1.view_medical_history(new_patient)
        sys.stdout = sys.__stdout__
        self.assertIn("Patient not found", captured_output.getvalue())


if __name__ == '__main__':
    unittest.main()
