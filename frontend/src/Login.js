import React, { useState } from 'react';
import axios from 'axios';
import './Login.css';

const Login = ({ onLogin, onRegister }) => {
  const [isLogin, setIsLogin] = useState(true);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [email, setEmail] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const apiBaseUrl = process.env.REACT_APP_API_BASE_URL || 'http://localhost:5000';

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      if (isLogin) {
        // Login logic
        const response = await axios.post(`${apiBaseUrl}/api/login`, {
          user_info: { username, password }
        });

        if (response.data.success && response.data.validID) {
          onLogin({
            userID: response.data.userID,
            sessionID: response.data.sessionID,
            token: response.data.token,
            username: username
          });
        } else {
          setError(response.data.error || 'Login failed');
        }
      } else {
        // Register logic
        const response = await axios.post(`${apiBaseUrl}/api/register`, {
          user_info: { username, password, email }
        });

        if (response.data.success) {
          // Auto-login after registration
          const loginResponse = await axios.post(`${apiBaseUrl}/api/login`, {
            user_info: { username, password }
          });

          if (loginResponse.data.success && loginResponse.data.validID) {
            onRegister({
              userID: loginResponse.data.userID,
              sessionID: loginResponse.data.sessionID,
              token: loginResponse.data.token,
              username: username
            });
          }
        } else {
          setError(response.data.error || 'Registration failed');
        }
      }
    } catch (error) {
      console.error('Authentication error:', error);
      setError(error.response?.data?.error || 'Authentication failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-container">
      <div className="login-form">
        <h2>{isLogin ? '登录 MindGuide' : '注册 MindGuide'}</h2>
        
        {error && <div className="error-message">{error}</div>}
        
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="username">用户名:</label>
            <input
              type="text"
              id="username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
              placeholder="请输入用户名"
            />
          </div>

          <div className="form-group">
            <label htmlFor="password">密码:</label>
            <input
              type="password"
              id="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              placeholder="请输入密码"
            />
          </div>

          {!isLogin && (
            <div className="form-group">
              <label htmlFor="email">邮箱 (可选):</label>
              <input
                type="email"
                id="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="请输入邮箱"
              />
            </div>
          )}

          <button type="submit" disabled={loading} className="submit-btn">
            {loading ? '处理中...' : (isLogin ? '登录' : '注册')}
          </button>
        </form>

        <div className="switch-mode">
          <p>
            {isLogin ? '没有账号？' : '已有账号？'}
            <button 
              type="button" 
              className="switch-btn"
              onClick={() => {
                setIsLogin(!isLogin);
                setError('');
              }}
            >
              {isLogin ? '立即注册' : '立即登录'}
            </button>
          </p>
        </div>

        <div className="demo-info">
          <h4>演示账号信息:</h4>
          <p>用户名: user1 到 user30</p>
          <p>密码: 查看后端代码中的密码列表</p>
          <p>或者注册新账号进行测试</p>
        </div>
      </div>
    </div>
  );
};

export default Login;