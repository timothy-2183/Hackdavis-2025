import { useState, useEffect } from 'react'
import { Link } from "wouter";
import './Navbar.css'

function Navbar() {
  const [user, setUser] = useState(null);

  // Check if user is logged in on component mount
  useEffect(() => {
    const userData = localStorage.getItem('userData');
    if (userData) {
      setUser(JSON.parse(userData));
    }
  }, []);

  // Handle logout
  const handleLogout = () => {
    localStorage.removeItem('userData');
    setUser(null);
    window.location.href = '/';
  };

  return (
    <div className='navbar'>
        <div className='app-name'>Docsy</div>
        <div className='navbar-links'>
          <Link href="/">Home</Link>
          
          {!user ? (
            // Show login link if user is not logged in
            <Link href="/login">Login</Link>
          ) : (
            // Show appropriate dashboard based on user type
            <>
              {user.user_type === 'doctor' && (
                <Link href="/dashboard">Dashboard</Link>
              )}
              
              {user.user_type === 'patient' && (
                <Link href="/getsupport">Get Support</Link>
              )}
              
              <Link href="#" onClick={handleLogout}>Logout</Link>
            </>
          )}
        </div>
    </div>
  )
}

export default Navbar