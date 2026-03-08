/**
 * ProgressBar Component
 * 
 * Progress indicator for generation pipeline.
 */
import React from 'react';

function ProgressBar({ current, total, label }) {
  const percentage = total > 0 ? (current / total) * 100 : 0;
  
  return (
    <div className="progress-bar">
      {label && <div className="progress-label">{label}</div>}
      <div className="progress-track">
        <div 
          className="progress-fill" 
          style={{ width: `${percentage}%` }}
        />
      </div>
      <div className="progress-text">
        {current} / {total} ({percentage.toFixed(0)}%)
      </div>
    </div>
  );
}

export default ProgressBar;
