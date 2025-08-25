import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import { getEnvironment } from './utils/environment';
import './Login.css';

const Login = ({ onLogin, onRegister }) => {
  const [isLogin, setIsLogin] = useState(true);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [email, setEmail] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const [rememberMe, setRememberMe] = useState(false);

  const { apiBaseUrl } = getEnvironment();
  const usernameRef = useRef(null);

  // 自动聚焦用户名输入框
  useEffect(() => {
    if (usernameRef.current) {
      usernameRef.current.focus();
    }
  }, []);

  // 检查本地存储中的记住用户名
  useEffect(() => {
    const savedUsername = localStorage.getItem('rememberedUsername');
    if (savedUsername) {
      setUsername(savedUsername);
      setRememberMe(true);
    }
  }, []);

  // 表单验证
  const validateForm = () => {
    if (!username.trim()) {
      setError('请输入用户名');
      return false;
    }
    if (!password) {
      setError('请输入密码');
      return false;
    }
    if (!isLogin && email && !/\S+@\S+\.\S+/.test(email)) {
      setError('请输入有效的邮箱地址');
      return false;
    }
    return true;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    
    if (!validateForm()) return;

    setLoading(true);

    try {
      if (isLogin) {
        // 登录逻辑
        const response = await axios.post(`${apiBaseUrl}/api/login`, {
          user_info: { username, password }
        });

        if (response.data.success && response.data.validID) {
          // 处理记住我功能
          if (rememberMe) {
            localStorage.setItem('rememberedUsername', username);
          } else {
            localStorage.removeItem('rememberedUsername');
          }

          onLogin({
            userID: response.data.userID,
            sessionID: response.data.sessionID,
            token: response.data.token,
            username: username,
            model_prompt: response.data.model_prompt,
            choices: response.data.choices
          });
        } else {
          setError(response.data.error || '登录失败');
        }
      } else {
        // 注册逻辑
        const response = await axios.post(`${apiBaseUrl}/api/register`, {
          user_info: { username, password, email }
        });

        if (response.data.success) {
          // 自动登录
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
          setError(response.data.error || '注册失败');
        }
      }
    } catch (error) {
      console.error('Authentication error:', error);
      setError(error.response?.data?.error || '网络错误，请稍后重试');
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (field, value) => {
    // 清除错误信息
    if (error) setError('');
    
    switch (field) {
      case 'username':
        setUsername(value);
        break;
      case 'password':
        setPassword(value);
        break;
      case 'email':
        setEmail(value);
        break;
      default:
        break;
    }
  };

  const togglePasswordVisibility = () => {
    setShowPassword(!showPassword);
  };

  const switchMode = () => {
    setIsLogin(!isLogin);
    setError('');
    setUsername('');
    setPassword('');
    setEmail('');
  };

  return (
    <div className="login-container">
      {/* 背景装饰 */}
      <div className="background-shapes">
        <div className="shape shape-1"></div>
        <div className="shape shape-2"></div>
        <div className="shape shape-3"></div>
        <div className="shape shape-4"></div>
        <div className="shape shape-5"></div>
      </div>

      <div className="login-form">
        {/* 品牌标识 */}
        <div className="brand-header">
          <div className="brand-icon">
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M12 2L2 7V12C2 16.5 4.23 20.68 12 22C19.77 20.68 22 16.5 22 12V7L12 2Z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              <path d="M12 8V16" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              <path d="M8 12H16" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
          </div>
          <h1 className="brand-title">MindGuide</h1>
          <p className="brand-subtitle">您的心灵健康伙伴</p>
        </div>

        {/* 登录表单 */}
        <form onSubmit={handleSubmit} className="form-container">
          <h2 className="form-title">
            {isLogin ? '欢迎回来' : '加入我们'}
          </h2>
          <p className="form-subtitle">
            {isLogin ? '登录您的账户继续治疗之旅' : '创建账户开始您的心灵疗愈'}
          </p>

          {error && (
            <div className="error-message">
              <svg className="error-icon" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
              </svg>
              {error}
            </div>
          )}

          <div className="form-group">
            <label htmlFor="username">用户名</label>
            <div className="input-wrapper">
              <input
                ref={usernameRef}
                id="username"
                type="text"
                value={username}
                onChange={(e) => handleInputChange('username', e.target.value)}
                placeholder="请输入用户名"
                className="form-input"
                disabled={loading}
              />
              <svg className="input-icon" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clipRule="evenodd" />
              </svg>
            </div>
          </div>

          <div className="form-group">
            <label htmlFor="password">密码</label>
            <div className="input-wrapper">
              <input
                id="password"
                type={showPassword ? "text" : "password"}
                value={password}
                onChange={(e) => handleInputChange('password', e.target.value)}
                placeholder="请输入密码"
                className="form-input"
                disabled={loading}
              />
              <svg className="input-icon" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M5 9V7a5 5 0 0110 0v2a2 2 0 012 2v5a2 2 0 01-2 2H5a2 2 0 01-2-2v-5a2 2 0 012-2zm8-2v2H7V7a3 3 0 016 0z" clipRule="evenodd" />
              </svg>
              <button
                type="button"
                className="password-toggle"
                onClick={togglePasswordVisibility}
                disabled={loading}
              >
                {showPassword ? (
                  <svg viewBox="0 0 20 20" fill="currentColor">
                    <path d="M10 12a2 2 0 100-4 2 2 0 000 4z" />
                    <path fillRule="evenodd" d="M.458 10C1.732 5.943 5.522 3 10 3s8.268 2.943 9.542 7c-1.274 4.057-5.064 7-9.542 7S1.732 14.057.458 10zM14 10a4 4 0 11-8 0 4 4 0 018 0z" clipRule="evenodd" />
                  </svg>
                ) : (
                  <svg viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M3.707 2.293a1 1 0 00-1.414 1.414l14 14a1 1 0 001.414-1.414l-1.473-1.473A10.014 10.014 0 0019.542 10C18.268 5.943 14.478 3 10 3a9.958 9.958 0 00-4.512 1.074l-1.78-1.781zm4.261 4.26l1.514 1.515a2.003 2.003 0 012.45 2.45l1.514 1.514a4 4 0 00-5.478-5.478z" clipRule="evenodd" />
                    <path d="M12.454 16.697L9.75 13.992a4 4 0 01-3.742-3.741L2.335 6.578A9.98 9.98 0 00.458 10c1.274 4.057 5.065 7 9.542 7 .847 0 1.669-.105 2.454-.303z" />
                  </svg>
                )}
              </button>
            </div>
          </div>

          {!isLogin && (
            <div className="form-group">
              <label htmlFor="email">邮箱 (可选)</label>
              <div className="input-wrapper">
                <input
                  id="email"
                  type="email"
                  value={email}
                  onChange={(e) => handleInputChange('email', e.target.value)}
                  placeholder="请输入邮箱"
                  className="form-input"
                  disabled={loading}
                />
                <svg className="input-icon" viewBox="0 0 20 20" fill="currentColor">
                  <path d="M2.003 5.884L10 9.882l7.997-3.998A2 2 0 0016 4H4a2 2 0 00-1.997 1.884z" />
                  <path d="M18 8.118l-8 4-8-4V14a2 2 0 002 2h12a2 2 0 002-2V8.118z" />
                </svg>
              </div>
            </div>
          )}

          {isLogin && (
            <div className="form-options">
              <label className="checkbox-label">
                <input
                  type="checkbox"
                  checked={rememberMe}
                  onChange={(e) => setRememberMe(e.target.checked)}
                  disabled={loading}
                />
                <span className="checkbox-text">记住我</span>
              </label>
              <a href="#" className="forgot-link">忘记密码？</a>
            </div>
          )}

          <button
            type="submit"
            disabled={loading}
            className="submit-btn"
          >
            {loading ? (
              <div className="loading-spinner">
                <div className="spinner"></div>
                <span>处理中...</span>
              </div>
            ) : (
              <span>{isLogin ? '登录' : '注册'}</span>
            )}
          </button>
        </form>

        {/* 切换登录/注册 */}
        <div className="switch-mode">
          <p>
            {isLogin ? '还没有账号？' : '已有账号？'}
            <button
              type="button"
              className="switch-btn"
              onClick={switchMode}
              disabled={loading}
            >
              {isLogin ? '立即注册' : '立即登录'}
            </button>
          </p>
        </div>

        {/* 演示信息 */}
        <div className="demo-info">
          <h4>演示账号</h4>
          <div className="demo-accounts">
            <div className="demo-account">
              <strong>用户名:</strong> user1
              <br />
              <strong>密码:</strong> ph6n76gec9
            </div>
            <div className="demo-account">
              <strong>用户名:</strong> user2
              <br />
              <strong>密码:</strong> ph6n76gec9
            </div>
          </div>
          <p className="demo-note">
            可使用 user1 到 user30 的任意账号进行测试
          </p>
        </div>
      </div>
    </div>
  );
};

export default Login;