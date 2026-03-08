/**
 * ConsoleOutput Component
 * 
 * Console output display for build logs.
 */
import React, { useEffect, useRef } from 'react';

function ConsoleOutput({ logs, autoScroll = true }) {
  const endRef = useRef(null);

  useEffect(() => {
    if (autoScroll && endRef.current) {
      endRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [logs, autoScroll]);

  return (
    <div className="console-output">
      <div className="console-content">
        {logs.map((log, index) => (
          <div 
            key={index} 
            className={`console-line console-${log.level || 'info'}`}
          >
            <span className="console-timestamp">{log.timestamp}</span>
            <span className="console-message">{log.message}</span>
          </div>
        ))}
        <div ref={endRef} />
      </div>
    </div>
  );
}

export default ConsoleOutput;
