import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { getEnvironment } from './utils/environment';

const MinimalChatTest = () => {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [user, setUser] = useState(null);
  const [session, setSession] = useState(null);

  useEffect(() => {
    // 自动登录
    login();
  }, []);

  const login = async () => {
    try {
      console.log('开始登录...');
      const { apiBaseUrl } = getEnvironment();
      const response = await axios.post(`${apiBaseUrl}/api/login`, {
        user_info: { username: 'user1', password: 'ph6n76gec9' }
      });
      
      console.log('登录响应:', response.data);
      
      if (response.data.success) {
        setUser(response.data.userID);
        setSession(response.data.sessionID);
        setMessages([
          { id: 1, text: response.data.model_prompt, sender: 'bot' }
        ]);
      }
    } catch (error) {
      console.error('登录失败:', error);
    }
  };

  const sendMessage = async () => {
    if (!inputValue.trim() || !user || !session) return;

    const userMessage = {
      id: messages.length + 1,
      text: inputValue,
      sender: 'user'
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      console.log('发送消息:', inputValue);
      console.log('用户信息:', { user, session });
      
      const requestData = {
        choice_info: {
          user_id: user,
          session_id: session,
          user_choice: inputValue,
          input_type: ['open_text']
        }
      };
      
      console.log('请求数据:', requestData);
      
      const { apiBaseUrl } = getEnvironment();
      const response = await axios.post(`${apiBaseUrl}/api/update_session`, requestData);
      
      console.log('收到响应:', response.data);
      
      if (response.data.chatbot_response) {
        const botMessage = {
          id: messages.length + 2,
          text: response.data.chatbot_response,
          sender: 'bot'
        };
        setMessages(prev => [...prev, botMessage]);
      }
    } catch (error) {
      console.error('发送消息失败:', error);
      const errorMessage = {
        id: messages.length + 2,
        text: `发送失败: ${error.message}`,
        sender: 'bot'
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !isLoading) {
      sendMessage();
    }
  };

  return (
    <div style={{ 
      height: '100vh', 
      display: 'flex', 
      flexDirection: 'column',
      backgroundColor: '#f5f5f5',
      fontFamily: 'Arial, sans-serif'
    }}>
      <div style={{ 
        padding: '20px', 
        backgroundColor: 'white', 
        boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
        zIndex: 1000
      }}>
        <h1>🧪 最小化聊天测试</h1>
        <p>这是一个最小化的聊天组件，用于测试基本的API连接功能</p>
        <div style={{ marginTop: '10px' }}>
          <strong>状态信息:</strong>
          <ul>
            <li>用户ID: {user || '未登录'}</li>
            <li>会话ID: {session || '无'}</li>
            <li>消息数量: {messages.length}</li>
            <li>加载状态: {isLoading ? '加载中' : '空闲'}</li>
          </ul>
        </div>
      </div>
      
      <div style={{ 
        flex: 1, 
        padding: '20px',
        overflow: 'hidden',
        display: 'flex',
        flexDirection: 'column'
      }}>
        <div style={{
          flex: 1,
          overflowY: 'auto',
          backgroundColor: 'white',
          borderRadius: '8px',
          padding: '20px',
          marginBottom: '20px',
          boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
        }}>
          {messages.map(message => (
            <div key={message.id} style={{
              margin: '10px 0',
              padding: '12px 16px',
              borderRadius: '18px',
              maxWidth: '70%',
              clear: 'both',
              backgroundColor: message.sender === 'user' ? '#007bff' : '#e9ecef',
              color: message.sender === 'user' ? 'white' : 'black',
              marginLeft: message.sender === 'user' ? 'auto' : '0',
              marginRight: message.sender === 'user' ? '0' : 'auto',
              wordWrap: 'break-word'
            }}>
              {message.text}
            </div>
          ))}
          {isLoading && (
            <div style={{
              margin: '10px 0',
              padding: '12px 16px',
              borderRadius: '18px',
              backgroundColor: '#e9ecef',
              color: 'black',
              marginLeft: '0',
              marginRight: '0',
              width: 'fit-content'
            }}>
              正在输入...
            </div>
          )}
        </div>
        
        <div style={{ display: 'flex', gap: '10px' }}>
          <input
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="输入消息..."
            disabled={isLoading || !user || !session}
            style={{
              flex: 1,
              padding: '12px 16px',
              border: '1px solid #ddd',
              borderRadius: '25px',
              fontSize: '14px',
              outline: 'none',
              backgroundColor: (!user || !session) ? '#f8f9fa' : 'white'
            }}
          />
          <button
            onClick={sendMessage}
            disabled={isLoading || !inputValue.trim() || !user || !session}
            style={{
              padding: '12px 24px',
              backgroundColor: '#007bff',
              color: 'white',
              border: 'none',
              borderRadius: '25px',
              cursor: 'pointer',
              fontSize: '14px',
              fontWeight: '500',
              opacity: (isLoading || !inputValue.trim() || !user || !session) ? 0.5 : 1
            }}
          >
            发送
          </button>
        </div>
        
        {(!user || !session) && (
          <div style={{
            marginTop: '10px',
            padding: '10px',
            backgroundColor: '#fff3cd',
            border: '1px solid #ffeaa7',
            borderRadius: '4px',
            color: '#856404',
            fontSize: '12px'
          }}>
            正在登录中...
          </div>
        )}
      </div>
    </div>
  );
};

export default MinimalChatTest;