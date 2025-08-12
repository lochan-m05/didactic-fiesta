import React, { useState } from 'react';
import './App.css';

function App() {
  const [hashtags, setHashtags] = useState('');
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(false);

  const searchJobs = async () => {
    if (!hashtags.trim()) return;
    
    setLoading(true);
    try {
      const response = await fetch('/api/jobs/search/hashtags', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          hashtags: hashtags.split(',').map(tag => tag.trim())
        })
      });
      
      const data = await response.json();
      setJobs(data.data?.jobs || []);
    } catch (error) {
      console.error('Search failed:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Job Discovery Platform</h1>
        <div className="search-container">
          <input
            type="text"
            placeholder="Enter hashtags (e.g., bca, fresher, python)"
            value={hashtags}
            onChange={(e) => setHashtags(e.target.value)}
            className="search-input"
          />
          <button 
            onClick={searchJobs} 
            disabled={loading}
            className="search-button"
          >
            {loading ? 'Searching...' : 'Search Jobs'}
          </button>
        </div>
        
        {jobs.length > 0 && (
          <div className="results">
            <h2>Found {jobs.length} jobs</h2>
            {jobs.map((job, index) => (
              <div key={index} className="job-card">
                <h3>{job.title}</h3>
                <p><strong>Company:</strong> {job.company?.name}</p>
                <p><strong>Location:</strong> {job.location}</p>
                <p><strong>Source:</strong> {job.source}</p>
              </div>
            ))}
          </div>
        )}
        
        {loading && (
          <div className="loading">
            <p>Searching for jobs...</p>
          </div>
        )}
      </header>
    </div>
  );
}

export default App;
