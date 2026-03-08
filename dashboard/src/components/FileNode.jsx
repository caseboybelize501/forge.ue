/**
 * FileNode Component
 * 
 * Tree node for file browser.
 */
import React, { useState } from 'react';

function FileNode({ file, depth = 0 }) {
  const [expanded, setExpanded] = useState(false);
  const hasChildren = file.children && file.children.length > 0;

  const handleClick = () => {
    if (hasChildren) {
      setExpanded(!expanded);
    }
  };

  return (
    <div className="file-node" style={{ paddingLeft: `${depth * 16}px` }}>
      <div 
        className="file-node-content" 
        onClick={handleClick}
      >
        <span className="file-icon">
          {hasChildren ? (expanded ? '📂' : '📁') : '📄'}
        </span>
        <span className="file-name">{file.name}</span>
        {file.size && <span className="file-size">{file.size} bytes</span>}
      </div>
      {expanded && hasChildren && (
        <div className="file-node-children">
          {file.children.map((child) => (
            <FileNode key={child.path} file={child} depth={depth + 1} />
          ))}
        </div>
      )}
    </div>
  );
}

export default FileNode;
