import os
import sys
import subprocess
import time
import requests

def check_server_running():
    """Check if the Flask server is running on localhost:5000"""
    try:
        response = requests.get("http://localhost:5000")
        print(f"Server is running. Status code: {response.status_code}")
        return True
    except requests.exceptions.ConnectionError:
        print("Server is not running on localhost:5000")
        return False

def start_server():
    """Start the Flask server"""
    print("Attempting to start Flask server...")
    
    # Ensure we're in the src directory (or adjust path as needed)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    try:
        # Use a non-blocking process to start the server
        if sys.platform.startswith('win'):
            # Windows command
            subprocess.Popen(["start", "python", "insert.py"], 
                            shell=True, 
                            cwd=script_dir)
        else:
            # Linux/Mac command
            subprocess.Popen(["python3", "insert.py"], 
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            cwd=script_dir)
        
        print("Server start command issued. Waiting for server to become available...")
        
        # Give the server time to start
        max_retries = 5
        for i in range(max_retries):
            time.sleep(3)  # Wait 3 seconds between checks
            print(f"Check {i+1}/{max_retries}...")
            if check_server_running():
                print("Server started successfully!")
                return True
        
        print("Server failed to start after multiple attempts")
        return False
    
    except Exception as e:
        print(f"Error trying to start server: {e}")
        return False

if __name__ == "__main__":
    if not check_server_running():
        print("\nAttempting to start the server...")
        if start_server():
            print("\nNow you can run test_flask_app.py in a separate terminal")
        else:
            print("\nTroubleshooting tips:")
            print("1. Make sure mysql-connector-python is installed: pip install mysql-connector-python")
            print("2. Check database configuration in insert.py")
            print("3. Verify MySQL server is running")
            print("4. Try running insert.py directly to see error messages")
    else:
        print("\nServer is already running. You can run test_flask_app.py now.") 