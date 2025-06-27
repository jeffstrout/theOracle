export interface MBTIResult {
  type: string;
  description: string;
  strengths: string[];
  weaknesses: string[];
  careers: string[];
}

export interface BigFiveResult {
  openness: number;
  conscientiousness: number;
  extraversion: number;
  agreeableness: number;
  neuroticism: number;
  description: string;
}

export interface EnneagramResult {
  type: number;
  wing?: number;
  description: string;
  core_motivation: string;
  basic_fear: string;
  strengths: string[];
}

export interface DISCResult {
  dominance: number;
  influence: number;
  steadiness: number;
  conscientiousness: number;
  primary_style: string;
  description: string;
}

export interface StrengthsFinderResult {
  top_strengths: string[];
  descriptions: Record<string, string>;
}

export interface LoveLanguagesResult {
  primary: string;
  secondary: string;
  scores: Record<string, number>;
}

export interface AttachmentStyleResult {
  style: string;
  percentage: number;
  description: string;
  characteristics: string[];
}

export interface EmotionalIntelligenceResult {
  overall_eq: number;
  self_awareness: number;
  self_regulation: number;
  motivation: number;
  empathy: number;
  social_skills: number;
  description: string;
}

export interface CareerPersonalityResult {
  holland_code: string;
  primary_type: string;
  career_matches: string[];
  work_environments: string[];
}

export interface PersonalityAssessment {
  user_id: string;
  birth_data: Record<string, any>;
  mbti?: MBTIResult;
  big_five?: BigFiveResult;
  enneagram?: EnneagramResult;
  disc?: DISCResult;
  strengths_finder?: StrengthsFinderResult;
  love_languages?: LoveLanguagesResult;
  attachment_styles?: AttachmentStyleResult;
  emotional_intelligence?: EmotionalIntelligenceResult;
  career_personality?: CareerPersonalityResult;
  created_at: string;
  confidence_score: number;
}

export type PersonalityTestType = 
  | 'mbti'
  | 'big_five'
  | 'enneagram'
  | 'disc'
  | 'strengths_finder'
  | 'love_languages'
  | 'attachment_styles'
  | 'emotional_intelligence'
  | 'career_personality';