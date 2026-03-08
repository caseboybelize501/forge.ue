/**
 * LearningStore Page
 * 
 * Display pattern library browser.
 */
import React, { useState, useEffect } from 'react';
import apiClient from '../api/client';

function LearningStore() {
  const [patterns, setPatterns] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedGenre, setSelectedGenre] = useState('all');

  useEffect(() => {
    const fetchPatterns = async () => {
      try {
        const response = await apiClient.get('/api/learning-store/patterns');
        setPatterns(response.data.patterns || []);
      } catch (error) {
        console.error('Failed to fetch patterns:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchPatterns();
  }, []);

  const filteredPatterns = selectedGenre === 'all' 
    ? patterns 
    : patterns.filter(p => p.genre === selectedGenre);

  const genres = ['all', ...new Set(patterns.map(p => p.genre))];

  if (loading) return <div>Loading...</div>;

  return (
    <div className="page learning-store">
      <h1>Learning Store</h1>
      <div className="genre-filter">
        {genres.map((genre) => (
          <button
            key={genre}
            className={`btn ${selectedGenre === genre ? 'btn-primary' : ''}`}
            onClick={() => setSelectedGenre(genre)}
          >
            {genre}
          </button>
        ))}
      </div>
      <div className="patterns-grid">
        {filteredPatterns.map((pattern) => (
          <div key={pattern.pattern_id} className="card pattern-card">
            <h3>{pattern.system_type}</h3>
            <p>Genre: {pattern.genre}</p>
            <p>Success Rate: {(pattern.success_rate * 100).toFixed(1)}%</p>
            <p>Avg Repair Cycles: {pattern.avg_repair_cycles}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default LearningStore;
