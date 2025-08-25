import React, { useState, useEffect } from "react";
import { Chatbot } from "react-chatbot-kit";
import { createChatBotMessage } from "react-chatbot-kit";
import "./App.css";
import MessageParser from "./MessageParser";
import ActionProvider from "./ActionProvider";
import config from "./config";
import Login from "./Login";

const App = () => {
  const [showTools, setShowTools] = useState(false);
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [userInfo, setUserInfo] = useState(null);
  const [chatConfig, setChatConfig] = useState(config);

  const handleLogin = (userData) => {
    setUserInfo(userData);
    setIsLoggedIn(true);
    
    // Create initial messages using the backend response
    const initialMessages = [
      createChatBotMessage(`Hi ${userData.username}, welcome to today's therapy session!`, {
        withAvatar: true,
        delay: 0,
      }),
    ];
    
    // Add the model prompt from backend if available
    if (userData.model_prompt) {
      initialMessages.push(
        createChatBotMessage(userData.model_prompt, {
          withAvatar: true,
          delay: 1500,
          widget: userData.choices && userData.choices.length > 0 ? "InitialOptions" : null,
        })
      );
    } else {
      initialMessages.push(
        createChatBotMessage("I'm here to help you with your emotional well-being. Let's begin our session.", {
          withAvatar: true,
          delay: 1500,
        })
      );
    }
    
    // Update config with user info and initial messages
    const updatedConfig = {
      ...config,
      initialMessages: initialMessages,
      state: {
        ...config.state,
        userState: userData.userID,
        sessionID: userData.sessionID,
        username: userData.username,
        // Store the initial choices from backend
        initialChoices: userData.choices || []
      }
    };
    
    setChatConfig(updatedConfig);
  };

  const handleRegister = (userData) => {
    setUserInfo(userData);
    setIsLoggedIn(true);
    
    // Create welcome messages for new user
    const welcomeMessages = [
      createChatBotMessage(`Welcome to MindGuide, ${userData.username}!`, {
        withAvatar: true,
        delay: 0,
      }),
      createChatBotMessage("I'm glad you're here. Let's start your first therapy session together.", {
        withAvatar: true,
        delay: 1500,
      }),
    ];
    
    // Update config with user info and welcome messages
    const updatedConfig = {
      ...config,
      initialMessages: welcomeMessages,
      state: {
        ...config.state,
        userState: userData.userID,
        sessionID: userData.sessionID,
        username: userData.username,
      }
    };
    
    setChatConfig(updatedConfig);
  };

  const handleLogout = () => {
    setIsLoggedIn(false);
    setUserInfo(null);
    setChatConfig(config); // Reset to original config
  };

  if (!isLoggedIn) {
    return <Login onLogin={handleLogin} onRegister={handleRegister} />;
  }

  return (
    <div className="App">
      <div className="app-header">
        <h1>MindGuide Therapy Assistant</h1>
        <div className="header-controls">
          <span className="user-info">欢迎, {userInfo?.username}</span>
          <button 
            className="tools-toggle"
            onClick={() => setShowTools(!showTools)}
          >
            {showTools ? '隐藏工具' : '显示工具'}
          </button>
          <button 
            className="logout-btn"
            onClick={handleLogout}
          >
            退出登录
          </button>
        </div>
      </div>
      
      <div className="app-content">
        {showTools && (
          <div className="tools-sidebar">
            <h3>治疗工具</h3>
            <div className="tool-section">
              <h4>情绪调节</h4>
              <button className="tool-btn">呼吸练习</button>
              <button className="tool-btn">正念冥想</button>
              <button className="tool-btn">情绪日记</button>
            </div>
            <div className="tool-section">
              <h4>自助资源</h4>
              <button className="tool-btn">应对策略</button>
              <button className="tool-btn">放松技巧</button>
              <button className="tool-btn">心理教育</button>
            </div>
          </div>
        )}
        
        <div className={`chat-container ${showTools ? 'with-tools' : ''}`}>
          <Chatbot
            config={chatConfig}
            messageParser={MessageParser}
            actionProvider={ActionProvider}
          />
        </div>
      </div>
    </div>
  );
}

export default App;
