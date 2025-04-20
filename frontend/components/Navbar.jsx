import { useState } from 'react'
import { Link } from "wouter";
import './Navbar.css'

function Navbar() {

  return (
    <div className='navbar'>
        <div className='app-name'>Docsy</div>
        <div className='navbar-links'>
        <Link href="/">
            Home
        </Link>
        <Link href="/login">
            Login
        </Link>
        <Link href="/dashboard">
            Dashboard
        </Link>
        <Link href='/getsupport'>
          Get Support
        </Link>
        </div>
      
    </div>
  )
}

export default Navbar