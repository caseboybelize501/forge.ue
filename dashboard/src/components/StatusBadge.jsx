/**
 * StatusBadge Component
 * 
 * Status indicator badge.
 */
import React from 'react';

function StatusBadge({ status, label }) {
  const statusClass = `status-badge status-${status}`;
  
  return (
    <span className={statusClass}>
      {label || status}
    </span>
  );
}

export default StatusBadge;
