import React, { useState, useEffect, useRef, useCallback } from 'react';
import './ChatWidget.css';

const ChatWidget = ({ initialIsOpen = false }) => {
  const [isOpen, setIsOpen] = useState(initialIsOpen);
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isTyping, setIsTyping] = useState(false);
  const [colorMode, setColorMode] = useState('light'); // Default to light mode
  const [selectedText, setSelectedText] = useState('');
  const [showAskAi, setShowAskAi] = useState(false);
  const [askAiPosition, setAskAiPosition] = useState({ x: 0, y: 0 });
  const [askAiInputValue, setAskAiInputValue] = useState('');
  const [showAskAiInput, setShowAskAiInput] = useState(false);
  const [askAiInputPosition, setAskAiInputPosition] = useState({ x: 0, y: 0 });
  const [agentMode, setAgentMode] = useState('normal'); // 'normal' or 'selected'
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);
  const askAiInputRef = useRef(null);

  // Initialize color mode based on system preference or localStorage
  useEffect(() => {
    const savedColorMode = localStorage.getItem('theme');
    const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;

    if (savedColorMode) {
      setColorMode(savedColorMode);
    } else if (systemPrefersDark) {
      setColorMode('dark');
    } else {
      setColorMode('light');
    }
  }, []);

  // Handle text selection
  useEffect(() => {
    const handleSelection = () => {
      const selection = window.getSelection();
      const text = selection.toString().trim();

      if (text.length > 0 && text.length < 500) { // Only show for reasonable text lengths
        const range = selection.getRangeAt(0);
        const rect = range.getBoundingClientRect();

        setSelectedText(text);
        setAgentMode('selected');
        setAskAiPosition({
          x: rect.left + window.scrollX,
          y: rect.top + window.scrollY - 40 // Position above the selection
        });
        setShowAskAi(true);

        // Hide the input if it was visible
        setShowAskAiInput(false);
      } else {
        setShowAskAi(false);
        setSelectedText('');
        setAgentMode('normal');
        setShowAskAiInput(false);
      }
    };

    const handleMouseUp = () => {
      setTimeout(handleSelection, 0); // Delay to ensure selection is complete
    };

    document.addEventListener('mouseup', handleMouseUp);
    document.addEventListener('keyup', handleSelection);

    return () => {
      document.removeEventListener('mouseup', handleMouseUp);
      document.removeEventListener('keyup', handleSelection);
    };
  }, []);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const sendMessage = async (message = null) => {
    const textToSend = String(message || inputValue || "").trim();
    if (!textToSend || isLoading) return;

    const userMessage = {
      id: Date.now(),
      text: textToSend,
      sender: 'user',
      timestamp: new Date().toISOString()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);
    setIsTyping(true);

    try {
      // Determine which endpoint to use based on agent mode
      let endpoint = '/api/v1/chat/message';
      let requestBody;

      if (agentMode === 'selected' && selectedText) {
        // Use the query_with_selection endpoint when there's selected text
        endpoint = '/api/v1/chat/query_with_selection';
        requestBody = {
          question: textToSend,
          selected_text: selectedText,
          history: messages.map(msg => ({
            role: msg.sender === 'user' ? 'user' : 'assistant',
            content: msg.text
          }))
        };
      } else {
        // Use the regular message endpoint
        requestBody = {
          message: textToSend,
          selected_text: selectedText || null, // Send selected_text if available
          history: messages.map(msg => ({
            role: msg.sender === 'user' ? 'user' : 'assistant',
            content: msg.text
          }))
        };
      }

      const response = await fetch(endpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestBody)
      });

      if (response.ok) {
        const data = await response.json();
        const botMessage = {
          id: Date.now() + 1,
          text: data.response,
          sender: 'bot',
          sources: data.sources || [],
          timestamp: new Date().toISOString()
        };
        setMessages(prev => [...prev, botMessage]);
      } else {
        const errorMessage = {
          id: Date.now() + 1,
          text: 'Sorry, I encountered an error processing your request. Please try again.',
          sender: 'bot',
          timestamp: new Date().toISOString()
        };
        setMessages(prev => [...prev, errorMessage]);
      }
    } catch (error) {
      const errorMessage = {
        id: Date.now() + 1,
        text: 'Sorry, I encountered an error connecting to the server. Please try again.',
        sender: 'bot',
        timestamp: new Date().toISOString()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
      setIsTyping(false);
      setShowAskAi(false); // Hide the Ask AI button after sending
      setShowAskAiInput(false); // Hide the Ask AI input after sending
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const toggleChat = () => {
    setIsOpen(!isOpen);
    if (!isOpen && inputRef.current) {
      setTimeout(() => inputRef.current?.focus(), 100);
    }
  };

  // Toggle color mode
  const toggleColorMode = () => {
    const newMode = colorMode === 'light' ? 'dark' : 'light';
    setColorMode(newMode);
    localStorage.setItem('theme', newMode);
  };

  // Handle Ask AI button click - show input field
  const handleAskAIButtonClick = () => {
    if (selectedText) {
      // Position the input field near the button
      setAskAiInputPosition({
        x: askAiPosition.x,
        y: askAiPosition.y + 40 // Position below the button
      });
      setShowAskAiInput(true);
      setShowAskAi(false); // Hide the button

      // Focus the input field after a short delay to ensure it's rendered
      setTimeout(() => {
        if (askAiInputRef.current) {
          askAiInputRef.current.focus();
        }
      }, 100);
    }
  };

  // Handle sending the question with selected text context
  const handleAskAIQuestion = () => {
    if (askAiInputValue.trim() && selectedText) {
      // We'll send the selected text separately via the API, not as part of the message
      sendMessage(askAiInputValue);
      setAskAiInputValue('');
      setShowAskAiInput(false);
    }
  };

  // Handle key down for Ask AI input
  const handleAskAIKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleAskAIQuestion();
    }
  };

  // Clear selected text and reset to normal mode
  const clearSelectedText = () => {
    setSelectedText('');
    setAgentMode('normal');
    setShowAskAi(false);
    setShowAskAiInput(false);
  };

  if (!isOpen) {
    return (
      <>
        {/* Ask AI button for selected text */}
        {showAskAi && (
          <button
            className="ask-ai-button"
            style={{
              position: 'fixed',
              left: `${askAiPosition.x}px`,
              top: `${askAiPosition.y}px`,
              zIndex: 10000,
              background: '#1a73e8',
              color: 'white',
              border: 'none',
              borderRadius: '20px',
              padding: '8px 16px',
              fontSize: '14px',
              cursor: 'pointer',
              boxShadow: '0 4px 12px rgba(0,0,0,0.15)',
              fontWeight: '500',
              transition: 'all 0.2s ease',
            }}
            onClick={handleAskAIButtonClick}
            onMouseDown={(e) => e.preventDefault()} // Prevent blurring the selection
          >
            💬 Ask AI
          </button>
        )}

        {/* Ask AI input field */}
        {showAskAiInput && (
          <div
            className="ask-ai-input-container"
            style={{
              position: 'fixed',
              left: `${askAiInputPosition.x}px`,
              top: `${askAiInputPosition.y}px`,
              zIndex: 10000,
              background: 'white',
              borderRadius: '12px',
              padding: '12px',
              boxShadow: '0 4px 20px rgba(0,0,0,0.15)',
              border: '1px solid #e0e0e0',
              minWidth: '300px',
              maxWidth: '400px',
            }}
          >
            <textarea
              ref={askAiInputRef}
              value={askAiInputValue}
              onChange={(e) => setAskAiInputValue(e.target.value)}
              onKeyDown={handleAskAIKeyDown}
              placeholder={`Ask about: "${selectedText.substring(0, 50)}${selectedText.length > 50 ? '...' : ''}"`}
              style={{
                width: '100%',
                minHeight: '60px',
                maxHeight: '120px',
                padding: '8px 12px',
                borderRadius: '8px',
                border: '1px solid #ddd',
                fontSize: '14px',
                resize: 'vertical',
                marginBottom: '8px',
                fontFamily: 'inherit',
              }}
              rows={2}
            />
            <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '8px' }}>
              <button
                onClick={() => setShowAskAiInput(false)}
                style={{
                  padding: '6px 12px',
                  border: '1px solid #ddd',
                  borderRadius: '6px',
                  backgroundColor: '#f5f5f5',
                  cursor: 'pointer',
                  fontSize: '13px',
                }}
              >
                Cancel
              </button>
              <button
                onClick={handleAskAIQuestion}
                disabled={!askAiInputValue.trim()}
                style={{
                  padding: '6px 12px',
                  backgroundColor: '#1a73e8',
                  color: 'white',
                  border: 'none',
                  borderRadius: '6px',
                  cursor: askAiInputValue.trim() ? 'pointer' : 'not-allowed',
                  fontSize: '13px',
                  opacity: askAiInputValue.trim() ? 1 : 0.6,
                }}
              >
                Send
              </button>
            </div>
          </div>
        )}

        <button
          className={`chat-widget-toggle chat-widget-toggle--${colorMode}`}
          onClick={toggleChat}
          aria-label="Open chat"
        >
          <ChatIcon />
        </button>
      </>
    );
  }

  return (
    <>
      {/* Ask AI button for selected text */}
      {showAskAi && (
        <button
          className="ask-ai-button"
          style={{
            position: 'fixed',
            left: `${askAiPosition.x}px`,
            top: `${askAiPosition.y}px`,
            zIndex: 10000,
            background: '#1a73e8',
            color: 'white',
            border: 'none',
            borderRadius: '20px',
            padding: '8px 16px',
            fontSize: '14px',
            cursor: 'pointer',
            boxShadow: '0 4px 12px rgba(0,0,0,0.15)',
            fontWeight: '500',
            transition: 'all 0.2s ease',
          }}
          onClick={handleAskAIButtonClick}
          onMouseDown={(e) => e.preventDefault()} // Prevent blurring the selection
        >
          💬 Ask AI
        </button>
      )}

      {/* Ask AI input field */}
      {showAskAiInput && (
        <div
          className="ask-ai-input-container"
          style={{
            position: 'fixed',
            left: `${askAiInputPosition.x}px`,
            top: `${askAiInputPosition.y}px`,
            zIndex: 10000,
            background: 'white',
            borderRadius: '12px',
            padding: '12px',
            boxShadow: '0 4px 20px rgba(0,0,0,0.15)',
            border: '1px solid #e0e0e0',
            minWidth: '300px',
            maxWidth: '400px',
          }}
        >
          <textarea
            ref={askAiInputRef}
            value={askAiInputValue}
            onChange={(e) => setAskAiInputValue(e.target.value)}
            onKeyDown={handleAskAIKeyDown}
            placeholder={`Ask about: "${selectedText.substring(0, 50)}${selectedText.length > 50 ? '...' : ''}"`}
            style={{
              width: '100%',
              minHeight: '60px',
              maxHeight: '120px',
              padding: '8px 12px',
              borderRadius: '8px',
              border: '1px solid #ddd',
              fontSize: '14px',
              resize: 'vertical',
              marginBottom: '8px',
              fontFamily: 'inherit',
            }}
            rows={2}
          />
          <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '8px' }}>
            <button
              onClick={() => setShowAskAiInput(false)}
              style={{
                padding: '6px 12px',
                border: '1px solid #ddd',
                borderRadius: '6px',
                backgroundColor: '#f5f5f5',
                cursor: 'pointer',
                fontSize: '13px',
              }}
            >
              Cancel
            </button>
            <button
              onClick={handleAskAIQuestion}
              disabled={!askAiInputValue.trim()}
              style={{
                padding: '6px 12px',
                backgroundColor: '#1a73e8',
                color: 'white',
                border: 'none',
                borderRadius: '6px',
                cursor: askAiInputValue.trim() ? 'pointer' : 'not-allowed',
                fontSize: '13px',
                opacity: askAiInputValue.trim() ? 1 : 0.6,
              }}
            >
              Send
            </button>
          </div>
        </div>
      )}

      <div className={`chat-widget chat-widget--${colorMode}`}>
        <div className="chat-widget-header">
          <h3>Physical AI Textbook Assistant</h3>
          <div style={{display: 'flex', gap: '8px'}}>
            {agentMode === 'selected' && selectedText && (
              <div className="chat-widget-mode-indicator" style={{ display: 'flex', alignItems: 'center', fontSize: '12px', background: '#e3f2fd', padding: '4px 8px', borderRadius: '12px' }}>
                <span style={{ color: '#1976d2', fontWeight: '500' }}>Selected text mode</span>
                <button
                  onClick={clearSelectedText}
                  style={{
                    marginLeft: '8px',
                    background: 'none',
                    border: 'none',
                    color: '#1976d2',
                    cursor: 'pointer',
                    fontSize: '14px'
                  }}
                  title="Clear selection"
                >
                  ×
                </button>
              </div>
            )}
            <button
              className="chat-widget-color-mode"
              onClick={toggleColorMode}
              aria-label="Toggle color mode"
              style={{
                background: 'none',
                border: 'none',
                color: 'white',
                cursor: 'pointer',
                fontSize: '16px',
                padding: '4px'
              }}
            >
              {colorMode === 'light' ? '🌙' : '☀️'}
            </button>
            <button
              className="chat-widget-close"
              onClick={toggleChat}
              aria-label="Close chat"
            >
              ×
            </button>
          </div>
        </div>

        <div className="chat-widget-messages">
          {messages.length === 0 ? (
            <div className="chat-widget-welcome">
              <p>Hello! I'm your Physical AI & Humanoid Robotics textbook assistant.</p>
              <p>Ask me anything about the content in your textbook, and I'll help you find relevant information.</p>
              {agentMode === 'selected' && selectedText && (
                <div className="chat-widget-selected-text-preview" style={{
                  marginTop: '10px',
                  padding: '8px',
                  backgroundColor: '#f5f5f5',
                  borderRadius: '4px',
                  fontSize: '12px',
                  borderLeft: '3px solid #1a73e8'
                }}>
                  <strong>Context:</strong> "{selectedText.substring(0, 100)}{selectedText.length > 100 ? '...' : ''}"
                </div>
              )}
            </div>
          ) : (
            messages.map((message) => (
              <div
                key={message.id}
                className={`chat-widget-message chat-widget-message--${message.sender}`}
              >
                <div className="chat-widget-message-text">
                  {message.text}
                </div>
                {message.sources && message.sources.length > 0 && message.sender === 'bot' && (
                  <div className="chat-widget-sources">
                    <details>
                      <summary>Sources:</summary>
                      <ul>
                        {message.sources.map((source, index) => (
                          <li key={index}>
                            {source.source_file || 'Unknown source'}
                          </li>
                        ))}
                      </ul>
                    </details>
                  </div>
                )}
              </div>
            ))
          )}
          {isTyping && (
            <div className="chat-widget-message chat-widget-message--bot">
              <div className="chat-widget-message-text">
                <TypingIndicator />
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        <div className="chat-widget-input-area">
          <textarea
            ref={inputRef}
            className="chat-widget-input"
            value={inputValue}
            onChange={(e) => setInputValue(String(e.target.value || ""))}
            onKeyDown={handleKeyDown}
            placeholder={agentMode === 'selected' ? "Ask about the selected text..." : "Ask a question about the textbook..."}
            disabled={isLoading}
            rows={2}
          />
          <button
            className="chat-widget-send-button"
            onClick={sendMessage}
            disabled={isLoading || !String(inputValue || "").trim()}
            aria-label="Send message"
          >
            <SendIcon />
          </button>
        </div>
      </div>
    </>
  );
};

// Simple SVG icons
const ChatIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M21 15C21 15.5304 20.7893 16.0391 20.4142 16.4142C20.0391 16.7893 19.5304 17 19 17H16.71C16.56 17.67 16.31 18.31 15.96 18.9C15.26 18.44 14.67 17.85 14.21 17.15C13.8 17.5 13.34 17.79 12.85 18.01C12.36 18.23 11.85 18.37 11.33 18.44C10.81 18.51 10.29 18.5 9.77 18.42C9.25 18.34 8.75 18.18 8.27 17.95C7.79 17.72 7.34 17.42 6.94 17.06C6.54 16.7 6.19 16.28 5.9 15.82C5.61 15.36 5.39 14.86 5.24 14.34C5.09 13.82 5.01 13.28 5.01 12.74C5.01 12.2 5.09 11.66 5.24 11.14C5.39 10.62 5.61 10.12 5.9 9.66C6.19 9.2 6.54 8.78 6.94 8.42C7.34 8.06 7.79 7.76 8.27 7.53C8.75 7.3 9.25 7.14 9.77 7.06C10.29 6.98 10.81 6.97 11.33 7.04C11.85 7.11 12.36 7.25 12.85 7.47C13.34 7.69 13.8 8.08 14.21 8.43C14.67 7.73 15.26 7.14 15.96 6.68C16.31 7.27 16.56 7.91 16.71 8.58H19C19.5304 8.58 20.0391 8.81071 20.4142 9.18579C20.7893 9.56086 21 10.0696 21 10.6V15Z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
  </svg>
);

const SendIcon = () => (
  <svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M18.3332 9.16667V16.6667C18.3332 16.8877 18.2457 17.0995 18.0892 17.2559C17.9328 17.4124 17.721 17.5 17.5001 17.5H2.50007C2.27909 17.5 2.06732 17.4124 1.91087 17.2559C1.75442 17.0995 1.66675 16.8877 1.66675 16.6667V3.33333C1.66675 3.11236 1.75442 2.90058 1.91087 2.74413C2.06732 2.58768 2.27909 2.5 2.50007 2.5H11.6667" stroke="currentColor" strokeWidth="1.66667" strokeLinecap="round" strokeLinejoin="round"/>
    <path d="M18.3334 2.5L10.8334 10.8333" stroke="currentColor" strokeWidth="1.66667" strokeLinecap="round" strokeLinejoin="round"/>
  </svg>
);

const TypingIndicator = () => (
  <div className="typing-indicator">
    <span></span>
    <span></span>
    <span></span>
  </div>
);

export default ChatWidget;