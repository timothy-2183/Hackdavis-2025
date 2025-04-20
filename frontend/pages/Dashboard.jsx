import { useState } from 'react'
import './Dashboard.css'
import PatientCard from '../components/PatientCard'
import Message from '../components/Message'

function Dashboard() {
  const [activePatient, setActivePatient] = useState(null);

  function handleFeedbackSubmit(formData) {
    
  }

  return (
    <>
      <div className='dashboard-container'>
        <h1 className='dashboard-text'>Dashboard</h1>
        <div className='dashboard-main'>
            <div className='patients-panel'>
                <h3>Your Patients</h3>
                <div className='patients-container'>
                    <PatientCard name='John Doe'></PatientCard>
                </div>
            </div>
            <div className='conversation-panel'>
              <h3>Conversation History</h3>
              <div className='conversation-container'>
                <Message author='John Doe' text='Ouch!'></Message>
                <Message author='Dr. Smarty' text='You should come in for an appointment.'></Message>
              </div>
            </div>
            <div className='feedback-panel'>
              <div className='feedback-container'>
                <form className='feedback-form' action={handleFeedbackSubmit}>
                  <p>Send feedback to patient:</p>
                  <textarea className='feedback-input' name='feedback' maxLength={350}></textarea>
                  <button type='submit'>Submit</button>
                </form>
              </div>
            </div>
        </div>
      </div>
      
    </>
  )
}

export default Dashboard