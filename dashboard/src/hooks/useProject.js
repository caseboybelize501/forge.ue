/**
 * useProject Hook
 * 
 * React hook for project data fetching.
 */
import { useState, useEffect } from 'react';
import apiClient from '../api/client';
import { endpoints } from '../api/endpoints';

export function useProject(projectId) {
  const [project, setProject] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!projectId) return;

    const fetchProject = async () => {
      try {
        setLoading(true);
        const response = await apiClient.get(endpoints.getProject(projectId));
        setProject(response.data);
        setError(null);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchProject();
  }, [projectId]);

  return { project, loading, error };
}

export default useProject;
