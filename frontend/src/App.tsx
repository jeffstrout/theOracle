import React, { useState } from 'react';
import './App.css';
import BirthDataForm from './components/BirthDataForm';
import AssessmentResults from './components/AssessmentResults';
import { BirthData } from './types/astro';
import { PersonalityAssessment } from './types/personality';
import { personalityApi } from './services/api';

function App() {
  const [assessment, setAssessment] = useState<PersonalityAssessment | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [astroData, setAstroData] = useState<any>(null);
  const [showDialog, setShowDialog] = useState(false);

  const handleFormSubmit = async (birthData: BirthData) => {
    setLoading(true);
    setError(null);

    try {
      // Instead of getting full assessment, just fetch astrological data
      const result = await personalityApi.getFullAssessment(birthData);
      
      // For now, display the raw data in a dialog
      setAstroData(result);
      setShowDialog(true);
      
      // Still set assessment for the existing flow
      setAssessment(result);
    } catch (err) {
      setError('Failed to fetch astrological data. Please check your birth data and try again.');
      console.error('Astro data error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setAssessment(null);
    setError(null);
    setAstroData(null);
    setShowDialog(false);
  };

  const closeDialog = () => {
    setShowDialog(false);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>🔮 The Oracle</h1>
        <p>Personality Evaluation Through Astrological Insight</p>
      </header>

      <main className="App-main">
        {error && (
          <div className="error-message">
            <p>{error}</p>
            <button onClick={() => setError(null)}>Dismiss</button>
          </div>
        )}

        {!assessment ? (
          <div className="form-container">
            <BirthDataForm onSubmit={handleFormSubmit} loading={loading} />
            
            <div className="app-info">
              <h3>What You'll Receive:</h3>
              <ul>
                <li><strong>Birth Chart Data</strong> - Complete astrological profile</li>
                <li><strong>Planetary Positions</strong> - Sun, Moon, Rising and all planets</li>
                <li><strong>House Placements</strong> - 12 houses and their meanings</li>
                <li><strong>Astrological Aspects</strong> - Planetary relationships</li>
                <li><strong>Raw API Response</strong> - Full data for LLM processing</li>
              </ul>
              <p><em>Future: This data will be processed by an LLM to generate 9 personality assessments including MBTI, Big Five, Enneagram, and more.</em></p>
            </div>
          </div>
        ) : (
          <div className="results-container">
            <AssessmentResults assessment={assessment} />
            <div className="reset-container">
              <button onClick={handleReset} className="reset-button">
                Get New Astrological Data
              </button>
            </div>
          </div>
        )}

        {/* Astrological Data Dialog */}
        {showDialog && astroData && (
          <div className="dialog-overlay" onClick={closeDialog}>
            <div className="dialog-content" onClick={(e) => e.stopPropagation()}>
              <div className="dialog-header">
                <h3>🌟 Your Astrological Data</h3>
                <button className="close-button" onClick={closeDialog}>×</button>
              </div>
              <div className="dialog-body">
                <p><strong>Data Source:</strong> Multi-provider astrology APIs</p>
                <p><em>This raw data will be used by an LLM to generate your personality assessments.</em></p>
                
                <div className="astro-data-display">
                  <h4>Raw API Response:</h4>
                  <pre className="json-display">
                    {JSON.stringify(astroData, null, 2)}
                  </pre>
                </div>
              </div>
              <div className="dialog-footer">
                <button onClick={closeDialog} className="dialog-button">Close</button>
              </div>
            </div>
          </div>
        )}
      </main>

      <footer className="App-footer">
        <p>&copy; 2024 The Oracle - Powered by Astrological Insights</p>
      </footer>
    </div>
  );
}

export default App;
