import React, { useState, useEffect } from 'react';

const AskAIButton = ({ selectedText, onAsk, position, isVisible }) => {
  if (!isVisible || !selectedText) {
    return null;
  }

  return (
    <button
      className="ask-ai-button"
      style={{
        position: 'fixed',
        left: `${position.x}px`,
        top: `${position.y}px`,
        zIndex: 10000,
        background: '#1a73e8',
        color: 'white',
        border: 'none',
        borderRadius: '20px',
        padding: '8px 16px',
        fontSize: '14px',
        cursor: 'pointer',
        boxShadow: '0 2px 10px rgba(0,0,0,0.2)',
        fontWeight: '500',
        transform: 'translateY(-10px)',
        opacity: 0.95
      }}
      onClick={onAsk}
      onMouseDown={(e) => e.preventDefault()} // Prevent selection loss
    >
      Ask AI
    </button>
  );
};

export default AskAIButton;