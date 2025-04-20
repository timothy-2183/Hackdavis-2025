import { useState } from 'react'
import './Home.css'

function Home() {
  return (
    <div className="home-container">
      <div className="hero-section">
        <h1 className='big-title'>Docsy</h1>
        <h3>Convenient symptom reporting system for patients and doctors</h3>
        <p>Patients? Say goodbye to Googling symptoms. Doctors? Say hello to quick communication that fits in your schedule.</p>
        
        <div className="cta-buttons">
          <a href="/login" className="cta-button primary">Get Started</a>
          <a href="#features" className="cta-button secondary">Learn More</a>
        </div>
      </div>
    </div>
  )
}

export default Home