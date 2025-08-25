import React from 'react';
import { createChatBotMessage } from 'react-chatbot-kit';
import './InitialOptions.css';

const InitialOptions = (props) => {
  const { setState, actionProvider, initialChoices } = props;

  const handleChoice = (choice) => {
    // Create client message for user's choice
    const message = actionProvider.createClientMessage(choice);
    actionProvider.addMessageToBotState(message);

    // Send the choice to the backend
    actionProvider.sendRequest({
      user_id: props.state.userState,
      session_id: props.state.sessionID,
      user_choice: choice,
      input_type: "initial_choice"
    });
  };

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