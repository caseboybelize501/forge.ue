/**
 * ProjectBrief Page
 * 
 * Submit game brief and create new project.
 */
import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import { useNavigate } from 'react-router-dom';
import apiClient from '../api/client';
import { endpoints } from '../api/endpoints';

function ProjectBrief() {
  const { register, handleSubmit, formState: { errors } } = useForm();
  const navigate = useNavigate();
  const [submitting, setSubmitting] = useState(false);

  const onSubmit = async (data) => {
    try {
      setSubmitting(true);
      const response = await apiClient.post(endpoints.createProject, {
        brief: data.brief,
      });
      const projectId = response.data.project_id;
      navigate(`/generation/${projectId}`);
    } catch (error) {
      console.error('Failed to create project:', error);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="page project-brief">
      <h1>Create New Project</h1>
      <form onSubmit={handleSubmit(onSubmit)} className="brief-form">
        <div className="form-group">
          <label className="form-label" htmlFor="brief">
            Game Brief
          </label>
          <textarea
            id="brief"
            className="form-input form-textarea"
            rows={10}
            placeholder="Describe your game: genre, mechanics, target platforms, art style..."
            {...register('brief', { required: 'Game brief is required' })}
          />
          {errors.brief && (
            <span className="form-error">{errors.brief.message}</span>
          )}
        </div>
        <button 
          type="submit" 
          className="btn btn-primary"
          disabled={submitting}
        >
          {submitting ? 'Creating...' : 'Create Project'}
        </button>
      </form>
    </div>
  );
}

export default ProjectBrief;
