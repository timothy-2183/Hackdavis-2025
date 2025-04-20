import { useState } from 'react'
import { Route, Switch } from 'wouter'
import './App.css'
import Navbar from '../components/Navbar'
import Home from '../pages/Home'
import Login from '../pages/Login'
import Dashboard from '../pages/Dashboard'
import GetSupport from '../pages/GetSupport'

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
      <Route path='/getsupport'>
        <GetSupport></GetSupport>
      </Route>
    </Switch>
    </>
  )
}

export default App
