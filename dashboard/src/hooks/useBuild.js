/**
 * useBuild Hook
 * 
 * React hook for build status polling.
 */
import { useState, useEffect } from 'react';
import apiClient from '../api/client';
import { endpoints } from '../api/endpoints';

export function useBuild(projectId, pollInterval = 5000) {
  const [buildStatus, setBuildStatus] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!projectId) return;

    const fetchBuild = async () => {
      try {
        const response = await apiClient.get(endpoints.getBuildStatus(projectId));
        setBuildStatus(response.data);
        setError(null);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchBuild();

    const interval = setInterval(fetchBuild, pollInterval);
    return () => clearInterval(interval);
  }, [projectId, pollInterval]);

  return { buildStatus, loading, error };
}

export default useBuild;
