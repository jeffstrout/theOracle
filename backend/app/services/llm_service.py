import json
import asyncio
from typing import Dict, List, Optional
from openai import OpenAI
from app.core.config import settings
from app.schemas.astro import BirthChart
from app.schemas.personality import *

class LLMService:
    """
    Service for generating personality assessments using Large Language Models
    """
    
    def __init__(self):
        self.client = None
        if settings.OPENAI_API_KEY and settings.OPENAI_API_KEY != "YOUR_OPENAI_API_KEY_HERE":
            try:
                self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
            except Exception as e:
                print(f"Error initializing OpenAI client: {e}")
                self.client = None
        self.model = "gpt-4" if settings.LLM_MODEL == "gpt-4o-mini" else settings.LLM_MODEL  # Upgrade to GPT-4 for better analysis
        
    def generate_personality_assessment(self, birth_chart: BirthChart) -> PersonalityAssessment:
        """
        Generate complete personality assessment using LLM analysis of birth chart
        """
        if not self.client or not settings.USE_LLM:
            print("LLM not configured, falling back to rule-based system")
            return None
        
        print(f"Generating LLM-powered personality assessment using {self.model}")
        
        # Prepare birth chart data for LLM
        chart_data = self._format_birth_chart_for_llm(birth_chart)
        
        # Generate all assessments sequentially
        try:
            mbti = self._generate_mbti_llm(chart_data)
            big_five = self._generate_big_five_llm(chart_data)
            enneagram = self._generate_enneagram_llm(chart_data)
            disc = self._generate_disc_llm(chart_data)
            strengths = self._generate_strengths_finder_llm(chart_data)
            love_lang = self._generate_love_languages_llm(chart_data)
            attachment = self._generate_attachment_styles_llm(chart_data)
            eq = self._generate_emotional_intelligence_llm(chart_data)
            career = self._generate_career_personality_llm(chart_data)
            
            results = [mbti, big_five, enneagram, disc, strengths, love_lang, attachment, eq, career]
            
            # If any assessment failed, return None to fall back to rule-based
            if any(result is None for result in results):
                print("Some LLM assessments failed, falling back to rule-based system")
                return None
            
            return PersonalityAssessment(
                user_id="llm_generated_user",
                birth_data=birth_chart.dict(),
                mbti=mbti,
                big_five=big_five,
                enneagram=enneagram,
                disc=disc,
                strengths_finder=strengths,
                love_languages=love_lang,
                attachment_styles=attachment,
                emotional_intelligence=eq,
                career_personality=career,
                created_at="2024-01-01T00:00:00Z",
                confidence_score=0.95  # Higher confidence for sophisticated LLM analysis
            )
            
        except Exception as e:
            print(f"Error generating LLM assessment: {e}")
            return None
    
    def _format_birth_chart_for_llm(self, birth_chart: BirthChart) -> str:
        """
        Format birth chart data into a comprehensive string for deep LLM analysis
        """
        chart_summary = f"""
=== COMPREHENSIVE BIRTH CHART ANALYSIS ===

🌟 CORE IDENTITY TRINITY:
• Sun Sign: {birth_chart.sun_sign} (Core Self, Life Purpose, Ego Expression)
• Moon Sign: {birth_chart.moon_sign} (Emotional Nature, Subconscious, Inner Needs)
• Rising Sign: {birth_chart.rising_sign} (Outer Personality, First Impressions, Life Approach)

🪐 DETAILED PLANETARY POSITIONS:
"""
        
        # Enhanced planetary descriptions with psychological significance
        planet_meanings = {
            "Sun": "Core identity, life force, father archetype, creativity",
            "Moon": "Emotional responses, mother archetype, instincts, past patterns", 
            "Mercury": "Communication style, thinking patterns, learning approach",
            "Venus": "Love style, values, aesthetic preferences, relationship approach",
            "Mars": "Drive, action style, anger expression, sexual energy",
            "Jupiter": "Growth, expansion, beliefs, optimism, fortune",
            "Saturn": "Structure, discipline, lessons, authority, limitations",
            "Uranus": "Innovation, rebellion, uniqueness, sudden changes",
            "Neptune": "Dreams, spirituality, illusions, compassion, creativity",
            "Pluto": "Transformation, power, depth, regeneration, obsessions"
        }
        
        for planet in birth_chart.planets:
            meaning = planet_meanings.get(planet.name, "Personal expression")
            chart_summary += f"• {planet.name}: {planet.sign} {planet.degree:.1f}° in {planet.house}th house"
            if planet.retrograde:
                chart_summary += " (RETROGRADE - internalized energy)"
            chart_summary += f" → {meaning}\n"
        
        # Enhanced house meanings
        house_themes = {
            "1": "Self-Image & Identity", "2": "Values & Resources", "3": "Communication & Learning",
            "4": "Home & Roots", "5": "Creativity & Romance", "6": "Work & Health",
            "7": "Partnerships & Others", "8": "Transformation & Shared Resources", "9": "Philosophy & Higher Learning",
            "10": "Career & Public Image", "11": "Friends & Aspirations", "12": "Spirituality & Subconscious"
        }
        
        chart_summary += f"\n🏠 LIFE SECTORS (Houses):\n"
        for house, sign in birth_chart.houses.items():
            theme = house_themes.get(house, "Life sector")
            chart_summary += f"• {house}th House ({theme}): {sign} energy\n"
        
        if birth_chart.aspects:
            chart_summary += f"\n⚡ PLANETARY RELATIONSHIPS (Aspects):\n"
            for aspect in birth_chart.aspects[:8]:  # More aspects for deeper analysis
                planet1 = aspect.get('planet1', '')
                planet2 = aspect.get('planet2', '')
                aspect_type = aspect.get('aspect', '')
                orb = aspect.get('orb', 'N/A')
                
                # Add aspect interpretation hints
                aspect_nature = {
                    'Conjunction': 'FUSION - energies blend together',
                    'Trine': 'HARMONY - natural flow and ease', 
                    'Square': 'TENSION - dynamic challenge requiring growth',
                    'Opposition': 'POLARITY - need for balance and integration',
                    'Sextile': 'OPPORTUNITY - potential for positive development'
                }.get(aspect_type, 'INTERACTION')
                
                chart_summary += f"• {planet1} {aspect_type} {planet2} (orb: {orb}) → {aspect_nature}\n"
        
        chart_summary += f"\n🔮 SYNTHESIS NOTES:\nThis chart shows the complex interplay between {birth_chart.sun_sign} solar identity, {birth_chart.moon_sign} emotional nature, and {birth_chart.rising_sign} external expression, creating a unique psychological fingerprint requiring deep integration of all elements."
        
        return chart_summary.strip()
    
    def _generate_mbti_llm(self, chart_data: str) -> MBTIResult:
        """Generate MBTI assessment using sophisticated LLM analysis"""
        
        prompt = f"""You are a master astrologer and depth psychologist with decades of experience integrating Jungian typology with astrological wisdom. 

Your task: Perform a comprehensive MBTI analysis of this birth chart using multi-layered psychological and astrological reasoning.

{chart_data}

🧠 DEEP ANALYSIS FRAMEWORK:

1. COGNITIVE FUNCTION ANALYSIS:
   First, analyze each MBTI dimension through multiple astrological lenses:

   EXTRAVERSION vs INTROVERSION:
   - Solar consciousness: Fire/Air signs lean extraverted, Earth/Water introverted
   - Lunar patterns: Emotional processing style (outward vs inward)
   - Rising sign: Social interface and energy direction
   - 1st vs 7th house emphasis: Self-focus vs other-focus
   - Planetary aspects: Social planet aspects indicate relational energy flow

   SENSING vs INTUITION:
   - Mercury placement: Information processing style
   - Earth sign emphasis: Concrete, practical focus (Sensing)
   - Air/Fire emphasis: Abstract, possibility focus (iNtuition)
   - 6th house vs 9th house themes: Detail vs big picture
   - Saturn vs Uranus influence: Structure vs innovation

   THINKING vs FEELING:
   - Venus vs Mars dominance: Harmony/values vs logic/action
   - Air signs vs Water signs: Objective analysis vs subjective values
   - 3rd/10th house vs 4th/11th house emphasis
   - Aspect patterns: Harmonious vs challenging aspects affecting decision-making

   JUDGING vs PERCEIVING:
   - Modality emphasis: Cardinal/Fixed (structure) vs Mutable (flexibility)
   - Saturn vs Jupiter influence: Control vs spontaneity
   - Angular vs Cadent house emphasis
   - Aspect integration: Tense aspects = more J, flowing aspects = more P

2. INTEGRATION SYNTHESIS:
   Consider how the planets work together as a psychological system. Look for:
   - Contradictions that create complexity
   - Dominant themes that override simple rules
   - Evolutionary tension points that drive growth
   - Shadow elements that influence type expression

3. CONFIDENCE ASSESSMENT:
   Rate your confidence in this typing based on:
   - Chart clarity and consistency
   - Strength of astrological indicators
   - Potential for type evolution or ambiguity

Provide your analysis in this exact JSON format:
{{
    "type": "[4-letter MBTI code]",
    "description": "[3-4 sentences explaining the primary astrological reasoning for this type, including specific planetary placements and their psychological significance]",
    "strengths": ["[5 specific strengths based on planetary placements]"],
    "weaknesses": ["[4 specific challenges or growth areas from the chart]"],
    "careers": ["[5 career paths that align with both MBTI type and astrological vocational indicators]"]
}}"""

        return self._call_openai_for_assessment(prompt, MBTIResult)
    
    def _generate_big_five_llm(self, chart_data: str) -> BigFiveResult:
        """Generate Big Five assessment using sophisticated psychological analysis"""
        
        prompt = f"""You are a renowned personality psychologist specializing in the intersection of astrology and the Five-Factor Model. Conduct a nuanced Big Five analysis.

{chart_data}

🔬 SYSTEMATIC BIG FIVE ANALYSIS:

For each dimension, analyze multiple astrological factors and provide a precise score (1-100):

1. OPENNESS TO EXPERIENCE (Intellect/Imagination):
   - Air sign emphasis (esp. Gemini/Aquarius): +20-30 points
   - 9th house planets: +15-25 points  
   - Uranus aspects: +10-20 points
   - Jupiter aspects: +5-15 points
   - Mercury in Air/Fire: +10-20 points
   - Strong Earth signs: -10-20 points
   - Saturn dominance: -5-15 points

2. CONSCIENTIOUSNESS (Organization/Discipline):
   - Virgo/Capricorn emphasis: +20-35 points
   - 6th/10th house planets: +15-25 points
   - Saturn strength: +15-30 points
   - Cardinal signs: +10-20 points
   - Mutable dominance: -10-25 points
   - Neptune/Pisces emphasis: -5-15 points

3. EXTRAVERSION (Social Energy/Assertiveness):
   - Fire sign dominance: +20-35 points
   - Air sign emphasis: +15-25 points
   - 1st/7th/11th house planets: +10-20 points
   - Sun/Mars strength: +10-25 points
   - Water sign dominance: -10-25 points
   - 12th house emphasis: -15-30 points

4. AGREEABLENESS (Cooperation/Compassion):
   - Water sign emphasis: +20-30 points
   - Venus strength: +15-25 points
   - 7th/11th house themes: +10-20 points
   - Challenging Mars aspects: -10-20 points
   - Fire sign dominance: -5-15 points
   - Aries/Scorpio emphasis: -10-25 points

5. NEUROTICISM (Emotional Stability - reverse scored):
   - Water sign dominance: +15-30 points
   - Challenging Moon aspects: +10-25 points
   - 8th/12th house emphasis: +10-20 points
   - Saturn challenges: +5-15 points
   - Fire sign strength: -10-25 points
   - Strong Earth grounding: -10-20 points

CONSIDER CHART INTEGRATION:
- How do contradictory influences balance out?
- Which themes are strongest and most consistent?
- What aspects create complexity or nuance?
- How might this person have evolved their traits?

Provide precise scores with detailed astrological reasoning:

{{
    "openness": [score 1-100],
    "conscientiousness": [score 1-100],
    "extraversion": [score 1-100],
    "agreeableness": [score 1-100],
    "neuroticism": [score 1-100],
    "description": "[Detailed 3-4 sentence analysis explaining the specific astrological factors that create this unique personality profile, including how contradictory elements integrate]"
}}"""

        return self._call_openai_for_assessment(prompt, BigFiveResult)
    
    def _generate_enneagram_llm(self, chart_data: str) -> EnneagramResult:
        """Generate Enneagram assessment using deep motivational analysis"""
        
        prompt = f"""You are a master Enneagram teacher and psychological astrologer specializing in core motivational patterns and unconscious drives.

{chart_data}

🔍 DEEP ENNEAGRAM ANALYSIS:

The Enneagram reveals the unconscious emotional patterns and core fears that drive behavior. Analyze this chart for:

🎯 CORE MOTIVATION ANALYSIS (by type):

Type 1 (Perfectionist): Virgo emphasis, strong Saturn, 6th house planets, need for order
Type 2 (Helper): Cancer/Venus dominance, 7th/11th house emphasis, others-focused planets
Type 3 (Achiever): Leo/Capricorn strength, 10th house planets, goal-oriented Mars
Type 4 (Individualist): Scorpio/Pisces emphasis, 8th/12th house themes, emotional depth
Type 5 (Investigator): Aquarius/Virgo, 11th/6th house, detached Mercury/Saturn
Type 6 (Loyalist): Cancer/Virgo, security-seeking Moon, loyalty themes, anxiety aspects
Type 7 (Enthusiast): Sagittarius/Gemini, Jupiter dominance, adventure-seeking, fear of limitation
Type 8 (Challenger): Aries/Scorpio emphasis, powerful Mars/Pluto, control needs
Type 9 (Peacemaker): Libra/Taurus emphasis, harmony-seeking Venus, avoidance patterns

💭 MOTIVATIONAL DEPTH ANALYSIS:
1. CORE FEAR PATTERNS:
   - What does this person most fear losing or encountering?
   - How do planetary challenges reveal unconscious anxieties?
   - What aspects create the deepest emotional triggers?

2. COMPULSIVE BEHAVIORS:
   - What patterns does this person repeat unconsciously?
   - How do planetary placements show automatic responses?
   - Where does the chart show rigid or addictive patterns?

3. WING ANALYSIS:
   - Which adjacent type adds flavor to the core type?
   - How do secondary planetary themes support the wing?

4. INTEGRATION/DISINTEGRATION:
   - How might this person grow (integration arrow)?
   - What stress patterns emerge (disintegration arrow)?
   - What planetary transits might trigger these movements?

🧠 PSYCHOLOGICAL SYNTHESIS:
Consider how the chart's deepest patterns create this person's worldview, defense mechanisms, and unconscious strategies for feeling safe and valued.

Provide your analysis:

{{
    "type": [1-9],
    "wing": [adjacent type that adds flavor],
    "description": "[4-5 sentences explaining the specific astrological indicators that reveal this core type, including planetary placements that show the unconscious patterns and defense mechanisms]",
    "core_motivation": "[The deepest drive - what this person is really seeking]",
    "basic_fear": "[The core fear this person is unconsciously avoiding]",
    "strengths": ["Four key strengths shown by planetary gifts and positive aspects"]
}}"""

        return self._call_openai_for_assessment(prompt, EnneagramResult)
    
    def _generate_disc_llm(self, chart_data: str) -> DISCResult:
        """Generate DISC assessment using LLM"""
        
        prompt = f"""You are an expert astrologer and psychologist. Based on the birth chart below, determine this person's DISC profile percentages.

{chart_data}

Analyze behavioral tendencies and score each DISC dimension (percentages must add to 100):

Guidelines:
- Dominance (D): Fire signs, Mars prominence, 1st/10th house emphasis
- Influence (I): Air signs, Venus/Mercury prominence, 3rd/11th house emphasis  
- Steadiness (S): Earth/Water signs, Moon/Venus prominence, 4th/6th house emphasis
- Conscientiousness (C): Earth signs, Saturn/Mercury prominence, 6th/10th house emphasis

Return ONLY a valid JSON object in this exact format:
{{
    "dominance": 35,
    "influence": 30,
    "steadiness": 20,
    "conscientiousness": 15,
    "primary_style": "D",
    "description": "Your Aries sun and Mars in the 10th house create a D-dominant profile with strong leadership tendencies and direct communication style."
}}"""

        return self._call_openai_for_assessment(prompt, DISCResult)
    
    def _generate_strengths_finder_llm(self, chart_data: str) -> StrengthsFinderResult:
        """Generate StrengthsFinder assessment using talent-focused astrological analysis"""
        
        prompt = f"""You are a master astrologer specializing in natural talent identification through birth chart analysis, working with Gallup's StrengthsFinder framework.

{chart_data}

🏆 NATURAL TALENT IDENTIFICATION:

Analyze this chart for the person's strongest natural talents using these 34 StrengthsFinder themes:

🧠 THINKING THEMES:
Analytical, Context, Futuristic, Ideation, Input, Intellection, Learner, Strategic

🤝 RELATING THEMES:
Empathy, Harmony, Includer, Individualization, Positivity, Relator

⚡ EXECUTING THEMES:
Achiever, Arranger, Belief, Consistency, Deliberative, Discipline, Focus, Responsibility, Restorative

💯 INFLUENCING THEMES:
Activator, Command, Communication, Competition, Maximizer, Self-Assurance, Significance, Woo

🔮 ASTROLOGICAL TALENT MAPPING:

Look for the STRONGEST planetary placements and aspects that indicate natural, effortless abilities:

- Which planets are in their ruling signs or exaltation?
- What themes appear in multiple chart areas (planets, houses, aspects)?
- Where does the chart show natural flow and ease vs. effort?
- What gifts emerge from the person's most harmonious aspects?
- How do the luminaries (Sun/Moon) express natural talents?
- What does the Midheaven and 10th house suggest about natural abilities?

🎯 SELECTION CRITERIA:
Choose the 5 themes that are most strongly and consistently indicated by:
1. Multiple astrological factors pointing to the same talent
2. Natural planetary strengths (dignity, aspects, house placement)
3. Themes that appear effortless rather than challenging
4. Gifts that support the person's life purpose and expression

Provide detailed astrological evidence for each selected strength:

{{
    "top_strengths": ["[5 most strongly indicated talents]"],
    "descriptions": {{
        "[Strength1]": "[Specific astrological evidence - planets, signs, houses, aspects that create this natural talent]",
        "[Strength2]": "[Specific astrological evidence for this gift]",
        "[Strength3]": "[Specific astrological evidence for this talent]",
        "[Strength4]": "[Specific astrological evidence for this ability]",
        "[Strength5]": "[Specific astrological evidence for this natural capacity]"
    }}
}}"""

        return self._call_openai_for_assessment(prompt, StrengthsFinderResult)
    
    def _generate_love_languages_llm(self, chart_data: str) -> LoveLanguagesResult:
        """Generate Love Languages assessment using LLM"""
        
        prompt = f"""You are an expert astrologer and psychologist. Based on the birth chart below, determine this person's love languages.

{chart_data}

Analyze Venus placement, 5th/7th house themes, and emotional patterns:

The 5 Love Languages:
- Words of Affirmation: Air signs, Mercury/Venus prominence
- Quality Time: Cancer/Libra emphasis, 4th/7th house themes
- Receiving Gifts: Taurus/Leo emphasis, Venus/2nd house themes
- Acts of Service: Virgo/Capricorn emphasis, 6th house themes
- Physical Touch: Fire/Water signs, Mars/Scorpio themes

Return ONLY a valid JSON object in this exact format:
{{
    "primary": "Quality Time",
    "secondary": "Physical Touch", 
    "scores": {{
        "Words of Affirmation": 15,
        "Quality Time": 35,
        "Receiving Gifts": 10,
        "Acts of Service": 20,
        "Physical Touch": 20
    }}
}}"""

        return self._call_openai_for_assessment(prompt, LoveLanguagesResult)
    
    def _generate_attachment_styles_llm(self, chart_data: str) -> AttachmentStyleResult:
        """Generate Attachment Styles assessment using LLM"""
        
        prompt = f"""You are an expert astrologer and psychologist. Based on the birth chart below, determine this person's attachment style.

{chart_data}

Analyze Moon sign, 4th house, family patterns, and emotional security themes:

Attachment Styles:
- Secure: Balanced emotional patterns, positive Moon aspects
- Anxious: Strong emotional needs, challenging Moon/Venus aspects
- Avoidant: Self-reliant patterns, Saturn/Capricorn emphasis
- Disorganized: Conflicting patterns, challenging aspects

Return ONLY a valid JSON object in this exact format:
{{
    "style": "Secure",
    "percentage": 75,
    "description": "Your Cancer moon in supportive aspects suggests a generally secure attachment style with strong emotional intelligence.",
    "characteristics": ["Comfortable with intimacy", "Good communication", "Emotionally stable", "Trusting in relationships"]
}}"""

        return self._call_openai_for_assessment(prompt, AttachmentStyleResult)
    
    def _generate_emotional_intelligence_llm(self, chart_data: str) -> EmotionalIntelligenceResult:
        """Generate Emotional Intelligence assessment using sophisticated EQ analysis"""
        
        prompt = f"""You are a leading expert in emotional intelligence and psychological astrology, specializing in how celestial patterns reveal emotional capacities and social intelligence.

{chart_data}

🧠 COMPREHENSIVE EMOTIONAL INTELLIGENCE ANALYSIS:

Analyze each EQ dimension through multiple astrological lenses, providing precise scores (1-100):

🪪 1. SELF-AWARENESS (Emotional Self-Knowledge):
- Moon sign and aspects: emotional pattern recognition
- Water sign emphasis: depth of feeling awareness
- 4th/8th/12th house planets: subconscious emotional access
- Mercury-Moon aspects: ability to articulate feelings
- Scorpio/Pisces placements: emotional depth perception
- Challenging aspects: forced emotional learning

⚙️ 2. SELF-REGULATION (Emotional Management):
- Saturn strength: emotional discipline and boundaries
- Earth sign grounding: practical emotional management
- Air sign detachment: perspective on emotions
- Mars aspects: impulse control and emotional expression
- Fixed sign emphasis: emotional stability vs. rigidity
- Mutable adaptability: emotional flexibility

🔥 3. MOTIVATION (Emotional Drive & Optimism):
- Fire sign vitality: enthusiasm and drive
- Sun strength and aspects: core motivation and life force
- Jupiter influence: optimism and future vision
- Mars placement: initiative and goal pursuit
- 5th/9th/10th house themes: creative and achievement motivation
- Challenging aspects: resilience through adversity

💕 4. EMPATHY (Understanding Others' Emotions):
- Water sign dominance: emotional attunement to others
- Moon-Neptune aspects: psychic/intuitive empathy
- Venus placements: harmony and relationship sensitivity
- 7th/11th house emphasis: other-awareness
- Pisces/Cancer strength: natural compassion
- Air signs: cognitive empathy and perspective-taking

🗣️ 5. SOCIAL SKILLS (Relationship Management):
- Air sign communication: verbal emotional intelligence
- Venus aspects: relationship harmony and charm
- Mercury-Venus connections: diplomatic communication
- 3rd/7th/11th house planets: social networking ability
- Fire sign leadership: inspiring and motivating others
- Cardinal signs: social initiative and leadership

🕰️ INTEGRATION ANALYSIS:
- How do these capacities work together as an emotional system?
- What are the person's greatest EQ gifts and challenges?
- How might emotional patterns have evolved through life experience?
- Where is there potential for continued EQ development?

Calculate precise scores considering multiple factors, not just obvious ones:

{{
    "overall_eq": [calculated average with weighting for chart emphasis],
    "self_awareness": [score based on lunar/water/introspective factors],
    "self_regulation": [score based on Saturn/earth/stability factors],
    "motivation": [score based on fire/sun/mars/jupiter factors],
    "empathy": [score based on water/neptune/venus factors],
    "social_skills": [score based on air/venus/mercury factors],
    "description": "[4-5 sentences explaining the specific astrological factors that create this person's unique emotional intelligence profile, including how different planetary energies integrate to support or challenge their EQ development]"
}}"""

        return self._call_openai_for_assessment(prompt, EmotionalIntelligenceResult)
    
    def _generate_career_personality_llm(self, chart_data: str) -> CareerPersonalityResult:
        """Generate Career Personality (Holland Code) assessment using LLM"""
        
        prompt = f"""You are an expert astrologer and psychologist. Based on the birth chart below, determine this person's Holland Code career personality.

{chart_data}

Analyze 10th house, Saturn/Mars placement, and vocational indicators:

Holland Codes:
- R (Realistic): Earth signs, practical skills, hands-on work
- I (Investigative): Air/Water signs, research, analysis  
- A (Artistic): Fire/Water signs, creativity, self-expression
- S (Social): Water/Air signs, helping, people-focused
- E (Enterprising): Fire signs, leadership, business
- C (Conventional): Earth signs, organization, structure

Select 3-letter code (e.g., EAS, RIC, SAI).

Return ONLY a valid JSON object in this exact format:
{{
    "holland_code": "EAS",
    "primary_type": "Enterprising",
    "career_matches": ["Business Manager", "Sales Director", "Entrepreneur", "Team Leader"],
    "work_environments": ["Leadership roles", "Dynamic environments", "People interaction", "Goal-oriented settings"]
}}"""

        return self._call_openai_for_assessment(prompt, CareerPersonalityResult)
    
    def _call_openai_for_assessment(self, prompt: str, result_class) -> any:
        """
        Helper method to call OpenAI API and parse result into the expected class
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a world-renowned expert in both psychological astrology and modern personality psychology, with deep understanding of how celestial patterns reveal psychological structures. Provide thoughtful, nuanced analysis. Respond ONLY with valid JSON in the exact format requested."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.8,  # Higher creativity for nuanced analysis
                max_tokens=2000   # More tokens for detailed reasoning
            )
            
            content = response.choices[0].message.content.strip()
            
            # Parse JSON response
            try:
                json_data = json.loads(content)
                return result_class(**json_data)
            except json.JSONDecodeError as e:
                print(f"JSON parsing error for {result_class.__name__}: {e}")
                print(f"Raw response: {content}")
                raise
                
        except Exception as e:
            print(f"Error calling OpenAI for {result_class.__name__}: {e}")
            raise

llm_service = LLMService()