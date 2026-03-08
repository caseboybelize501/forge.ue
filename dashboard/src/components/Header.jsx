/**
 * Header Component
 * 
 * Navigation header for FORGE dashboard.
 */
import React from 'react';
import { Link } from 'react-router-dom';

function Header() {
  return (
    <header className="header">
      <div className="header-content">
        <Link to="/" className="logo">
          FORGE
        </Link>
        <nav className="nav">
          <Link to="/">New Project</Link>
          <Link to="/learning-store">Learning Store</Link>
        </nav>
      </div>
    </header>
  );
}

export default Header;
