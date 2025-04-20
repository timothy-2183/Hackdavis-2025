import { useState } from 'react'
import './Message.css'

function Message(messageData) {
  // Check if this is an analysis message
  const isAnalysis = messageData.author === 'AI' && messageData.text.startsWith('ANALYSIS:');
  
  // Parse AI analysis if applicable
  const renderAnalysis = () => {
    if (!isAnalysis) return null;
    
    // Remove the "ANALYSIS:" prefix
    const analysisText = messageData.text.substring(9).trim();
    
    // Split the analysis text into lines
    const lines = analysisText.split('\n').filter(line => line.trim());
    
    // First paragraph is typically the summary
    const summary = lines[0];
    
    // Extract tags (we're assuming they come after the summary)
    const tags = lines.slice(1).filter(line => line.includes(':') || line.startsWith('#') || line.startsWith('-'));
    
    return (
      <div className="analysis-content">
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
    
  return (
    <div className={`message ${isAnalysis ? 'analysis-message' : ''}`}>
      {isAnalysis ? (
        <>
          <p className="analysis-header"><b>AI Analysis:</b></p>
          {renderAnalysis()}
        </>
      ) : (
        <p><b>{messageData.author}:</b> {messageData.text}</p>
      )}
    </div>
  )
}

export default Message