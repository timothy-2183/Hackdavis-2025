import { useEffect, useState } from 'react'
import './Dashboard.css'
import PatientCard from '../components/PatientCard'
import Message from '../components/Message'

function Dashboard() {
  const [patientInfo, setPatientInfo] = useState([{key: 1,name: "John Doe"}, {key:2,name: "Best Patient"}, {key:3,name: "Third Person"}]);
  const [messagesInfo, setMessagesInfo] = useState([{author: 'John Doe', text:'My leg!'}, {author: 'Dr. Smarty', text:'Come in for an appointment.'}]);
  const [activePatient, setActivePatient] = useState(patientInfo[0]);

  function handleFeedbackSubmit(formData) {

    // update message log locally
    const prevState = messagesInfo;
    setMessagesInfo(prevState.concat({author: 'Me', text: formData.get('feedback')})) // TODO replace 'me' with logged in user's name?
  }
  
  // handle changing active patient
  useEffect(()=>{
    
  }, [activePatient])

  const patients = patientInfo.map((patient) => (<PatientCard 
    active={patient.key == activePatient.key ? true : false}
    name={patient.name} 
    onClick={() => {setActivePatient(patient)}}
    ></PatientCard>))

  const messages = messagesInfo.map((message) => (
    <Message author={message.author} text={message.text}></Message>
  ))


  return (
    <>
      <div className='dashboard-container'>
        <h1 className='dashboard-text'>Dashboard</h1>
        <div className='dashboard-main'>
            <div className='patients-panel'>
                <h3>Your Patients</h3>
                <div className='patients-container'>
                  {patients}
                </div>
            </div>
            <div className='conversation-panel'>
              <h3>Conversation History</h3>
              <div className='conversation-container'>
                {messages}
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