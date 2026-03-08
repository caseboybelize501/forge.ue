/**
 * PlatformPackages Page
 * 
 * Display per-platform build status and download.
 */
import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import apiClient from '../api/client';
import { endpoints } from '../api/endpoints';
import StatusBadge from '../components/StatusBadge';
import DownloadButton from '../components/DownloadButton';

function PlatformPackages() {
  const { projectId } = useParams();
  const [packages, setPackages] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchPackages = async () => {
      try {
        // This would be a new endpoint to list packages
        const response = await apiClient.get(`${endpoints.triggerPackaging(projectId)}/status`);
        setPackages(response.data.packages || []);
      } catch (error) {
        console.error('Failed to fetch packages:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchPackages();
  }, [projectId]);

  if (loading) return <div>Loading...</div>;

  return (
    <div className="page platform-packages">
      <h1>Platform Packages</h1>
      <table className="packages-table">
        <thead>
          <tr>
            <th>Platform</th>
            <th>Status</th>
            <th>Size</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {packages.map((pkg) => (
            <tr key={pkg.platform}>
              <td>{pkg.platform}</td>
              <td>
                <StatusBadge 
                  status={pkg.success ? 'success' : 'error'}
                  label={pkg.status}
                />
              </td>
              <td>{pkg.size_bytes ? `${(pkg.size_bytes / 1024 / 1024).toFixed(1)} MB` : '-'}</td>
              <td>
                {pkg.success && (
                  <DownloadButton
                    url={endpoints.downloadPackage(projectId, pkg.platform)}
                    filename={`${projectId}-${pkg.platform}.zip`}
                  />
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default PlatformPackages;
