/**
 * Sidebar Component
 * 
 * Navigation sidebar for FORGE dashboard.
 */
import React from 'react';
import { NavLink } from 'react-router-dom';

function Sidebar() {
  return (
    <aside className="sidebar">
      <nav className="sidebar-nav">
        <NavLink to="/" className="nav-item">
          New Project
        </NavLink>
        <NavLink to="/learning-store" className="nav-item">
          Learning Store
        </NavLink>
      </nav>
    </aside>
  );
}

export default Sidebar;
