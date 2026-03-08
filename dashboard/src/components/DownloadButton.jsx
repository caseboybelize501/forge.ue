/**
 * DownloadButton Component
 * 
 * Download action button.
 */
import React from 'react';

function DownloadButton({ url, filename, label = 'Download', disabled = false }) {
  const handleClick = async () => {
    try {
      const response = await fetch(url);
      const blob = await response.blob();
      const downloadUrl = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = downloadUrl;
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(downloadUrl);
      a.remove();
    } catch (error) {
      console.error('Download failed:', error);
    }
  };

  return (
    <button 
      className="btn btn-download"
      onClick={handleClick}
      disabled={disabled}
    >
      {label}
    </button>
  );
}

export default DownloadButton;
