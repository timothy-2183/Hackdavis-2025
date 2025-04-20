import { useEffect, useState } from 'react'
import './Dashboard.css'
import PatientCard from '../components/PatientCard'
import Message from '../components/Message'

function Dashboard() {
  const [patientInfo, setPatientInfo] = useState([{key: 1, name: "John Doe"}, {key: 2, name: "Jane Smith"}, {key: 3, name: "Bob Johnson"}]);
  const [messagesInfo, setMessagesInfo] = useState([]);
  const [activePatient, setActivePatient] = useState(patientInfo[0]);
  const [patientThreads, setPatientThreads] = useState({});
  const [activeThread, setActiveThread] = useState(null);
  const [patientMedical, setPatientMedical] = useState(null);
  const [aiAnalysis, setAiAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);
  const [analyzingConversation, setAnalyzingConversation] = useState(false);
  
  // Mock user for demo, in real app this would come from auth context
  const user = {
    id: 901,
    type: 'doctor'
  };

  // Fetch patient data when active patient changes
  useEffect(() => {
    if (activePatient) {
      fetchPatientMedicalData(activePatient.key);
      fetchPatientThreads(activePatient.key);
    }
  }, [activePatient]);
  
  // Fetch conversation when active thread changes
  useEffect(() => {
    if (activeThread) {
      fetchConversation(activeThread);
    } else {
      setMessagesInfo([]);
      setAiAnalysis(null);
    }
  }, [activeThread]);

  // Fetch patient medical information
  const fetchPatientMedicalData = async (patientId) => {
    try {
      const response = await fetch(`/api/patient/medical/${patientId}`);
      if (response.ok) {
        const data = await response.json();
        setPatientMedical(data);
      }
    } catch (error) {
      console.error('Error fetching patient data:', error);
    }
  };
  
  // Fetch all conversation threads for a patient
  const fetchPatientThreads = async (patientId) => {
    // For the sample data, we're going to use the preset thread IDs
    const threadIds = [];
    if (patientId === 1) threadIds.push(1, 3);
    if (patientId === 2) threadIds.push(2);
    if (patientId === 3) threadIds.push(3);
    
    setPatientThreads({
      [patientId]: threadIds
    });
    
    // Set the first thread as active if there are any
    if (threadIds.length > 0) {
      setActiveThread(threadIds[0]);
    } else {
      setActiveThread(null);
    }
  };
  
  // Fetch a specific conversation
  const fetchConversation = async (threadId) => {
    try {
      setLoading(true);
      const response = await fetch(`/api/conversation/${threadId}`);
      if (response.ok) {
        const data = await response.json();
        
        // Format conversation data for display
        const messages = data.conversation.map(comment => {
          const authId = JSON.parse(comment.auth_id);
          let author = 'AI';
          
          if (authId[0] === 0) { // Patient
            author = patientMedical?.pat_name || 'Patient';
          } else if (authId[0] === 1) { // Doctor
            author = 'You';
          }
          
          return {
            author: author,
            text: comment.content
          };
        });
        
        setMessagesInfo(messages);
        setAiAnalysis(null); // Clear previous analysis
      }
    } catch (error) {
      console.error('Error fetching conversation:', error);
    } finally {
      setLoading(false);
    }
  };

  // Analyze the current conversation using the Claude importance() function
  const analyzeConversation = async () => {
    if (!activeThread) return;
    
    try {
      setAnalyzingConversation(true);
      const response = await fetch(`/api/conversation/${activeThread}/analyze`, {
        method: 'POST'
      });
      
      if (response.ok) {
        const data = await response.json();
        // After analysis, refresh the conversation to get the AI comment
        fetchConversation(activeThread);
        setAiAnalysis(data.ai_analysis);
      }
    } catch (error) {
      console.error('Error analyzing conversation:', error);
    } finally {
      setAnalyzingConversation(false);
    }
  };

  async function handleFeedbackSubmit(e) {
    e.preventDefault();
    const formData = new FormData(e.target);
    const message = formData.get('feedback');
    
    if (!message.trim() || !activeThread) return;
    
    // Add message to conversation (optimistic update)
    const newMessage = {
      author: 'You',
      text: message
    };
    setMessagesInfo(prev => [...prev, newMessage]);
    
    try {
      setLoading(true);
      const response = await fetch('/insert_comment', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          id: activeThread,
          content: message,
          auth_id: JSON.stringify([1, user.id]) // 1 indicates doctor
        })
      });
      
      if (response.ok) {
        // Refresh conversation to get updated data
        fetchConversation(activeThread);
        
        // Clear the form
        e.target.reset();
      }
    } catch (error) {
      console.error('Error sending message:', error);
    } finally {
      setLoading(false);
    }
  }
  
  // Parse AI analysis to extract summary and tags
  const renderAiAnalysis = () => {
    if (!aiAnalysis) return null;
    
    // Split the analysis text into lines
    const lines = aiAnalysis.split('\n').filter(line => line.trim());
    
    // First paragraph is typically the summary
    const summary = lines[0];
    
    // Extract tags (we're assuming they come after the summary)
    const tags = lines.slice(1).filter(line => line.includes(':') || line.startsWith('#') || line.startsWith('-'));
    
    return (
      <div className="ai-analysis">
        <h4>AI Analysis</h4>
        <p className="summary">{summary}</p>
        {tags.length > 0 && (
          <div className="tags">
            <h5>Tags</h5>
            <ul>
              {tags.map((tag, index) => (
                <li key={index}>{tag}</li>
              ))}
            </ul>
          </div>
        )}
      </div>
    );
  };

  const patients = patientInfo.map((patient) => (
    <PatientCard 
      key={patient.key}
      active={patient.key === activePatient.key}
      name={patient.name} 
      onClick={() => {setActivePatient(patient)}}
    />
  ));

  const messages = messagesInfo.map((message, index) => (
    <Message key={index} author={message.author} text={message.text} />
  ));

  // Render patient threads
  const renderPatientThreads = () => {
    const threads = patientThreads[activePatient?.key] || [];
    
    if (threads.length === 0) {
      return <p>No conversations found</p>;
    }
    
    return (
      <div className="thread-list">
        <h4>Conversations</h4>
        <ul>
          {threads.map(threadId => (
            <li 
              key={threadId} 
              className={threadId === activeThread ? 'active' : ''}
              onClick={() => setActiveThread(threadId)}
            >
              Conversation #{threadId}
            </li>
          ))}
        </ul>
      </div>
    );
  };

  // Render patient medical information
  const renderPatientMedical = () => {
    if (!patientMedical) return null;
    
    return (
      <div className="patient-medical-info">
        <h4>Patient Medical Information</h4>
        <p><strong>Allergies:</strong> {patientMedical.allergies || 'None reported'}</p>
        <p><strong>Medications:</strong> {patientMedical.medications || 'None reported'}</p>
      </div>
    );
  };

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
            {renderPatientMedical()}
            {renderPatientThreads()}
          </div>
          <div className='conversation-panel'>
            <div className="conversation-header">
              <h3>Conversation History</h3>
            </div>
            {aiAnalysis && renderAiAnalysis()}
            <div className='conversation-container'>
            <button 
                className="analyze-button" 
                onClick={analyzeConversation}
                disabled={!activeThread || analyzingConversation}
              >
                {analyzingConversation ? 'Analyzing...' : 'Analyze Conversation'}
              </button>
              {loading ? (
                <p className="loading">Loading conversation...</p>
              ) : messages.length > 0 ? (
                messages
              ) : (
                <p className="no-messages">No messages in this conversation.</p>
              )}
            </div>
          </div>
          <div className='feedback-panel'>
            <div className='feedback-container'>
              <form className='feedback-form' onSubmit={handleFeedbackSubmit}>
                <p>Send feedback to patient:</p>
                <textarea 
                  className='feedback-input' 
                  name='feedback' 
                  maxLength={350}
                  disabled={!activeThread || loading}
                ></textarea>
                <button 
                  type='submit' 
                  disabled={!activeThread || loading}
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

export default Dashboard