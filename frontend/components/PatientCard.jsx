import { useState } from 'react'
import './PatientCard.css'
import Tag from './Tag'

function PatientCard(patientData) {

  return (
    <div className='patient-card'>
        <i><p>Name: </p></i>
        <b><p>Symptoms</p></b>
        <ul>
            <li>Symptom 1</li>
            <li>Symptom 2</li>
        </ul>
        <div className='tags'>
            <Tag></Tag>
        </div>
    </div>
  )
}

export default PatientCard