from typing import Dict, List
from app.schemas.astro import BirthChart
from app.schemas.personality import *

class PersonalityEngine:
    """
    Core engine that maps astrological data to personality assessment results
    """
    
    def __init__(self):
        self.sign_traits = self._init_sign_traits()
        self.planet_influences = self._init_planet_influences()
    
    def generate_all_assessments(self, birth_chart: BirthChart) -> PersonalityAssessment:
        """Generate all 9 personality assessments from birth chart data"""
        
        return PersonalityAssessment(
            user_id="temp_user",  # Replace with actual user ID
            birth_data=birth_chart.dict(),
            mbti=self._generate_mbti(birth_chart),
            big_five=self._generate_big_five(birth_chart),
            enneagram=self._generate_enneagram(birth_chart),
            disc=self._generate_disc(birth_chart),
            strengths_finder=self._generate_strengths_finder(birth_chart),
            love_languages=self._generate_love_languages(birth_chart),
            attachment_styles=self._generate_attachment_styles(birth_chart),
            emotional_intelligence=self._generate_emotional_intelligence(birth_chart),
            career_personality=self._generate_career_personality(birth_chart),
            created_at="2024-01-01T00:00:00Z",
            confidence_score=0.85
        )
    
    def _generate_mbti(self, chart: BirthChart) -> MBTIResult:
        """Generate MBTI result based on sun, moon, and rising signs"""
        sun_sign = chart.sun_sign
        moon_sign = chart.moon_sign
        rising_sign = chart.rising_sign
        
        # Determine E/I based on fire/air vs earth/water emphasis
        extroversion_signs = ["Aries", "Gemini", "Leo", "Libra", "Sagittarius", "Aquarius"]
        e_score = sum(1 for sign in [sun_sign, rising_sign] if sign in extroversion_signs)
        ei = "E" if e_score >= 1 else "I"
        
        # Determine S/N based on earth/water vs fire/air
        sensing_signs = ["Taurus", "Virgo", "Capricorn", "Cancer", "Scorpio", "Pisces"]
        s_score = sum(1 for sign in [sun_sign, moon_sign] if sign in sensing_signs)
        sn = "S" if s_score >= 1 else "N"
        
        # Determine T/F based on air/fire vs water/earth emphasis for decision making
        thinking_signs = ["Gemini", "Libra", "Aquarius", "Aries", "Leo", "Sagittarius"]
        t_score = sum(1 for sign in [sun_sign, moon_sign] if sign in thinking_signs)
        tf = "T" if t_score >= 1 else "F"
        
        # Determine J/P based on cardinal/fixed vs mutable signs
        judging_signs = ["Aries", "Cancer", "Libra", "Capricorn", "Taurus", "Leo", "Scorpio", "Aquarius"]
        j_score = sum(1 for sign in [sun_sign, rising_sign] if sign in judging_signs)
        jp = "J" if j_score >= 1 else "P"
        
        mbti_type = f"{ei}{sn}{tf}{jp}"
        
        return MBTIResult(
            type=mbti_type,
            description=f"Based on your {sun_sign} sun and {rising_sign} rising, you exhibit {mbti_type} characteristics.",
            strengths=self._get_mbti_strengths(mbti_type),
            weaknesses=self._get_mbti_weaknesses(mbti_type),
            careers=self._get_mbti_careers(mbti_type)
        )
    
    def _generate_big_five(self, chart: BirthChart) -> BigFiveResult:
        """Generate Big Five scores based on planetary positions"""
        sun_sign = chart.sun_sign
        moon_sign = chart.moon_sign
        
        # Openness - influenced by Uranus, Aquarius, Gemini
        openness = 50
        if sun_sign in ["Aquarius", "Gemini", "Sagittarius"]: openness += 20
        if moon_sign in ["Aquarius", "Gemini", "Sagittarius"]: openness += 15
        
        # Conscientiousness - influenced by Saturn, Capricorn, Virgo
        conscientiousness = 50
        if sun_sign in ["Capricorn", "Virgo", "Taurus"]: conscientiousness += 25
        if moon_sign in ["Capricorn", "Virgo", "Taurus"]: conscientiousness += 15
        
        # Extraversion - fire and air signs
        extraversion = 50
        if sun_sign in ["Aries", "Leo", "Sagittarius", "Gemini", "Libra", "Aquarius"]: extraversion += 20
        if chart.rising_sign in ["Aries", "Leo", "Sagittarius", "Gemini", "Libra", "Aquarius"]: extraversion += 15
        
        # Agreeableness - water and earth signs, Venus influence
        agreeableness = 50
        if sun_sign in ["Cancer", "Pisces", "Libra", "Taurus"]: agreeableness += 20
        if moon_sign in ["Cancer", "Pisces", "Libra", "Taurus"]: agreeableness += 15
        
        # Neuroticism - influenced by water signs, challenging aspects
        neuroticism = 50
        if moon_sign in ["Cancer", "Scorpio", "Pisces"]: neuroticism += 15
        if sun_sign in ["Cancer", "Scorpio", "Pisces"]: neuroticism += 10
        
        # Clamp values between 1-100
        openness = max(1, min(100, openness))
        conscientiousness = max(1, min(100, conscientiousness))
        extraversion = max(1, min(100, extraversion))
        agreeableness = max(1, min(100, agreeableness))
        neuroticism = max(1, min(100, neuroticism))
        
        return BigFiveResult(
            openness=openness,
            conscientiousness=conscientiousness,
            extraversion=extraversion,
            agreeableness=agreeableness,
            neuroticism=neuroticism,
            description=f"Your {sun_sign} sun and {moon_sign} moon create this personality profile."
        )
    
    def _generate_enneagram(self, chart: BirthChart) -> EnneagramResult:
        """Generate Enneagram type based on core motivations from astrology"""
        sun_sign = chart.sun_sign
        moon_sign = chart.moon_sign
        
        # Map zodiac signs to likely Enneagram types
        sign_to_enneagram = {
            "Aries": [8, 3, 7],  # Challenger, Achiever, Enthusiast
            "Taurus": [9, 6, 2],  # Peacemaker, Loyalist, Helper
            "Gemini": [7, 6, 3],  # Enthusiast, Loyalist, Achiever
            "Cancer": [2, 6, 4],  # Helper, Loyalist, Individualist
            "Leo": [3, 8, 7],    # Achiever, Challenger, Enthusiast
            "Virgo": [1, 6, 5],  # Perfectionist, Loyalist, Investigator
            "Libra": [9, 2, 7],  # Peacemaker, Helper, Enthusiast
            "Scorpio": [8, 4, 5], # Challenger, Individualist, Investigator
            "Sagittarius": [7, 8, 9], # Enthusiast, Challenger, Peacemaker
            "Capricorn": [1, 3, 8], # Perfectionist, Achiever, Challenger
            "Aquarius": [5, 4, 7], # Investigator, Individualist, Enthusiast
            "Pisces": [4, 9, 2]   # Individualist, Peacemaker, Helper
        }
        
        # Get primary type from sun sign, modified by moon
        primary_types = sign_to_enneagram.get(sun_sign, [1])
        enneagram_type = primary_types[0]
        
        # Adjust based on moon sign
        moon_types = sign_to_enneagram.get(moon_sign, [])
        if moon_types and moon_types[0] in primary_types:
            enneagram_type = moon_types[0]
        
        wing = enneagram_type + 1 if enneagram_type < 9 else 1
        
        return EnneagramResult(
            type=enneagram_type,
            wing=wing,
            description=f"Your {sun_sign} core nature suggests Enneagram Type {enneagram_type}.",
            core_motivation=self._get_enneagram_motivation(enneagram_type),
            basic_fear=self._get_enneagram_fear(enneagram_type),
            strengths=self._get_enneagram_strengths(enneagram_type)
        )
    
    def _generate_disc(self, chart: BirthChart) -> DISCResult:
        """Generate DISC profile from astrological data"""
        sun_sign = chart.sun_sign
        mars_sign = next((p.sign for p in chart.planets if p.name == "Mars"), sun_sign)
        
        # Initialize base scores
        d = i = s = c = 25
        
        # Dominance - fire signs, Mars influence
        if sun_sign in ["Aries", "Leo", "Sagittarius"]: d += 30
        if mars_sign in ["Aries", "Scorpio", "Capricorn"]: d += 20
        
        # Influence - air signs, social planets
        if sun_sign in ["Gemini", "Libra", "Aquarius"]: i += 25
        if chart.rising_sign in ["Leo", "Libra", "Sagittarius"]: i += 20
        
        # Steadiness - earth and water signs
        if sun_sign in ["Taurus", "Cancer", "Virgo", "Pisces"]: s += 25
        if chart.moon_sign in ["Cancer", "Taurus", "Pisces"]: s += 20
        
        # Conscientiousness - earth signs, Saturn influence
        if sun_sign in ["Virgo", "Capricorn", "Taurus"]: c += 30
        
        # Normalize scores
        total = d + i + s + c
        d = int((d / total) * 100)
        i = int((i / total) * 100)
        s = int((s / total) * 100)
        c = 100 - d - i - s
        
        # Determine primary style
        scores = {"D": d, "I": i, "S": s, "C": c}
        primary_style = max(scores, key=scores.get)
        
        return DISCResult(
            dominance=d,
            influence=i,
            steadiness=s,
            conscientiousness=c,
            primary_style=primary_style,
            description=f"Your {sun_sign} sun creates a {primary_style}-dominant DISC profile."
        )
    
    def _generate_strengths_finder(self, chart: BirthChart) -> StrengthsFinderResult:
        """Generate top 5 strengths based on planetary positions"""
        sun_sign = chart.sun_sign
        moon_sign = chart.moon_sign
        rising_sign = chart.rising_sign
        
        # Map signs to StrengthsFinder themes
        sign_strengths = {
            "Aries": ["Achiever", "Command", "Competition", "Activator"],
            "Taurus": ["Deliberative", "Consistency", "Restorative", "Responsibility"],
            "Gemini": ["Communication", "Intellection", "Learner", "Adaptability"],
            "Cancer": ["Empathy", "Developer", "Harmony", "Includer"],
            "Leo": ["Command", "Positivity", "Self-Assurance", "Maximizer"],
            "Virgo": ["Analytical", "Discipline", "Focus", "Responsibility"],
            "Libra": ["Harmony", "Connectedness", "Empathy", "Diplomatic"],
            "Scorpio": ["Focus", "Strategic", "Restorative", "Intensity"],
            "Sagittarius": ["Positivity", "Futuristic", "Learner", "Activator"],
            "Capricorn": ["Achiever", "Responsibility", "Discipline", "Focus"],
            "Aquarius": ["Futuristic", "Ideation", "Intellection", "Innovation"],
            "Pisces": ["Empathy", "Harmony", "Connectedness", "Developer"]
        }
        
        strengths = set()
        strengths.update(sign_strengths.get(sun_sign, [])[:2])
        strengths.update(sign_strengths.get(moon_sign, [])[:2])
        strengths.update(sign_strengths.get(rising_sign, [])[:1])
        
        # Ensure we have exactly 5 strengths
        all_strengths = [
            "Achiever", "Activator", "Adaptability", "Analytical", "Arranger",
            "Belief", "Command", "Communication", "Competition", "Connectedness",
            "Consistency", "Context", "Deliberative", "Developer", "Discipline",
            "Empathy", "Focus", "Futuristic", "Harmony", "Ideation",
            "Includer", "Individualization", "Input", "Intellection", "Learner",
            "Maximizer", "Positivity", "Relator", "Responsibility", "Restorative",
            "Self-Assurance", "Significance", "Strategic", "Woo"
        ]
        
        while len(strengths) < 5:
            for strength in all_strengths:
                if strength not in strengths:
                    strengths.add(strength)
                    break
        
        top_strengths = list(strengths)[:5]
        
        return StrengthsFinderResult(
            top_strengths=top_strengths,
            descriptions={strength: f"This strength is indicated by your astrological profile." 
                         for strength in top_strengths}
        )
    
    def _generate_love_languages(self, chart: BirthChart) -> LoveLanguagesResult:
        """Generate love languages based on Venus sign and aspects"""
        venus_sign = next((p.sign for p in chart.planets if p.name == "Venus"), chart.sun_sign)
        
        # Map Venus signs to love languages
        venus_to_love_language = {
            "Aries": "Physical Touch",
            "Taurus": "Receiving Gifts",
            "Gemini": "Words of Affirmation",
            "Cancer": "Quality Time",
            "Leo": "Words of Affirmation",
            "Virgo": "Acts of Service",
            "Libra": "Quality Time",
            "Scorpio": "Physical Touch",
            "Sagittarius": "Quality Time",
            "Capricorn": "Acts of Service",
            "Aquarius": "Words of Affirmation",
            "Pisces": "Physical Touch"
        }
        
        primary = venus_to_love_language.get(venus_sign, "Quality Time")
        
        # Secondary based on moon sign
        moon_to_love_language = {
            "Cancer": "Quality Time",
            "Taurus": "Physical Touch",
            "Virgo": "Acts of Service",
            "Leo": "Words of Affirmation",
            "Scorpio": "Physical Touch"
        }
        
        secondary = moon_to_love_language.get(chart.moon_sign, "Acts of Service")
        if secondary == primary:
            secondary = "Receiving Gifts"
        
        scores = {
            "Words of Affirmation": 15,
            "Quality Time": 15,
            "Receiving Gifts": 15,
            "Acts of Service": 15,
            "Physical Touch": 15
        }
        
        scores[primary] += 25
        scores[secondary] += 15
        
        return LoveLanguagesResult(
            primary=primary,
            secondary=secondary,
            scores=scores
        )
    
    def _generate_attachment_styles(self, chart: BirthChart) -> AttachmentStyleResult:
        """Generate attachment style based on moon sign and aspects"""
        moon_sign = chart.moon_sign
        
        # Map moon signs to attachment styles
        moon_to_attachment = {
            "Cancer": ("Secure", 70),
            "Taurus": ("Secure", 75),
            "Leo": ("Secure", 65),
            "Scorpio": ("Anxious", 60),
            "Pisces": ("Anxious", 55),
            "Virgo": ("Avoidant", 60),
            "Capricorn": ("Avoidant", 65),
            "Aquarius": ("Avoidant", 70),
            "Aries": ("Anxious", 50),
            "Gemini": ("Avoidant", 50),
            "Libra": ("Secure", 60),
            "Sagittarius": ("Avoidant", 55)
        }
        
        style, percentage = moon_to_attachment.get(moon_sign, ("Secure", 60))
        
        return AttachmentStyleResult(
            style=style,
            percentage=percentage,
            description=f"Your {moon_sign} moon suggests a {style} attachment style.",
            characteristics=self._get_attachment_characteristics(style)
        )
    
    def _generate_emotional_intelligence(self, chart: BirthChart) -> EmotionalIntelligenceResult:
        """Generate EQ scores based on water sign emphasis and aspects"""
        moon_sign = chart.moon_sign
        sun_sign = chart.sun_sign
        
        # Base EQ from water sign emphasis
        water_signs = ["Cancer", "Scorpio", "Pisces"]
        base_eq = 50
        
        if moon_sign in water_signs: base_eq += 20
        if sun_sign in water_signs: base_eq += 15
        
        # Individual components
        self_awareness = base_eq + (10 if moon_sign in water_signs else 0)
        self_regulation = base_eq + (15 if sun_sign in ["Capricorn", "Virgo", "Libra"] else 0)
        motivation = base_eq + (15 if sun_sign in ["Aries", "Leo", "Sagittarius"] else 0)
        empathy = base_eq + (20 if moon_sign in water_signs else 0)
        social_skills = base_eq + (15 if chart.rising_sign in ["Gemini", "Libra", "Leo"] else 0)
        
        # Normalize
        overall_eq = int((self_awareness + self_regulation + motivation + empathy + social_skills) / 5)
        overall_eq = max(30, min(95, overall_eq))
        
        return EmotionalIntelligenceResult(
            overall_eq=overall_eq,
            self_awareness=max(30, min(95, self_awareness)),
            self_regulation=max(30, min(95, self_regulation)),
            motivation=max(30, min(95, motivation)),
            empathy=max(30, min(95, empathy)),
            social_skills=max(30, min(95, social_skills)),
            description=f"Your {moon_sign} moon contributes to your emotional intelligence profile."
        )
    
    def _generate_career_personality(self, chart: BirthChart) -> CareerPersonalityResult:
        """Generate Holland Code career personality"""
        sun_sign = chart.sun_sign
        
        # Map signs to Holland codes
        sign_to_holland = {
            "Aries": "E",      # Enterprising
            "Taurus": "R",     # Realistic
            "Gemini": "A",     # Artistic
            "Cancer": "S",     # Social
            "Leo": "E",        # Enterprising
            "Virgo": "C",      # Conventional
            "Libra": "A",      # Artistic
            "Scorpio": "I",    # Investigative
            "Sagittarius": "E", # Enterprising
            "Capricorn": "C",  # Conventional
            "Aquarius": "I",   # Investigative
            "Pisces": "A"      # Artistic
        }
        
        primary = sign_to_holland.get(sun_sign, "S")
        
        # Add secondary and tertiary based on other planets
        mercury_sign = next((p.sign for p in chart.planets if p.name == "Mercury"), sun_sign)
        secondary = sign_to_holland.get(mercury_sign, "I")
        
        # Ensure different codes
        if secondary == primary:
            secondary = "S"
        
        tertiary = "A" if primary not in ["A"] and secondary not in ["A"] else "R"
        
        holland_code = f"{primary}{secondary}{tertiary}"
        
        return CareerPersonalityResult(
            holland_code=holland_code,
            primary_type=self._get_holland_type_name(primary),
            career_matches=self._get_holland_careers(primary),
            work_environments=self._get_holland_environments(primary)
        )
    
    # Helper methods for generating specific content
    def _init_sign_traits(self) -> Dict:
        return {
            "Aries": {"keywords": ["leader", "energetic", "impulsive", "competitive"]},
            "Taurus": {"keywords": ["stable", "practical", "stubborn", "reliable"]},
            # ... etc for all signs
        }
    
    def _init_planet_influences(self) -> Dict:
        return {
            "Sun": {"represents": "core self, ego, vitality"},
            "Moon": {"represents": "emotions, instincts, subconscious"},
            # ... etc for all planets
        }
    
    def _get_mbti_strengths(self, mbti_type: str) -> List[str]:
        return ["Natural leadership", "Creative problem solving", "Strong communication"]
    
    def _get_mbti_weaknesses(self, mbti_type: str) -> List[str]:
        return ["Can be impulsive", "May overlook details", "Difficulty with routine"]
    
    def _get_mbti_careers(self, mbti_type: str) -> List[str]:
        return ["Entrepreneur", "Consultant", "Creative Director", "Teacher"]
    
    def _get_enneagram_motivation(self, type_num: int) -> str:
        motivations = {
            1: "To be perfect and improve everything",
            2: "To feel loved and needed",
            3: "To feel valuable and worthwhile",
            4: "To find themselves and their significance",
            5: "To be competent and understanding",
            6: "To have security and support",
            7: "To maintain happiness and satisfaction",
            8: "To be self-reliant and in control",
            9: "To maintain inner peace and harmony"
        }
        return motivations.get(type_num, "To find balance")
    
    def _get_enneagram_fear(self, type_num: int) -> str:
        fears = {
            1: "Being corrupt, defective, or wrong",
            2: "Being unloved or unwanted",
            3: "Being worthless without achievement",
            4: "Having no identity or significance",
            5: "Being useless, helpless, or incapable",
            6: "Being without support or guidance",
            7: "Being trapped in pain or deprivation",
            8: "Being controlled or vulnerable",
            9: "Loss of connection and fragmentation"
        }
        return fears.get(type_num, "Being disconnected")
    
    def _get_enneagram_strengths(self, type_num: int) -> List[str]:
        return ["Self-aware", "Empathetic", "Driven", "Creative"]
    
    def _get_attachment_characteristics(self, style: str) -> List[str]:
        characteristics = {
            "Secure": ["Comfortable with intimacy", "Good communication", "Trusting"],
            "Anxious": ["Seeks reassurance", "Fear of abandonment", "Highly empathetic"],
            "Avoidant": ["Values independence", "Uncomfortable with closeness", "Self-reliant"],
            "Disorganized": ["Inconsistent behaviors", "Difficulty regulating emotions"]
        }
        return characteristics.get(style, ["Balanced approach to relationships"])
    
    def _get_holland_type_name(self, code: str) -> str:
        names = {
            "R": "Realistic", "I": "Investigative", "A": "Artistic",
            "S": "Social", "E": "Enterprising", "C": "Conventional"
        }
        return names.get(code, "Social")
    
    def _get_holland_careers(self, code: str) -> List[str]:
        careers = {
            "R": ["Engineer", "Mechanic", "Farmer", "Pilot"],
            "I": ["Scientist", "Researcher", "Analyst", "Doctor"],
            "A": ["Artist", "Writer", "Designer", "Musician"],
            "S": ["Teacher", "Counselor", "Nurse", "Social Worker"],
            "E": ["Manager", "Lawyer", "Sales", "Entrepreneur"],
            "C": ["Accountant", "Administrator", "Banker", "Secretary"]
        }
        return careers.get(code, ["Teacher", "Counselor", "Manager"])
    
    def _get_holland_environments(self, code: str) -> List[str]:
        environments = {
            "R": ["Hands-on work", "Outdoor settings", "Technical environments"],
            "I": ["Research labs", "Academic settings", "Analytical work"],
            "A": ["Creative studios", "Flexible schedules", "Artistic communities"],
            "S": ["People-oriented", "Collaborative", "Helping environments"],
            "E": ["Leadership roles", "Competitive", "Business settings"],
            "C": ["Structured", "Detail-oriented", "Organized systems"]
        }
        return environments.get(code, ["Collaborative", "People-oriented"])

personality_engine = PersonalityEngine()