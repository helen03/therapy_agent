import React, { useState } from 'react';

const EnhancedDemoInfo = () => {
  const [activeTab, setActiveTab] = useState('demo');
  
  const demoAccounts = [
    { username: 'user1', role: '新手用户', description: '适合初次体验的用户' },
    { username: 'user10', role: '进阶用户', description: '已使用一段时间的用户' },
    { username: 'user20', role: '高级用户', description: '熟悉所有功能的用户' }
  ];
  
  const features = [
    {
      icon: '🧠',
      title: 'AI 心理分析',
      description: '基于先进的AI技术，提供个性化的心理健康分析'
    },
    {
      icon: '💬',
      title: '智能对话',
      description: '24/7 在线的AI心理顾问，随时倾听您的心声'
    },
    {
      icon: '📊',
      title: '情绪追踪',
      description: '记录和分析情绪变化，帮助您更好地了解自己'
    },
    {
      icon: '🎯',
      title: '个性化方案',
      description: '根据您的具体情况，定制专属的心理健康计划'
    }
  ];
  
  const testimonials = [
    {
      name: '张小明',
      role: '软件工程师',
      content: 'MindGuide 帮助我度过了职业倦怠期，AI的陪伴让我感到不再孤单。',
      rating: 5
    },
    {
      name: '李美丽',
      role: '大学生',
      content: '作为学生，压力很大。MindGuide 的情绪追踪功能让我学会了更好地管理压力。',
      rating: 5
    },
    {
      name: '王大伟',
      role: '产品经理',
      content: '专业的心理健康指导，加上便捷的移动端体验，强烈推荐！',
      rating: 5
    }
  ];

  return (
    <div className="enhanced-demo-info">
      {/* 标签切换 */}
      <div className="demo-tabs">
        <button 
          className={`tab-button ${activeTab === 'demo' ? 'active' : ''}`}
          onClick={() => setActiveTab('demo')}
        >
          演示账号
        </button>
        <button 
          className={`tab-button ${activeTab === 'features' ? 'active' : ''}`}
          onClick={() => setActiveTab('features')}
        >
          功能特色
        </button>
        <button 
          className={`tab-button ${activeTab === 'testimonials' ? 'active' : ''}`}
          onClick={() => setActiveTab('testimonials')}
        >
          用户评价
        </button>
      </div>
      
      {/* 内容区域 */}
      <div className="demo-content">
        {activeTab === 'demo' && (
          <div className="demo-accounts">
            <h4>
              <span className="icon">🔑</span>
              快速体验账号
            </h4>
            <p className="demo-description">选择一个演示账号，立即体验 MindGuide 的全部功能</p>
            
            <div className="account-cards">
              {demoAccounts.map((account, index) => (
                <div key={index} className="account-card">
                  <div className="account-header">
                    <div className="account-avatar">
                      {account.username.slice(-1)}
                    </div>
                    <div className="account-info">
                      <h5>{account.username}</h5>
                      <span className="role-badge">{account.role}</span>
                    </div>
                  </div>
                  <p className="account-desc">{account.description}</p>
                  <div className="account-footer">
                    <span className="password-hint">密码: 123456</span>
                    <button className="copy-btn" onClick={() => navigator.clipboard.writeText(account.username)}>
                      复制用户名
                    </button>
                  </div>
                </div>
              ))}
            </div>
            
            <div className="demo-note">
              <span className="note-icon">ℹ️</span>
              <p>提示：您也可以注册新账号来体验完整的用户流程</p>
            </div>
          </div>
        )}
        
        {activeTab === 'features' && (
          <div className="features-showcase">
            <h4>
              <span className="icon">✨</span>
              核心功能
            </h4>
            
            <div className="features-grid">
              {features.map((feature, index) => (
                <div key={index} className="feature-card">
                  <div className="feature-icon-wrapper">
                    <span className="feature-icon">{feature.icon}</span>
                  </div>
                  <h5 className="feature-title">{feature.title}</h5>
                  <p className="feature-description">{feature.description}</p>
                  <div className="feature-arrow">→</div>
                </div>
              ))}
            </div>
          </div>
        )}
        
        {activeTab === 'testimonials' && (
          <div className="testimonials-section">
            <h4>
              <span className="icon">💝</span>
              用户心声
            </h4>
            
            <div className="testimonials-slider">
              {testimonials.map((testimonial, index) => (
                <div key={index} className="testimonial-card">
                  <div className="testimonial-header">
                    <div className="user-avatar">
                      {testimonial.name[0]}
                    </div>
                    <div className="user-info">
                      <h5>{testimonial.name}</h5>
                      <p>{testimonial.role}</p>
                    </div>
                    <div className="rating">
                      {'★'.repeat(testimonial.rating)}
                    </div>
                  </div>
                  <p className="testimonial-content">"{testimonial.content}"</p>
                  <div className="testimonial-footer">
                    <span className="verified-badge">✓ 已验证</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
      
      {/* 底部行动召唤 */}
      <div className="demo-cta">
        <h5>准备开始您的心灵之旅了吗？</h5>
        <p>加入我们，让 AI 成为您的心灵伙伴</p>
        <div className="cta-buttons">
          <button className="cta-primary">立即注册</button>
          <button className="cta-secondary">了解更多</button>
        </div>
      </div>
    </div>
  );
};

export default EnhancedDemoInfo;