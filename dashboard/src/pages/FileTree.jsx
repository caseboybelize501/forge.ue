/**
 * FileTree Page
 * 
 * Display generated UE5 project file browser.
 */
import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import apiClient from '../api/client';
import { endpoints } from '../api/endpoints';
import FileNode from '../components/FileNode';

function FileTree() {
  const { projectId } = useParams();
  const [files, setFiles] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchFiles = async () => {
      try {
        const response = await apiClient.get(endpoints.getFileTree(projectId));
        setFiles(response.data.files);
      } catch (error) {
        console.error('Failed to fetch files:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchFiles();
  }, [projectId]);

  if (loading) return <div>Loading...</div>;

  return (
    <div className="page file-tree">
      <h1>Generated Files</h1>
      <div className="file-tree-container">
        {files.map((file) => (
          <FileNode key={file.path} file={file} />
        ))}
      </div>
    </div>
  );
}

export default FileTree;
