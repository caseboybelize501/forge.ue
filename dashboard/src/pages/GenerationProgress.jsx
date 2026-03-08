/**
 * GenerationProgress Page
 * 
 * Display topological level progress and critic status.
 */
import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import apiClient from '../api/client';
import { endpoints } from '../api/endpoints';
import ProgressBar from '../components/ProgressBar';
import StatusBadge from '../components/StatusBadge';

function GenerationProgress() {
  const { projectId } = useParams();
  const [progress, setProgress] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchProgress = async () => {
      try {
        const response = await apiClient.get(endpoints.getProgress(projectId));
        setProgress(response.data);
      } catch (error) {
        console.error('Failed to fetch progress:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchProgress();
    const interval = setInterval(fetchProgress, 3000);
    return () => clearInterval(interval);
  }, [projectId]);

  if (loading) return <div>Loading...</div>;

  return (
    <div className="page generation-progress">
      <h1>Generation Progress</h1>
      <ProgressBar 
        current={progress.current_level} 
        total={progress.total_levels}
        label="Pipeline Progress"
      />
      <div className="critic-status">
        <h2>Critic Gate Status</h2>
        <StatusBadge status={progress.critic_status} />
      </div>
      <div className="files-generated">
        <p>Files Generated: {progress.files_generated}</p>
      </div>
    </div>
  );
}

export default GenerationProgress;
