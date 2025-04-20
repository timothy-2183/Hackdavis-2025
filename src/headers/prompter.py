import os 
import requests
import json
import importlib.util
import sys

# Try to import config.py for API key
try:
    # First try to import from config.py
    from headers.config import CLAUDE_API_KEY
    api_key = CLAUDE_API_KEY
except ImportError:
    # If config.py doesn't exist, try environment variable
    api_key = os.environ.get("CLAUDE_API_KEY", "")
    if not api_key:
        print("WARNING: No Claude API key found in config.py or environment. Using mock responses.")

def ask_claude(prompt, model="claude-3-opus-20240229", max_tokens=1000):
    if not api_key:
        print("WARNING: No Claude API key found. Using mock response.")
        return mock_ask_claude(prompt)
        
    url = "https://api.anthropic.com/v1/messages"
    headers = {
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    }
    data = {
        "model": model,
        "max_tokens": max_tokens,
        "messages": [
            {"role": "user", "content": (prompt+ " but turn it into a more professional clinical diagnosis while being as concise as possible.")}
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()["content"][0]["text"]
    except requests.exceptions.RequestException as e:
        print("Error during request:", e)
        return mock_ask_claude(prompt)
    except KeyError:
        print("Unexpected response structure:", response.text)
        return mock_ask_claude(prompt)
    
def importance(prompt, model="claude-3-opus-20240229", max_tokens=1000):
    if not api_key:
        print("WARNING: No Claude API key found. Using mock response.")
        return mock_importance(prompt)
    
    url = "https://api.anthropic.com/v1/messages"
    headers = {
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    }
    data = {
        "model": model,
        "max_tokens": max_tokens,
        "messages": [
            {"role": "user", "content": (prompt+ ". Create short summary of the previous conversation. You are a doctor's assistant. Create 4 most relevant tags that are related to this conversation based on their symptoms (i.e. Coughing blood), area that is effected (i.e. Foot related), how urgent the matter is, 'Mild', 'Moderate', 'Urgent', 'Emergency'; and whether they are improving or needing a followup regarding further treatment.")}
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()["content"][0]["text"]
    except requests.exceptions.RequestException as e:
        print("Error during request:", e)
        return mock_importance(prompt)
    except KeyError:
        print("Unexpected response structure:", response.text)
        return mock_importance(prompt)
    
def mchat(prompt, model="claude-3-opus-20240229", max_tokens=1000):
    if not api_key:
        print("WARNING: No Claude API key found. Using mock response.")
        return mock_mchat(prompt)
    
    url = "https://api.anthropic.com/v1/messages"
    headers = {
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    }
    data = {
        "model": model,
        "max_tokens": max_tokens,
        "messages": [
            {"role": "user", "content": (prompt+ ". This is the conversation of the .")}
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()["content"][0]["text"]
    except requests.exceptions.RequestException as e:
        print("Error during request:", e)
        return mock_mchat(prompt)
    except KeyError:
        print("Unexpected response structure:", response.text)
        return mock_mchat(prompt)

# Mock response functions for testing when no API key is available
def mock_ask_claude(prompt):
    # Extract key symptoms from the prompt
    symptoms = []
    if "chest pain" in prompt.lower():
        symptoms.append("chest pain")
    if "rash" in prompt.lower():
        symptoms.append("skin rash")
    if "headache" in prompt.lower():
        symptoms.append("headache")
    if "short of breath" in prompt.lower() or "shortness of breath" in prompt.lower():
        symptoms.append("shortness of breath")
    
    # Default response if no symptoms detected
    if not symptoms:
        return "Based on the limited information provided, I recommend scheduling an appointment with your primary care physician for a thorough evaluation. Please monitor your symptoms and seek immediate medical attention if your condition worsens."
    
    # Generate appropriate mock response based on symptoms
    if "chest pain" in symptoms:
        return "The patient is presenting with chest pain that radiates to the left arm during exertion, which resolves with rest. Associated symptoms include shortness of breath and lightheadedness. These findings are concerning for potential angina pectoris or other cardiac ischemia. Recommend prompt cardiology evaluation, stress test, and ECG. Advise to avoid strenuous exercise and seek emergency care if symptoms worsen or occur at rest."
    
    if "skin rash" in symptoms:
        return "Patient presents with an erythematous, pruritic rash following initiation of new medication (Allerdryl). Distribution on arms and neck. Clinical presentation consistent with cutaneous drug reaction. Recommend discontinuation of suspected agent, symptomatic treatment with antihistamines and topical corticosteroids. Monitor for signs of systemic involvement. Follow-up in 7-10 days to assess resolution."
    
    if "headache" in symptoms:
        return "Patient reports tension-type headaches occurring daily for one month, typically in the afternoon. Bilateral frontal and temporal pressure, exacerbated by prolonged screen time and stress. No associated neurological symptoms. Assessment: Chronic tension headaches with contributing factors of digital eye strain and poor sleep hygiene. Recommend regular screen breaks, stress management techniques, and appropriate analgesia as needed. Follow-up if symptoms persist beyond two weeks despite these measures."
    
    return "Based on your described symptoms, I recommend scheduling an appointment with your healthcare provider for proper evaluation. In the meantime, monitor your symptoms carefully and seek immediate medical attention if your condition worsens significantly."

def mock_importance(prompt):
    # Extract key information from the prompt
    if "chest pain" in prompt.lower():
        return "Patient reports chest pain radiating to left arm during exercise with associated shortness of breath and lightheadedness, increasing in frequency over past two weeks. Doctor recommends prompt evaluation.\n\n#Chest pain\n#Cardiovascular symptoms\n#Urgent\n#Needs immediate follow-up"
    
    if "rash" in prompt.lower():
        return "Patient developed itchy rash on arms and neck after starting new allergy medication Allerdryl. Doctor advised to discontinue medication, use antihistamines and hydrocortisone cream, and watch for signs of severe allergic reaction.\n\n#Medication reaction\n#Skin symptoms\n#Moderate\n#Needs follow-up appointment"
    
    if "headache" in prompt.lower():
        return "Patient experiencing daily headaches for one month, worse in afternoons, described as pressure around temples and forehead. Related to screen time and poor sleep due to work stress.\n\n#Tension headaches\n#Neurological\n#Mild\n#Self-management with follow-up if persisting"
    
    return "Brief patient-doctor exchange regarding recent symptoms. Further evaluation needed.\n\n#General symptoms\n#Needs clarification\n#Undetermined urgency\n#Follow-up recommended"

def mock_mchat(prompt):
    return "This conversation shows effective communication between patient and provider. The doctor provided clear instructions and appropriate medical advice based on the patient's symptoms."