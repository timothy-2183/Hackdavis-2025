import { useState } from 'react'
import './Login.css'

// API base URL for the backend
const API_BASE_URL = 'http://localhost:5000';

function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [email, setEmail] = useState('');
  const [userType, setUserType] = useState('patient');
  const [isLogin, setIsLogin] = useState(true);
  const [error, setError] = useState(''); // To display login errors

  async function handleLoginSubmit(event) {
    event.preventDefault(); // Prevent default HTML form submission
    setError(''); // Clear previous errors

    try {
      // --- Send data to your backend API ---
      const response = await fetch(`${API_BASE_URL}/api/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password }),
      });

      const data = await response.json();

      if (response.ok) {
        // Login successful!
        console.log('Login successful:', data);
        // Store user data in localStorage
        localStorage.setItem('userData', JSON.stringify(data.user));
        // Redirect to dashboard based on user type
        const userType = data.user.user_type;
        window.location.href = userType === 'doctor' ? '/dashboard' : '/getsupport';
      } else {
        // Login failed
        setError(data.message || 'Invalid username or password');
        console.error('Login failed:', data.message);
      }
    } catch (err) {
      setError('An error occurred during login. Please try again.');
      console.error('Login request error:', err);
    }
  }

  async function handleSignupSubmit(event) {
    event.preventDefault();
    setError('');

    // Basic validation
    if (!username || !password || !email) {
      setError('All fields are required');
      return;
    }

    try {
      const response = await fetch(`${API_BASE_URL}/api/signup`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          username,
          email,
          password,
          user_type: userType
        }),
      });

      const data = await response.json();

      if (response.ok) {
        // Signup successful!
        console.log('Signup successful:', data);
        // Switch to login form
        setIsLogin(true);
        setError('');
        // Optional: Add a success message
      } else {
        setError(data.message || 'Signup failed. Please try again.');
        console.error('Signup failed:', data.message);
      }
    } catch (err) {
      setError('An error occurred during signup. Please try again.');
      console.error('Signup request error:', err);
    }
  }

  function toggleForm() {
    setIsLogin(!isLogin);
    setError('');
  }

  return (
    <div className="auth-container">
      <h1>{isLogin ? 'Login' : 'Sign Up'}</h1>
      
      {isLogin ? (
        // Login Form
        <form className='login-form' onSubmit={handleLoginSubmit}>
          <div className='form-row'>
            <p>Username:</p>
            <input
              name='username'
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
            />
          </div>
          <div className='form-row'>
            <p>Password:</p>
            <input
              name='password'
              type='password'
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          {error && <p className="login-error">{error}</p>}
          <button type="submit">Login</button>
        </form>
      ) : (
        // Signup Form
        <form className='login-form' onSubmit={handleSignupSubmit}>
          <div className='form-row'>
            <p>Username:</p>
            <input
              name='username'
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
            />
          </div>
          <div className='form-row'>
            <p>Email:</p>
            <input
              name='email'
              type='email'
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>
          <div className='form-row'>
            <p>Password:</p>
            <input
              name='password'
              type='password'
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          <div className='form-row'>
            <p>Account Type:</p>
            <select 
              value={userType} 
              onChange={(e) => setUserType(e.target.value)}
            >
              <option value="patient">Patient</option>
              <option value="doctor">Doctor</option>
            </select>
          </div>
          {error && <p className="login-error">{error}</p>}
          <button type="submit">Sign Up</button>
        </form>
      )}
      
      <div className="toggle-form">
        <button onClick={toggleForm} className="toggle-btn">
          {isLogin ? 'Need an account? Sign Up' : 'Already have an account? Login'}
        </button>
      </div>
    </div>
  )
}

export default Login