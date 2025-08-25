import React, { useState, useEffect, useCallback, useRef } from 'react';
import axios from 'axios';
import './Login.css';
import './LoginEnhanced.css';
import ParticleBackground from './components/ParticleBackground';
import WaveBackground from './components/WaveBackground';
import { LoadingSpinner, StepIndicator } from './components/UIElements';
import SocialLogin from './components/SocialLogin';
import BrandBadges from './components/BrandBadges';
import EnhancedDemoInfo from './components/EnhancedDemoInfo';

const Login = ({ onLogin, onRegister }) => {
  const [isLogin, setIsLogin] = useState(true);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [email, setEmail] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [rememberMe, setRememberMe] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const [formErrors, setFormErrors] = useState({
    username: '',
    password: '',
    email: ''
  });
  const [touched, setTouched] = useState({
    username: false,
    password: false,
    email: false
  });
  const [showSocialLogin, setShowSocialLogin] = useState(false);
  const [formProgress, setFormProgress] = useState(0);
  const [showSuccess, setShowSuccess] = useState(false);
  const [successMessage, setSuccessMessage] = useState('');
  const [isTransitioning, setIsTransitioning] = useState(false);
  const [showDemoInfo, setShowDemoInfo] = useState(false);

  const apiBaseUrl = process.env.REACT_APP_API_BASE_URL || 'http://localhost:5002';
  const usernameRef = useRef(null);

  // 表单验证规则
  const validationRules = {
    username: {
      required: true,
      minLength: 3,
      maxLength: 20,
      pattern: /^[a-zA-Z0-9_]+$/,
      message: '用户名必须是3-20个字符，只能包含字母、数字和下划线'
    },
    password: {
      required: true,
      minLength: 6,
      message: '密码至少需要6个字符'
    },
    email: {
      required: false,
      pattern: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
      message: '请输入有效的邮箱地址'
    }
  };

  // 实时验证函数
  const validateField = useCallback((fieldName, value) => {
    const rules = validationRules[fieldName];
    if (!rules) return '';

    if (rules.required && !value.trim()) {
      return `${fieldName === 'username' ? '用户名' : fieldName === 'password' ? '密码' : '邮箱'}不能为空`;
    }

    if (value && rules.minLength && value.length < rules.minLength) {
      return rules.message;
    }

    if (value && rules.maxLength && value.length > rules.maxLength) {
      return `${fieldName === 'username' ? '用户名' : '邮箱'}不能超过${rules.maxLength}个字符`;
    }

    if (value && rules.pattern && !rules.pattern.test(value)) {
      return rules.message;
    }

    return '';
  }, []);

  // 防抖函数
  const debounce = (func, wait) => {
    let timeout;
    return function executedFunction(...args) {
      const later = () => {
        clearTimeout(timeout);
        func(...args);
      };
      clearTimeout(timeout);
      timeout = setTimeout(later, wait);
    };
  };

  // 防抖验证函数
  const debouncedValidate = useCallback(
    debounce((fieldName, value) => {
      const error = validateField(fieldName, value);
      setFormErrors(prev => ({
        ...prev,
        [fieldName]: error
      }));
    }, 300),
    [validateField]
  );

  // 计算表单完成进度
  const calculateFormProgress = useCallback(() => {
    let progress = 0;
    const fields = ['username', 'password'];
    if (!isLogin) fields.push('email');
    
    fields.forEach(field => {
      const value = field === 'username' ? username : 
                   field === 'password' ? password : email;
      if (value && !validateField(field, value)) {
        progress += 100 / fields.length;
      }
    });
    
    setFormProgress(Math.round(progress));
  }, [username, password, email, isLogin, validateField]);

  // 处理输入变化
  const handleInputChange = (fieldName, value) => {
    switch (fieldName) {
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

    // 使用防抖验证
    debouncedValidate(fieldName, value);
    // 更新进度
    calculateFormProgress();
  };

  // 处理失焦事件
  const handleBlur = (fieldName) => {
    setTouched(prev => ({
      ...prev,
      [fieldName]: true
    }));
  };

  // 检查表单是否有效
  const isFormValid = useCallback(() => {
    const usernameError = validateField('username', username);
    const passwordError = validateField('password', password);
    const emailError = isLogin ? '' : validateField('email', email);

    return !usernameError && !passwordError && !emailError && username && password;
  }, [username, password, email, isLogin, validateField]);

  // 从本地存储加载记住的凭据
  useEffect(() => {
    const savedCredentials = localStorage.getItem('rememberedCredentials');
    if (savedCredentials) {
      try {
        const { username: savedUsername, remember: savedRemember } = JSON.parse(savedCredentials);
        if (savedRemember) {
          setUsername(savedUsername);
          setRememberMe(true);
        }
      } catch (error) {
        console.error('Error loading saved credentials:', error);
      }
    }
  }, []);

  // 组件加载时聚焦用户名输入框
  useEffect(() => {
    if (usernameRef.current) {
      usernameRef.current.focus();
    }
  }, []);

  // 处理键盘事件
  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      if (isFormValid()) {
        handleSubmit(e);
      }
    }
  };

  // 处理社交登录
  const handleSocialLogin = (provider) => {
    console.log(`Social login with ${provider}`);
    // 这里可以添加实际的社交登录逻辑
    setSuccessMessage(`正在连接到 ${provider}...`);
    setShowSuccess(true);
    setTimeout(() => setShowSuccess(false), 3000);
  };

  // 处理模式切换
  const handleModeSwitch = () => {
    setIsTransitioning(true);
    setTimeout(() => {
      setIsLogin(!isLogin);
      setError('');
      setFormProgress(0);
      setIsTransitioning(false);
    }, 300);
  };

  // 显示成功消息
  const showSuccessMessage = (message) => {
    setSuccessMessage(message);
    setShowSuccess(true);
    setTimeout(() => setShowSuccess(false), 3000);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // 标记所有字段为已触摸
    setTouched({
      username: true,
      password: true,
      email: true
    });

    // 验证所有字段
    const usernameError = validateField('username', username);
    const passwordError = validateField('password', password);
    const emailError = isLogin ? '' : validateField('email', email);

    setFormErrors({
      username: usernameError,
      password: passwordError,
      email: emailError
    });

    // 如果有错误，不提交
    if (usernameError || passwordError || emailError) {
      return;
    }

    setError('');
    setLoading(true);

    try {
      if (isLogin) {
        // Login logic
        const response = await axios.post(`${apiBaseUrl}/api/login`, {
          user_info: { username, password }
        });

        if (response.data.success && response.data.validID) {
          showSuccessMessage('登录成功！正在跳转...');
          // 处理记住我功能
          if (rememberMe) {
            localStorage.setItem('rememberedCredentials', JSON.stringify({
              username,
              remember: true
            }));
          } else {
            localStorage.removeItem('rememberedCredentials');
          }

          setTimeout(() => {
            onLogin({
              userID: response.data.userID,
              sessionID: response.data.sessionID,
              token: response.data.token,
              username: username,
              model_prompt: response.data.model_prompt,
              choices: response.data.choices
            });
          }, 1500);
        } else {
          setError(response.data.error || '登录失败');
        }
      } else {
        // Register logic
        const response = await axios.post(`${apiBaseUrl}/api/register`, {
          user_info: { username, password, email }
        });

        if (response.data.success) {
          showSuccessMessage('注册成功！正在自动登录...');
          // Auto-login after registration
          const loginResponse = await axios.post(`${apiBaseUrl}/api/login`, {
            user_info: { username, password }
          });

          if (loginResponse.data.success && loginResponse.data.validID) {
            // 处理记住我功能
            if (rememberMe) {
              localStorage.setItem('rememberedCredentials', JSON.stringify({
                username,
                remember: true
              }));
            }

            setTimeout(() => {
              onRegister({
                userID: loginResponse.data.userID,
                sessionID: loginResponse.data.sessionID,
                token: loginResponse.data.token,
                username: username
              });
            }, 1500);
          }
        } else {
          setError(response.data.error || '注册失败');
        }
      }
    } catch (error) {
      console.error('Authentication error:', error);
      setError(error.response?.data?.error || '认证失败');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-container enhanced">
      {/* 增强背景效果 */}
      <ParticleBackground />
      <WaveBackground />
      
      {/* 浮动几何形状 */}
      <div className="floating-shapes">
        <div className="shape"></div>
        <div className="shape"></div>
        <div className="shape"></div>
        <div className="shape"></div>
        <div className="shape"></div>
      </div>

      {/* 成功提示 */}
      {showSuccess && (
        <div className="success-notification">
          <div className="success-icon">✓</div>
          <div className="success-message">{successMessage}</div>
        </div>
      )}

      <div className={`login-form ${isTransitioning ? 'transitioning' : ''}`}>
        {/* 品牌标识区域 */}
        <div className="brand-section">
          <div className="brand-logo">
            <svg width="48" height="48" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
              <circle cx="24" cy="24" r="20" fill="url(#brainGradient)"/>
              <path d="M24 12C18 12 14 16 14 22C14 26 16 28 18 28C20 28 22 26 22 24C22 22 20 20 18 20" stroke="white" strokeWidth="2" strokeLinecap="round"/>
              <path d="M24 12C30 12 34 16 34 22C34 26 32 28 30 28C28 28 26 26 26 24C26 22 28 20 30 20" stroke="white" strokeWidth="2" strokeLinecap="round"/>
              <path d="M20 28C20 30 22 32 24 32C26 32 28 30 28 28" stroke="white" strokeWidth="2" strokeLinecap="round"/>
              <circle cx="20" cy="22" r="1.5" fill="white"/>
              <circle cx="28" cy="22" r="1.5" fill="white"/>
              <defs>
                <linearGradient id="brainGradient" x1="24" y1="4" x2="24" y2="44" gradientUnits="userSpaceOnUse">
                  <stop stopColor="#6366f1"/>
                  <stop offset="1" stopColor="#8b5cf6"/>
                </linearGradient>
              </defs>
            </svg>
          </div>
          <h1 className="brand-title">MindGuide</h1>
          <p className="brand-tagline">您的心灵健康伙伴</p>
        </div>

        <h2>{isLogin ? '欢迎回来' : '加入我们'}</h2>
        
        {/* 步骤指示器 */}
        <StepIndicator 
          currentStep={formProgress === 100 ? 1 : 0} 
          steps={isLogin ? ['填写信息', '完成登录'] : ['创建账号', '开始使用']} 
        />
        
        {/* 进度条 */}
        <div className="form-progress">
          <div className="progress-track">
            <div 
              className="progress-fill" 
              style={{ width: `${formProgress}%` }}
            ></div>
          </div>
          <span className="progress-text">{formProgress}% 完成</span>
        </div>
        
        {error && <div className="error-message">{error}</div>}
        
        <form onSubmit={handleSubmit} onKeyDown={handleKeyDown}>
          <div className="form-group">
            <label htmlFor="username">用户名</label>
            <input
              type="text"
              id="username"
              ref={usernameRef}
              value={username}
              onChange={(e) => handleInputChange('username', e.target.value)}
              onBlur={() => handleBlur('username')}
              required
              placeholder="请输入您的用户名"
              className={touched.username && formErrors.username ? 'error' : ''}
              aria-invalid={touched.username && formErrors.username ? 'true' : 'false'}
              aria-describedby={touched.username && formErrors.username ? 'username-error' : undefined}
              autoComplete="username"
            />
            <div className="input-icon">
              <svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M10 9C11.1046 9 12 8.10457 12 7C12 5.89543 11.1046 5 10 5C8.89543 5 8 5.89543 8 7C8 8.10457 8.89543 9 10 9Z" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
                <path d="M10 12C7.79086 12 6 13.7909 6 16H14C14 13.7909 12.2091 12 10 12Z" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
              </svg>
            </div>
            {touched.username && formErrors.username && (
              <div className="field-error" id="username-error">
                {formErrors.username}
              </div>
            )}
          </div>

          <div className="form-group">
            <label htmlFor="password">密码</label>
            <div className="password-input-wrapper">
              <input
                type={showPassword ? 'text' : 'password'}
                id="password"
                value={password}
                onChange={(e) => handleInputChange('password', e.target.value)}
                onBlur={() => handleBlur('password')}
                required
                placeholder="请输入您的密码"
                className={touched.password && formErrors.password ? 'error' : ''}
                aria-invalid={touched.password && formErrors.password ? 'true' : 'false'}
                aria-describedby={touched.password && formErrors.password ? 'password-error' : undefined}
                autoComplete={isLogin ? 'current-password' : 'new-password'}
              />
              <button
                type="button"
                className="password-toggle"
                onClick={() => setShowPassword(!showPassword)}
                aria-label={showPassword ? '隐藏密码' : '显示密码'}
                tabIndex="-1"
              >
                <svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
                  {showPassword ? (
                    <>
                      <path d="M10 12C11.1046 12 12 11.1046 12 10C12 8.89543 11.1046 8 10 8C8.89543 8 8 8.89543 8 10C8 11.1046 8.89543 12 10 12Z" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
                      <path d="M2 10C2 10 5 5 10 5C15 5 18 10 18 10C18 10 15 15 10 15C5 15 2 10 2 10Z" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
                    </>
                  ) : (
                    <>
                      <path d="M10 12C11.1046 12 12 11.1046 12 10C12 8.89543 11.1046 8 10 8C8.89543 8 8 8.89543 8 10C8 11.1046 8.89543 12 10 12Z" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
                      <path d="M3 10C3 10 5.5 6 10 6C14.5 6 17 10 17 10C17 10 14.5 14 10 14C5.5 14 3 10 3 10Z" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
                      <path d="M2 2L18 18" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
                    </>
                  )}
                </svg>
              </button>
            </div>
            <div className="input-icon">
              <svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M5 9V7C5 4.23858 7.23858 2 10 2C12.7614 2 15 4.23858 15 7V9M10 14C10.5523 14 11 13.5523 11 13C11 12.4477 10.5523 12 10 12C9.44772 12 9 12.4477 9 13C9 13.5523 9.44772 14 10 14Z" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
                <rect x="3" y="9" width="14" height="9" rx="2" stroke="currentColor" strokeWidth="1.5"/>
              </svg>
            </div>
            {touched.password && formErrors.password && (
              <div className="field-error" id="password-error">
                {formErrors.password}
              </div>
            )}
          </div>

          {isLogin && (
            <div className="form-group remember-me">
              <label className="checkbox-label">
                <input
                  type="checkbox"
                  checked={rememberMe}
                  onChange={(e) => setRememberMe(e.target.checked)}
                />
                <span className="checkmark"></span>
                记住我
              </label>
            </div>
          )}

          {!isLogin && (
            <div className="form-group">
              <label htmlFor="email">邮箱地址</label>
              <input
                type="email"
                id="email"
                value={email}
                onChange={(e) => handleInputChange('email', e.target.value)}
                onBlur={() => handleBlur('email')}
                placeholder="请输入您的邮箱（可选）"
                className={touched.email && formErrors.email ? 'error' : ''}
                aria-invalid={touched.email && formErrors.email ? 'true' : 'false'}
                aria-describedby={touched.email && formErrors.email ? 'email-error' : undefined}
                autoComplete="email"
              />
              <div className="input-icon">
                <svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M3 8L10 13L17 8M3 5H17C17.5523 5 18 5.44772 18 6V14C18 14.5523 17.5523 15 17 15H3C2.44772 15 2 14.5523 2 14V6C2 5.44772 2.44772 5 3 5Z" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
                </svg>
              </div>
              {touched.email && formErrors.email && (
                <div className="field-error" id="email-error">
                  {formErrors.email}
                </div>
              )}
            </div>
          )}

          <button 
            type="submit" 
            disabled={loading || !isFormValid()} 
            className="submit-btn"
            aria-busy={loading}
          >
            {loading && <div className="loading-spinner"></div>}
            {loading ? '处理中...' : (isLogin ? '开始心灵之旅' : '开启新篇章')}
          </button>
        </form>

        {/* 社交登录选项 */}
        <div className="social-login-toggle">
          <button 
            type="button"
            className="toggle-social-btn"
            onClick={() => setShowSocialLogin(!showSocialLogin)}
          >
            {showSocialLogin ? '收起社交登录' : '更多登录方式'}
            <span className={`toggle-icon ${showSocialLogin ? 'up' : 'down'}`}>▼</span>
          </button>
        </div>

        {showSocialLogin && <SocialLogin onSocialLogin={handleSocialLogin} />}

        <div className="switch-mode">
          <p>
            {isLogin ? '还没有账号？' : '已有账号？'}
            <button 
              type="button" 
              className="switch-btn"
              onClick={handleModeSwitch}
            >
              {isLogin ? '立即注册' : '立即登录'}
            </button>
          </p>
        </div>

        {/* 演示信息切换按钮 */}
        <div className="demo-info-toggle">
          <button 
            type="button"
            className="toggle-demo-btn"
            onClick={() => setShowDemoInfo(!showDemoInfo)}
          >
            {showDemoInfo ? '隐藏演示信息' : '显示演示账号'}
            <span className={`toggle-icon ${showDemoInfo ? 'up' : 'down'}`}>▼</span>
          </button>
        </div>

        {/* 增强的演示信息 */}
        {showDemoInfo && <EnhancedDemoInfo />}
        
        {/* 品牌徽章 */}
        <BrandBadges />
      </div>
    </div>
  );
};

export default Login;