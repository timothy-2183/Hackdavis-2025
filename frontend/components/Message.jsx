import { useState } from 'react'
import './Message.css'

function Message(messageData) {
    
  return (
    <div className='message'>
      <p><b>{messageData.author}:</b> {messageData.text}</p>
    </div>
  )
}

export default Message