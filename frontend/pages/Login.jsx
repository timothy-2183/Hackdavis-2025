import { useState } from 'react'
import './Login.css'

function Login() {
  function handleLogin(formData) {
    const username = formData.get('username')
    const password = formData.get('password')
    
    
  }

  return (
    <>
      <h1>Login</h1>
      <form className='login-form' action={handleLogin}>
        <div className='form-row'>
          <p>Username:</p>
          <input name='username'></input>
        </div>
        <div className='form-row'>
          <p>Password:</p>
          <input name='password' type='password'></input>
        </div>
        <button type="submit">Login</button>
      </form>
    </>
  )
}

export default Login