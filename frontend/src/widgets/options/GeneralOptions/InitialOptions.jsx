import React from 'react';
import { createChatBotMessage } from 'react-chatbot-kit';
import './InitialOptions.css';

const InitialOptions = (props) => {
  console.log('InitialOptions received props:', props);
  const { setState, actionProvider, initialChoices, state } = props;

  const handleChoice = (choice) => {
    console.log('Initial choice selected:', choice);
    console.log('Current state:', state);
    
    // Create client message for user's choice
    const message = actionProvider.createClientMessage(choice);
    actionProvider.addMessageToBotState(message);

    // Send the choice to the backend
    const choice_info = {
      user_id: state.userState,
      session_id: state.sessionID,
      user_choice: choice,
      input_type: initialChoices
    };
    
    console.log('Sending choice_info:', choice_info);
    actionProvider.sendRequest(choice_info);
  };

  if (!initialChoices || initialChoices.length === 0) {
    console.log('No initial choices available');
    return null;
  }

  return (
    <div className="initial-options-container">
      <div className="options-grid">
        {initialChoices.map((choice, index) => (
          <button
            key={index}
            className="option-button"
            onClick={() => handleChoice(choice)}
          >
            {choice}
          </button>
        ))}
      </div>
    </div>
  );
};

export default InitialOptions;