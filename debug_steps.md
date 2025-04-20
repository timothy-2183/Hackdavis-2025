# Debugging Steps for "Connection Refused" Error

The error `HTTPConnectionPool(host='localhost', port=5000): Max retries exceeded with url: /insert_patient (Caused by NewConnectionError('<urllib3.connection.HTTPConnection object at 0x7f253ab1b700>: Failed to establish a new connection: [Errno 111] Connection refused'))` indicates that your test script cannot connect to the Flask server.

Follow these steps to troubleshoot and fix the issue:

## Step 1: Check if the Flask Server is Running

The most common cause of this error is that the Flask server is not running when you try to run the test script.

1. First, make sure the Flask server is running:
   ```
   cd src
   python insert.py
   ```

2. You should see output like:
   ```
   Starting Flask server on http://localhost:5000
   * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
   * Restarting with stat
   * Debugger is active!
   * Debugger PIN: xxx-xxx-xxx
   ```

3. Verify the server is accessible by opening a web browser and navigating to `http://localhost:5000`
   - You should see a JSON response with server status information

## Step 2: Test Connectivity

1. Use the server check script to verify connectivity:
   ```
   python src/server_check.py
   ```

2. If the server is not running, the script will attempt to start it

## Step 3: Check for Network/Firewall Issues

1. Make sure no firewall is blocking port 5000
2. If you're running the server in a container or VM, ensure port forwarding is set up correctly

## Step 4: Check Database Configuration

1. Verify that your MySQL credentials are correct in the `db_config` variable in `src/insert.py`
2. Make sure the MySQL server is running:
   ```
   sudo systemctl status mysql  # Linux
   # or
   sc query mysql               # Windows
   ```

## Step 5: Run in Separate Terminals

1. Use two separate terminal windows:
   - Terminal 1: Run the Flask server with `python src/insert.py`
   - Terminal 2: Run the test script with `python src/test_flask_app.py`

## Step 6: Check for Error Messages

1. Look for error messages in the Flask server terminal
2. Common issues include:
   - MySQL connection errors
   - Port conflicts (another service using port 5000)
   - Missing dependencies

## Step 7: Install Required Packages

Ensure all dependencies are installed:
```
pip install flask mysql-connector-python requests
```

## Step 8: Try a Different Port

If port 5000 is blocked or in use:

1. Modify the Flask app to use a different port:
   ```python
   app.run(debug=True, host='0.0.0.0', port=5001)
   ```

2. Update your test script to use the new port:
   ```python
   base_url = "http://localhost:5001"
   ```

## Troubleshooting Additional Issues

If you're still having trouble:

1. Check server logs for detailed error messages
2. Run `netstat -tuln | grep 5000` to check if something else is using the port
3. Temporarily disable your firewall to test if it's blocking connections 