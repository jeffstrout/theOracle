import React from 'react';
import { PersonalityAssessment } from '../types/personality';

interface AssessmentResultsProps {
  assessment: PersonalityAssessment;
}

const AssessmentResults: React.FC<AssessmentResultsProps> = ({ assessment }) => {
  const formatPercentage = (value: number) => `${value}%`;

  return (
    <div className="assessment-results">
      <div className="results-header">
        <h1>Your Personality Profile</h1>
        <p>Based on your astrological birth chart</p>
        <div className="confidence-score">
          Confidence Score: {Math.round(assessment.confidence_score * 100)}%
        </div>
      </div>

      {/* MBTI Results */}
      {assessment.mbti && (
        <div className="assessment-section">
          <h2>Myers-Briggs Type Indicator (MBTI)</h2>
          <div className="result-card">
            <h3>Your Type: {assessment.mbti.type}</h3>
            <p>{assessment.mbti.description}</p>
            
            <div className="traits-grid">
              <div className="trait-category">
                <h4>Strengths</h4>
                <ul>
                  {assessment.mbti.strengths.map((strength, index) => (
                    <li key={index}>{strength}</li>
                  ))}
                </ul>
              </div>
              
              <div className="trait-category">
                <h4>Areas for Growth</h4>
                <ul>
                  {assessment.mbti.weaknesses.map((weakness, index) => (
                    <li key={index}>{weakness}</li>
                  ))}
                </ul>
              </div>
              
              <div className="trait-category">
                <h4>Ideal Careers</h4>
                <ul>
                  {assessment.mbti.careers.map((career, index) => (
                    <li key={index}>{career}</li>
                  ))}
                </ul>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Big Five Results */}
      {assessment.big_five && (
        <div className="assessment-section">
          <h2>Big Five Personality Traits (OCEAN)</h2>
          <div className="result-card">
            <p>{assessment.big_five.description}</p>
            
            <div className="big-five-scores">
              <div className="trait-score">
                <label>Openness to Experience</label>
                <div className="score-bar">
                  <div 
                    className="score-fill" 
                    style={{width: `${assessment.big_five.openness}%`}}
                  ></div>
                  <span>{assessment.big_five.openness}%</span>
                </div>
              </div>
              
              <div className="trait-score">
                <label>Conscientiousness</label>
                <div className="score-bar">
                  <div 
                    className="score-fill" 
                    style={{width: `${assessment.big_five.conscientiousness}%`}}
                  ></div>
                  <span>{assessment.big_five.conscientiousness}%</span>
                </div>
              </div>
              
              <div className="trait-score">
                <label>Extraversion</label>
                <div className="score-bar">
                  <div 
                    className="score-fill" 
                    style={{width: `${assessment.big_five.extraversion}%`}}
                  ></div>
                  <span>{assessment.big_five.extraversion}%</span>
                </div>
              </div>
              
              <div className="trait-score">
                <label>Agreeableness</label>
                <div className="score-bar">
                  <div 
                    className="score-fill" 
                    style={{width: `${assessment.big_five.agreeableness}%`}}
                  ></div>
                  <span>{assessment.big_five.agreeableness}%</span>
                </div>
              </div>
              
              <div className="trait-score">
                <label>Neuroticism</label>
                <div className="score-bar">
                  <div 
                    className="score-fill" 
                    style={{width: `${assessment.big_five.neuroticism}%`}}
                  ></div>
                  <span>{assessment.big_five.neuroticism}%</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Enneagram Results */}
      {assessment.enneagram && (
        <div className="assessment-section">
          <h2>Enneagram</h2>
          <div className="result-card">
            <h3>Type {assessment.enneagram.type}{assessment.enneagram.wing && `w${assessment.enneagram.wing}`}</h3>
            <p>{assessment.enneagram.description}</p>
            
            <div className="enneagram-details">
              <div className="detail-item">
                <strong>Core Motivation:</strong> {assessment.enneagram.core_motivation}
              </div>
              <div className="detail-item">
                <strong>Basic Fear:</strong> {assessment.enneagram.basic_fear}
              </div>
              <div className="detail-item">
                <strong>Key Strengths:</strong>
                <ul>
                  {assessment.enneagram.strengths.map((strength, index) => (
                    <li key={index}>{strength}</li>
                  ))}
                </ul>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* DISC Results */}
      {assessment.disc && (
        <div className="assessment-section">
          <h2>DISC Assessment</h2>
          <div className="result-card">
            <h3>Primary Style: {assessment.disc.primary_style}</h3>
            <p>{assessment.disc.description}</p>
            
            <div className="disc-scores">
              <div className="disc-score">
                <label>Dominance</label>
                <div className="score-circle">
                  <span>{assessment.disc.dominance}%</span>
                </div>
              </div>
              <div className="disc-score">
                <label>Influence</label>
                <div className="score-circle">
                  <span>{assessment.disc.influence}%</span>
                </div>
              </div>
              <div className="disc-score">
                <label>Steadiness</label>
                <div className="score-circle">
                  <span>{assessment.disc.steadiness}%</span>
                </div>
              </div>
              <div className="disc-score">
                <label>Conscientiousness</label>
                <div className="score-circle">
                  <span>{assessment.disc.conscientiousness}%</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* StrengthsFinder Results */}
      {assessment.strengths_finder && (
        <div className="assessment-section">
          <h2>StrengthsFinder - Top 5 Strengths</h2>
          <div className="result-card">
            <div className="strengths-list">
              {assessment.strengths_finder.top_strengths.map((strength, index) => (
                <div key={index} className="strength-item">
                  <h4>#{index + 1} {strength}</h4>
                  <p>{assessment.strengths_finder.descriptions[strength]}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Love Languages Results */}
      {assessment.love_languages && (
        <div className="assessment-section">
          <h2>Love Languages</h2>
          <div className="result-card">
            <div className="love-languages-summary">
              <h3>Primary: {assessment.love_languages.primary}</h3>
              <h4>Secondary: {assessment.love_languages.secondary}</h4>
            </div>
            
            <div className="love-languages-scores">
              {Object.entries(assessment.love_languages.scores).map(([language, score]) => (
                <div key={language} className="language-score">
                  <label>{language}</label>
                  <div className="score-bar">
                    <div 
                      className="score-fill" 
                      style={{width: `${(score / 50) * 100}%`}}
                    ></div>
                    <span>{score}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Attachment Styles Results */}
      {assessment.attachment_styles && (
        <div className="assessment-section">
          <h2>Attachment Style</h2>
          <div className="result-card">
            <h3>{assessment.attachment_styles.style} ({assessment.attachment_styles.percentage}%)</h3>
            <p>{assessment.attachment_styles.description}</p>
            
            <div className="attachment-characteristics">
              <h4>Key Characteristics:</h4>
              <ul>
                {assessment.attachment_styles.characteristics.map((char, index) => (
                  <li key={index}>{char}</li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      )}

      {/* Emotional Intelligence Results */}
      {assessment.emotional_intelligence && (
        <div className="assessment-section">
          <h2>Emotional Intelligence (EQ)</h2>
          <div className="result-card">
            <div className="eq-overview">
              <h3>Overall EQ Score: {assessment.emotional_intelligence.overall_eq}</h3>
              <p>{assessment.emotional_intelligence.description}</p>
            </div>
            
            <div className="eq-breakdown">
              <div className="eq-component">
                <label>Self-Awareness</label>
                <span>{assessment.emotional_intelligence.self_awareness}%</span>
              </div>
              <div className="eq-component">
                <label>Self-Regulation</label>
                <span>{assessment.emotional_intelligence.self_regulation}%</span>
              </div>
              <div className="eq-component">
                <label>Motivation</label>
                <span>{assessment.emotional_intelligence.motivation}%</span>
              </div>
              <div className="eq-component">
                <label>Empathy</label>
                <span>{assessment.emotional_intelligence.empathy}%</span>
              </div>
              <div className="eq-component">
                <label>Social Skills</label>
                <span>{assessment.emotional_intelligence.social_skills}%</span>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Career Personality Results */}
      {assessment.career_personality && (
        <div className="assessment-section">
          <h2>Career Personality (Holland Code)</h2>
          <div className="result-card">
            <h3>Your Code: {assessment.career_personality.holland_code}</h3>
            <h4>Primary Type: {assessment.career_personality.primary_type}</h4>
            
            <div className="career-details">
              <div className="career-section">
                <h4>Recommended Careers:</h4>
                <ul>
                  {assessment.career_personality.career_matches.map((career, index) => (
                    <li key={index}>{career}</li>
                  ))}
                </ul>
              </div>
              
              <div className="career-section">
                <h4>Ideal Work Environments:</h4>
                <ul>
                  {assessment.career_personality.work_environments.map((env, index) => (
                    <li key={index}>{env}</li>
                  ))}
                </ul>
              </div>
            </div>
          </div>
        </div>
      )}

      <div className="results-footer">
        <p>Generated on {new Date(assessment.created_at).toLocaleDateString()}</p>
        <p>Based on astrological analysis of your birth chart</p>
      </div>
    </div>
  );
};

export default AssessmentResults;