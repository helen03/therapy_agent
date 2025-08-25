import React from 'react';

const BrandBadges = () => {
  const certifications = [
    {
      title: 'HIPAA 合规',
      description: '符合医疗隐私保护标准',
      icon: '🏥',
      color: '#10b981'
    },
    {
      title: 'ISO 27001',
      description: '信息安全管理体系认证',
      icon: '🔐',
      color: '#3b82f6'
    },
    {
      title: 'GDPR 合规',
      description: '欧盟数据保护法规合规',
      icon: '🛡️',
      color: '#8b5cf6'
    },
    {
      title: '心理健康认证',
      description: '专业心理健康服务认证',
      icon: '🧠',
      color: '#ec4899'
    }
  ];

  const achievements = [
    { icon: '🏆', text: '10万+ 用户信赖' },
    { icon: '⭐', text: '4.9 评分' },
    { icon: '🎯', text: '95% 满意度' },
    { icon: '🌍', text: '50+ 国家' }
  ];

  return (
    <div className="brand-badges">
      {/* 认证标识 */}
      <div className="certification-section">
        <h3 className="section-title">
          <span className="title-icon">✨</span>
          专业认证与保障
        </h3>
        <div className="certification-grid">
          {certifications.map((cert, index) => (
            <div key={index} className="certification-card">
              <div className="cert-icon" style={{ backgroundColor: cert.color + '20' }}>
                <span className="icon-emoji">{cert.icon}</span>
              </div>
              <div className="cert-content">
                <h4 className="cert-title">{cert.title}</h4>
                <p className="cert-desc">{cert.description}</p>
              </div>
              <div className="cert-badge">
                <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor">
                  <path d="M10.97 4.97a.75.75 0 0 1 1.07 1.05l-3.99 4.99a.75.75 0 0 1-1.08.02L4.324 8.384a.75.75 0 1 1 1.06-1.06l2.094 2.093 3.473-4.425a.267.267 0 0 1 .02-.022z"/>
                </svg>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* 成就数据 */}
      <div className="achievements-section">
        <div className="achievements-grid">
          {achievements.map((achievement, index) => (
            <div key={index} className="achievement-item">
              <span className="achievement-icon">{achievement.icon}</span>
              <span className="achievement-text">{achievement.text}</span>
            </div>
          ))}
        </div>
      </div>

      {/* 媒体报道 */}
      <div className="media-section">
        <h3 className="section-title">
          <span className="title-icon">📰</span>
          媒体报道
        </h3>
        <div className="media-logos">
          <div className="media-logo">TechCrunch</div>
          <div className="media-logo">Forbes</div>
          <div className="media-logo">WIRED</div>
          <div className="media-logo">The Verge</div>
        </div>
      </div>

      {/* 安全保障 */}
      <div className="security-section">
        <div className="security-features">
          <div className="security-feature">
            <span className="feature-icon">🔒</span>
            <span className="feature-text">端到端加密</span>
          </div>
          <div className="security-feature">
            <span className="feature-icon">🔄</span>
            <span className="feature-text">定期安全审计</span>
          </div>
          <div className="security-feature">
            <span className="feature-icon">👥</span>
            <span className="feature-text">专业心理咨询师</span>
          </div>
          <div className="security-feature">
            <span className="feature-icon">24/7</span>
            <span className="feature-text">全天候支持</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default BrandBadges;