import { useState } from 'react'
import './Features.css'

function Features() {
  return (
    <div className="home-container">
      <div className="hero-section">
        <h1>Features</h1>
        <ul style={{textAlign:"left"}}>
            <li>
                Doctor dashboard organizes conversations with patients
            </li>
            <li>
                Patients can send messages to their doctor to update them on their condition
            </li>
            <li>
                AI provides tags and initial screening summary for doctors
            </li>
        </ul>
      </div>
    </div>
  )
}

export default Features