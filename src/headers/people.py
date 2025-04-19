
class Patient():
    def __init__(ID, self, name, age, contact, allergies, medications):
        self.ID = ID
        self.name = name
        self.age = age
        self.contact = contact
        self.medical_history = []
        self.allergies = allergies
        self.medications = medications
        self.diagnosis = None
    def add_diagnosis(self, diagnosis):
        self.diagnosis = diagnosis
    # Medical History Operations for the Patients
    def view_medical_history(self, patient):
        if patient in self.patients:
            for record in patient.medical_history:
                print(f"Date: {record['date']}, Diagnosis: {record['diagnosis']}, Treatment: {record['treatment']}")
        else:
            print("Patient not found.")
    def add_medical_record(self, patient, date, diagnosis, treatment):
        if patient in self.patients:
            record = {
                'date': date,
                'diagnosis': diagnosis,
                'treatment': treatment
            }
            patient.medical_history.append(record)
        else:
            print("Patient not found.")
    def remove_medical_record(self, patient, record):
        if patient in self.patients:
            if record in patient.medical_history:
                patient.medical_history.remove(record)
            else:
                print("Record not found.")
        else:
            print("Patient not found.")

class Doctor():
    def __init__(self, name, age, contact, specialization, patients, schedule):
        self.name = name
        self.contact = contact
        self.specialization = specialization  # Dictionary of {string: int}
        self.patients = patients  # List of Patient objects
        self.schedule = schedule  # Dictionary of {string: list of time slots available in hourly increments}
    # Patient Operations for the Doctors
    def add_patient(self, patient):
        self.patients.append(patient)
    def remove_patient(self, patient):
        if patient in self.patients:
            self.patients.remove(patient)
        else:
            print("Patient not found.")
    def view_patients(self):
        for patient in self.patients:
            print(f"Name: {patient.name}, Age: {patient.age}, Contact: {patient.contact}, Allergies: {patient.allergies}, Medications: {patient.medications}")
    # Schedule Operations for the Doctors
    def view_schedule(self):
        for date, time_slots in self.schedule.items():
            print(f"Date: {date}, Available Time Slots: {', '.join(time_slots)}")
    def add_schedule(self, date, time_slots):
        if date in self.schedule:
            self.schedule[date].extend(time_slots)
        else:
            self.schedule[date] = time_slots
    def remove_schedule(self, date):
        if date in self.schedule:
            del self.schedule[date]
        else:
            print("Schedule not found.")
    # Specialization Operations for the Doctors
    def view_specialization(self):
        for specialization, years in self.specialization.items():
            print(f"Specialization: {specialization}, Years of Experience: {years}")
    def add_specialization(self, specialization, years):
        self.specialization[specialization] = years
    def remove_specialization(self, specialization):
        if specialization in self.specialization:
            del self.specialization[specialization]
        else:
            print("Specialization not found.")
    
    # Medical History Operations for the Doctors
    def view_medical_history(self, patient):
        if patient in self.patients:
            for record in patient.medical_history:
                print(f"Date: {record['date']}, Diagnosis: {record['diagnosis']}, Treatment: {record['treatment']}")
        else:
            print("Patient not found.")
    def add_medical_record(self, patient, date, diagnosis, treatment):
        if patient in self.patients:
            record = {
                'date': date,
                'diagnosis': diagnosis,
                'treatment': treatment
            }
            patient.medical_history.append(record)
        else:
            print("Patient not found.")
    def remove_medical_record(self, patient, record):
        if patient in self.patients:
            if record in patient.medical_history:
                patient.medical_history.remove(record)
            else:
                print("Record not found.")
        else:
            print("Patient not found.")
    
    # Contact Operations for the Doctors
    def view_contact(self):
        print(f"Name: {self.name}, Contact: {self.contact}")
    def update_contact(self, contact):
        self.contact = contact
    def update_name(self, name):
        self.name = name
    def update_age(self, age):
        self.age = age