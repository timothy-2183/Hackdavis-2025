import { useState, useEffect } from 'react'
import './GetSupport.css'
import Message from '../components/Message'

function GetSupport() {
    const [messageData, setMessageData] = useState([]);
    const [threadId, setThreadId] = useState(0);
    const [loading, setLoading] = useState(false);
    
    // Mock user for demo, in real app this would come from auth context
    const user = {
        id: 1,
        type: 'patient'
    };

    useEffect(() => {
        // If we have a thread ID, load the conversation
        if (threadId > 0) {
            fetchConversation(threadId);
        } else {
            // If no active thread, check if there are existing threads for this user
            checkExistingThreads();
        }
    }, [threadId]);

    const checkExistingThreads = async () => {
        // For demo purposes, just set thread ID 1 for user 1
        if (user.id === 1) {
            setThreadId(1);
        }
    };

    const fetchConversation = async (id) => {
        try {
            const response = await fetch(`/api/conversation/${id}`);
            if (response.ok) {
                const data = await response.json();
                
                // Format conversation data for display
                const messages = data.conversation.map(comment => {
                    const authId = JSON.parse(comment.auth_id);
                    let author = 'AI';
                    
                    if (authId[0] === 0) {
                        author = 'You'; // Patient
                    } else if (authId[0] === 1) {
                        author = 'Doctor'; // Doctor
                    }
                    
                    return {
                        author: author,
                        text: comment.content
                    };
                });
                
                setMessageData(messages);
            }
        } catch (error) {
            console.error('Error fetching conversation:', error);
        }
    };

    async function handleMessageSubmit(e) {
        e.preventDefault();
        const formData = new FormData(e.target);
        const message = formData.get('message');
        
        if (!message.trim()) return;
        
        // Add message to conversation (optimistic update)
        setMessageData(prev => [...prev, { author: 'You', text: message }]);
        
        try {
            setLoading(true);
            const response = await fetch('/insert_comment', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    id: threadId || 0, // Use 0 to create a new thread if none exists
                    content: message,
                    auth_id: JSON.stringify([0, user.id]) // 0 indicates patient
                })
            });
            
            if (response.ok) {
                // If this is a new thread, the response doesn't include a thread_id
                // We'll just fetch the conversation to ensure we have all messages
                if (threadId > 0) {
                    fetchConversation(threadId);
                } else {
                    // If this was a new thread, we need to get the thread ID from somewhere
                    // For demo, let's assume response has thread_id
                    const data = await response.json();
                    if (data && data.thread_id) {
                        setThreadId(data.thread_id);
                    }
                }
                
                // Clear the form
                e.target.reset();
            }
        } catch (error) {
            console.error('Error sending message:', error);
        } finally {
            setLoading(false);
        }
    }

    async function handleSymptomSubmit(e) {
        e.preventDefault();
        const formData = new FormData(e.target);
        
        // Create payload from form data
        const payload = {
            patient_id: user.id,
            allergies: formData.get('allergies'),
            medications: formData.get('medications'),
            symptoms: formData.get('symptoms')
        };
        
        if (!payload.symptoms.trim()) {
            alert('Please describe your symptoms');
            return;
        }
        
        try {
            setLoading(true);
            const response = await fetch('/api/patient/symptoms', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(payload)
            });
            
            if (response.ok) {
                const data = await response.json();
                
                // Set the thread ID for this conversation
                setThreadId(data.thread_id);
                
                // Update the message data with the new conversation
                setMessageData([
                    { author: 'You', text: payload.symptoms },
                    { author: 'AI', text: data.ai_response }
                ]);
                
                // Clear the form
                e.target.reset();
            }
        } catch (error) {
            console.error('Error submitting symptoms:', error);
        } finally {
            setLoading(false);
        }
    }

  return (
    <>
      <div className='dashboard-container'>
        <h1 className='dashboard-text'>Get Support</h1>
        <div className='dashboard-main'>
            <div className='symptoms-panel'>
                <form className='symptoms-form' onSubmit={handleSymptomSubmit}>
                    <div className='form-row'>
                        <p>Describe your allergies: </p>
                        <input name='allergies'></input>
                    </div>
                    <div className='form-row'>
                        <p>Describe your previous medications: </p>
                        <input name='medications'></input>
                    </div>
                    <div className='form-row'>
                        <p>Describe your current symptoms: </p>
                        <input name='symptoms' required></input>
                    </div>
                    <button type='submit' disabled={loading}>
                        {loading ? 'Submitting...' : 'Submit Symptoms'}
                    </button>
                </form>
            </div>
            <div className='conversation-panel'>
              <h3>Conversation History</h3>
              <div className='conversation-container'>
                {messageData.length > 0 ? (
                    messageData.map((message, index) => (
                        <Message key={index} author={message.author} text={message.text} />
                    ))
                ) : (
                    <p className="no-messages">No messages yet. Describe your symptoms or send a message to start a conversation.</p>
                )}
              </div>
            </div>
            <div className='feedback-panel'>
              <div className='feedback-container'>
                <form className='feedback-form' onSubmit={handleMessageSubmit}>
                  <p>Send a message to your doctor:</p>
                  <textarea 
                    className='feedback-input' 
                    name='message' 
                    maxLength={350}
                    disabled={loading}
                  ></textarea>
                  <button 
                    type='submit' 
                    disabled={loading}
                  >
                    {loading ? 'Sending...' : 'Submit'}
                  </button>
                </form>
              </div>
            </div>
        </div>
      </div>
      
    </>
  )
}

export default GetSupport