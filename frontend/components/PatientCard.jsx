import { useState } from 'react'
import './PatientCard.css'
import Tag from './Tag'

function PatientCard(patientData) {
  return (
    <div className={patientData.active ? 'patient-card patient-active': 'patient-card'} onClick={patientData.onClick}>
      <div className='patient-info'>
        <i><p>Name: {patientData.name}</p></i>
      </div>
        
        <div className='symptoms-container'>
          <b><p>Symptoms:</p></b>
          <ul>
              <li>Symptom 1</li>
              <li>Symptom 2</li>
          </ul>
        </div>
        
        <div className='tags'>
            <Tag text='Urgent' color='red'></Tag>
            <Tag text='Showing Improvement' color='green'></Tag>
            <Tag text='Needs Followup' color='Yellow'></Tag>
        </div>
    </div>
  )
}

export default PatientCard