import os 
import requests
api_key = ""
def ask_claude(prompt, model="claude-3-opus-20240229", max_tokens=1000):
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
        return None
    except KeyError:
        print("Unexpected response structure:", response.text)
        return None
    
def importance(prompt, model="claude-3-opus-20240229", max_tokens=1000):
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
        return None
    except KeyError:
        print("Unexpected response structure:", response.text)
        return None
    
