import { useState } from 'react'
import { Route, Switch } from 'wouter'
import './App.css'
import Navbar from '../components/Navbar'
import Home from '../pages/Home'
import Login from '../pages/Login'
import Dashboard from '../pages/Dashboard'

function App() {

  return (
    <>
    <Navbar></Navbar>
    <Switch>
      <Route path='/'>
        <Home/>
      </Route>
      <Route path='/login'>
        <Login></Login>
      </Route>
      <Route path='/dashboard'>
        <Dashboard></Dashboard>
      </Route>
    </Switch>
    </>
  )
}

export default App
