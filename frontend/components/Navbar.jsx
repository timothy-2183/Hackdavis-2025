import { useState } from 'react'
import { Link } from "wouter";
import './Navbar.css'

function Navbar() {

  return (
    <div className='navbar'>
        <div className='app-name'>AppNameHere</div>
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
        </div>
      
    </div>
  )
}

export default Navbar