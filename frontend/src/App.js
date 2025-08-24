import React, { useState } from "react";
import { Chatbot } from "react-chatbot-kit";
import "./App.css";
import MessageParser from "./MessageParser";
import ActionProvider from "./ActionProvider";
import config from "./config";

const App = () => {
  const [showTools, setShowTools] = useState(false);

  return (
    <div className="App">
      <div className="app-header">
        <h1>MindGuide Therapy Assistant</h1>
        <button 
          className="tools-toggle"
          onClick={() => setShowTools(!showTools)}
        >
          {showTools ? '隐藏工具' : '显示工具'}
        </button>
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
            config={config}
            messageParser={MessageParser}
            actionProvider={ActionProvider}
          />
        </div>
      </div>
    </div>
  );
}

export default App;
