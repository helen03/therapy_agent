import React, { useState, useEffect } from "react";
import { Chatbot, createChatBotMessage } from "react-chatbot-kit";
import "./App.css";
import MessageParser from "./MessageParser";
import ActionProvider from "./ActionProvider";
import baseConfig from "./config";
import Login from "./Login";
import { logEnvironment } from "./utils/environment";

const App = () => {
  const [showTools, setShowTools] = useState(false);
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [userInfo, setUserInfo] = useState(null);
  const [chatConfig, setChatConfig] = useState(baseConfig);
  const [ultraThinkMode, setUltraThinkMode] = useState(false);

  useEffect(() => {
    logEnvironment();
  }, []);

  /** 登录逻辑 */
  const handleLogin = (userData) => {
    console.log("App.js handleLogin called with:", userData);
    setUserInfo(userData);
    setIsLoggedIn(true);

    // Store user info in localStorage for the new HTML page
    const userSessionData = {
      userID: userData.userID,
      sessionID: userData.sessionID,
      username: userData.username,
      token: userData.token,
      model_prompt: userData.model_prompt || "你好！欢迎回来。今天感觉怎么样？有什么想和我聊的吗？",
      choices: userData.choices || []
    };
    
    localStorage.setItem('userSessionData', JSON.stringify(userSessionData));
    
    // Redirect to the new therapy chat page
    window.location.href = '/therapy-chat.html';
  };

  /** 注册逻辑 */
  const handleRegister = (userData) => {
    setUserInfo(userData);
    setIsLoggedIn(true);

    // Store user info in localStorage for the new HTML page
    const userSessionData = {
      userID: userData.userID,
      sessionID: userData.sessionID,
      username: userData.username,
      token: userData.token,
      model_prompt: "欢迎加入MindGuide！让我们一起开始您的第一次治疗会话。",
      choices: userData.choices || []
    };
    
    localStorage.setItem('userSessionData', JSON.stringify(userSessionData));
    
    // Redirect to the new therapy chat page
    window.location.href = '/therapy-chat.html';
  };

  /** 登出 */
  const handleLogout = () => {
    setIsLoggedIn(false);
    setUserInfo(null);
    setChatConfig(baseConfig); // 重置 config
  };

  /** UltraThink 模式切换 */
  const toggleUltraThinkMode = () => {
    setUltraThinkMode(!ultraThinkMode);
    console.log("UltraThink mode toggled:", !ultraThinkMode);
  };

  /** 未登录时显示登录页 */
  if (!isLoggedIn) {
    return (
      <div className="app-container">
        <div className="app-header">
          <h1>MindGuide Therapy Assistant</h1>
          <div className="header-controls">
            <button className="tools-toggle" onClick={toggleUltraThinkMode}>
              {ultraThinkMode ? "退出深度思考" : "🧠 UltraThink"}
            </button>
          </div>
        </div>
        <Login onLogin={handleLogin} onRegister={handleRegister} />
      </div>
    );
  }

  /** 登录后显示聊天 + 工具栏 */
  return (
    <div className="app-container">
      <div className="app-header">
        <h1>MindGuide Therapy Assistant</h1>
        <div className="header-controls">
          <span className="user-info">欢迎, {userInfo?.username}</span>
          <button className="tools-toggle" onClick={() => setShowTools(!showTools)}>
            {showTools ? "隐藏工具" : "显示工具"}
          </button>
          <button className="tools-toggle" onClick={toggleUltraThinkMode}>
            {ultraThinkMode ? "退出深度思考" : "🧠 UltraThink"}
          </button>
          <button className="logout-btn" onClick={handleLogout}>
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

        <div className={`chat-container ${showTools ? "with-tools" : ""}`}>
          <Chatbot
            key={chatConfig.state.sessionID}   // 保证更新时强制挂载
            config={chatConfig}
            messageParser={MessageParser}
            actionProvider={ActionProvider}
          />
        </div>
      </div>
    </div>
  );
};

export default App;
