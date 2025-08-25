import React, { useState, useEffect } from 'react';
import { Chatbot } from 'react-chatbot-kit';
import { createChatBotMessage } from 'react-chatbot-kit';
import MessageParser from './MessageParser';
import ActionProvider from './ActionProvider';
import './App.css';

// 简化的配置用于测试
const testConfig = {
  botName: "TestBot",
  initialMessages: [
    createChatBotMessage("你好！我是测试机器人。", {
      withAvatar: true,
      delay: 0,
    }),
    createChatBotMessage("今天感觉怎么样？", {
      withAvatar: true,
      delay: 1500,
    })
  ],
  state: {
    userState: 1,
    sessionID: "test_session_123",
    username: "test_user",
    inputType: ["open_text"],
    currentOptionToShow: null,
    protocols: [],
    askingForProtocol: false,
    initialChoices: [],
    messages: []
  },
  customComponents: {
    header: () => <div style={{height: '15px', fontFamily: 'Trebuchet MS', fontSize: "1em", textAlign: "center", color: '#fff', paddingTop: '1em', paddingBottom: '1em'}}>TestBot</div>,
  },
  widgets: [
    {
      widgetName: "YesNo",
      widgetFunc: (props) => {
        console.log('YesNo widget props:', props);
        return (
          <div style={{ display: 'flex', gap: '10px', marginTop: '10px' }}>
            <button onClick={() => props.actionProvider.handleButtons(props.state.userState, props.state.sessionID, "Yes", ["yes", "no"])}>Yes</button>
            <button onClick={() => props.actionProvider.handleButtons(props.state.userState, props.state.sessionID, "No", ["yes", "no"])}>No</button>
          </div>
        );
      },
      mapStateToProps: ["userState", "sessionID"],
    },
  ],
};

const TestChat = () => {
  const [chatConfig, setChatConfig] = useState(testConfig);

  useEffect(() => {
    console.log('TestChat component mounted');
    console.log('Chat config:', chatConfig);
  }, [chatConfig]);

  return (
    <div style={{ 
      height: '100vh', 
      display: 'flex', 
      flexDirection: 'column',
      backgroundColor: '#f5f5f5'
    }}>
      <div style={{ 
        padding: '20px', 
        backgroundColor: 'white', 
        boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
        zIndex: 1000
      }}>
        <h1>🧪 聊天机器人测试页面</h1>
        <p>这是一个简化的测试页面，用于验证react-chatbot-kit是否正常工作</p>
        <div style={{ marginTop: '10px' }}>
          <strong>测试信息:</strong>
          <ul>
            <li>用户ID: {chatConfig.state.userState}</li>
            <li>会话ID: {chatConfig.state.sessionID}</li>
            <li>用户名: {chatConfig.state.username}</li>
            <li>输入类型: {JSON.stringify(chatConfig.state.inputType)}</li>
          </ul>
        </div>
      </div>
      
      <div style={{ 
        flex: 1, 
        padding: '20px',
        overflow: 'hidden'
      }}>
        <Chatbot
          config={chatConfig}
          messageParser={MessageParser}
          actionProvider={ActionProvider}
        />
      </div>
    </div>
  );
};

export default TestChat;