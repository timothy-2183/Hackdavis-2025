import { useState } from 'react'
import './Dashboard.css'
import PatientCard from '../components/PatientCard'

function Dashboard() {

  return (
    <>
      <div className='dashboard-container'>
        <h1 className='dashboard-text'>Dashboard</h1>
        <div className='dashboard-main'>
            <div className='patients-panel'>
                <h3>Your Patients</h3>
                <div className='patients-container'>
                    <PatientCard></PatientCard>
                </div>
            </div>
        </div>
      </div>
      
    </>
  )
}

export default Dashboard