import React from 'react';

const ProgressBar = ({ progress, animated = true }) => {
  return (
    <div className="progress-bar-container">
      <div 
        className={`progress-bar ${animated ? 'animated' : ''}`}
        style={{ width: `${progress}%` }}
      >
        <div className="progress-glow"></div>
      </div>
      <div className="progress-label">{Math.round(progress)}%</div>
    </div>
  );
};

const LoadingSpinner = ({ size = 'medium', text = '加载中...' }) => {
  return (
    <div className={`loading-spinner-wrapper ${size}`}>
      <div className="spinner">
        <div className="spinner-circle"></div>
        <div className="spinner-circle"></div>
        <div className="spinner-circle"></div>
      </div>
      {text && <div className="spinner-text">{text}</div>}
    </div>
  );
};

const StepIndicator = ({ currentStep, steps }) => {
  return (
    <div className="step-indicator">
      {steps.map((step, index) => (
        <div key={index} className={`step ${index <= currentStep ? 'active' : ''}`}>
          <div className="step-number">
            {index < currentStep ? (
              <svg className="check-icon" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
              </svg>
            ) : (
              index + 1
            )}
          </div>
          <div className="step-label">{step}</div>
          {index < steps.length - 1 && <div className="step-connector"></div>}
        </div>
      ))}
    </div>
  );
};

const SkeletonLoader = ({ type = 'input', lines = 1 }) => {
  if (type === 'input') {
    return (
      <div className="skeleton-input">
        <div className="skeleton-label"></div>
        <div className="skeleton-field"></div>
      </div>
    );
  }
  
  if (type === 'button') {
    return <div className="skeleton-button"></div>;
  }
  
  if (type === 'text') {
    return (
      <>
        {Array.from({ length: lines }).map((_, index) => (
          <div key={index} className="skeleton-text" style={{ width: `${80 - index * 10}%` }}></div>
        ))}
      </>
    );
  }
  
  return null;
};

export { ProgressBar, LoadingSpinner, StepIndicator, SkeletonLoader };