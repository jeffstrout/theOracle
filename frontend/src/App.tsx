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

  const handleFormSubmit = async (birthData: BirthData) => {
    setLoading(true);
    setError(null);

    try {
      const result = await personalityApi.getFullAssessment(birthData);
      setAssessment(result);
    } catch (err) {
      setError('Failed to generate assessment. Please check your birth data and try again.');
      console.error('Assessment error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setAssessment(null);
    setError(null);
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
                <li><strong>Myers-Briggs (MBTI)</strong> - Your 4-letter personality type</li>
                <li><strong>Big Five (OCEAN)</strong> - Core personality dimensions</li>
                <li><strong>Enneagram</strong> - Your core motivation and fears</li>
                <li><strong>DISC Assessment</strong> - Behavioral communication style</li>
                <li><strong>StrengthsFinder</strong> - Your top 5 natural talents</li>
                <li><strong>Love Languages</strong> - How you give and receive love</li>
                <li><strong>Attachment Style</strong> - Your relationship patterns</li>
                <li><strong>Emotional Intelligence</strong> - EQ breakdown and insights</li>
                <li><strong>Career Personality</strong> - Holland Code career matching</li>
              </ul>
            </div>
          </div>
        ) : (
          <div className="results-container">
            <AssessmentResults assessment={assessment} />
            <div className="reset-container">
              <button onClick={handleReset} className="reset-button">
                Generate New Assessment
              </button>
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
