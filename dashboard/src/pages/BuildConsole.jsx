/**
 * BuildConsole Page
 * 
 * Display live UBT output and error highlighting.
 */
import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import apiClient from '../api/client';
import { endpoints } from '../api/endpoints';
import ConsoleOutput from '../components/ConsoleOutput';
import StatusBadge from '../components/StatusBadge';

function BuildConsole() {
  const { projectId } = useParams();
  const [buildStatus, setBuildStatus] = useState(null);
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchBuild = async () => {
      try {
        const response = await apiClient.get(endpoints.getBuildStatus(projectId));
        setBuildStatus(response.data);
        
        // Convert errors to log entries
        const newLogs = (response.data.errors || []).map((error) => ({
          level: 'error',
          message: error.error_message,
          timestamp: new Date().toISOString(),
        }));
        setLogs(newLogs);
      } catch (error) {
        console.error('Failed to fetch build status:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchBuild();
    const interval = setInterval(fetchBuild, 2000);
    return () => clearInterval(interval);
  }, [projectId]);

  if (loading) return <div>Loading...</div>;

  return (
    <div className="page build-console">
      <h1>Build Console</h1>
      <div className="build-status">
        <StatusBadge 
          status={buildStatus.success ? 'success' : 'error'} 
          label={buildStatus.success ? 'Build Successful' : 'Build Failed'}
        />
        {buildStatus.duration_seconds && (
          <span>Duration: {buildStatus.duration_seconds.toFixed(1)}s</span>
        )}
      </div>
      <ConsoleOutput logs={logs} />
    </div>
  );
}

export default BuildConsole;
