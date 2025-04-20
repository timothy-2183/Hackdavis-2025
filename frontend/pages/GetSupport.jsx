import { useState } from 'react'
import './GetSupport.css'
import Message from '../components/Message'

function GetSupport() {
    const [messageData, setMessageData] = useState([]);

    function handleMessageSubmit(formData) { // TODO this should add a new message the most recent conversation

    }

    function handleSymptomSubmit(formData) { // TODO this should add symptoms, allergies, and medication
      // TODO basically starts a new conversation

    }

  return (
    <>
      <div className='dashboard-container'>
        <h1 className='dashboard-text'>Get Support</h1>
        <div className='dashboard-main'>
            <div className='symptoms-panel'>
              <h3>Start a new conversation</h3>
                <form className='symptoms-form' action={handleSymptomSubmit}>
                    <div className='form-row'>
                        <p>Describe your allergies: </p>
                        <input></input>
                    </div>
                    <div className='form-row'>
                        <p>Describe your recent medications: </p>
                        <input></input>
                    </div>
                    <div className='form-row'>
                        <p>Describe your current symptoms: </p>
                        <input></input>
                    </div>
                    <button type='submit'>Submit</button>
                </form>
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
                <form className='feedback-form' action={handleMessageSubmit}>
                  <p>Send a message to your doctor:</p>
                  <textarea className='feedback-input' name='message' maxLength={350}></textarea>
                  <button type='submit'>Submit</button>
                </form>
              </div>
            </div>
        </div>
      </div>
      
    </>
  )
}

export default GetSupport