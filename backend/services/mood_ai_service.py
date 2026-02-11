import os
import httpx
import json
import logging
import time
from typing import Dict, Any, List
from datetime import datetime
from services.resource_service import ResourceService

API_PROVIDER = os.getenv("AI_PROVIDER", "openai").lower()
API_KEY = os.getenv("API_KEY")
MODEL_NAME = os.getenv("AI_MODEL_NAME", "gpt-4o-mini")

class MoodAIService:
    _recommendation_cache = {}
    _last_api_call = 0
    _api_cooldown = 3  # Reduced cooldown to 3 seconds to make AI recommendations more likely
    
    MOOD_RECOMMENDATIONS = {
        "sad": {
            "movies": [
                {"title": "The Secret Life of Walter Mitty", "description": "An uplifting adventure about finding purpose", "category": "feel-good"},
                {"title": "La La Land", "description": "Beautiful musical that celebrates dreams and love", "category": "musical"},
                {"title": "The Grand Budapest Hotel", "description": "Witty comedy with stunning visuals", "category": "comedy"},
                {"title": "Spirited Away", "description": "Magical animated film that transports you to another world", "category": "animation"},
                {"title": "The Princess Bride", "description": "Classic fairy tale with humor and heart", "category": "fantasy"}
            ],
            "cocktails": [
                {"title": "Hot Toddy", "description": "Warm, comforting drink with honey and whiskey", "ingredients": ["whiskey", "honey", "lemon", "hot water"]},
                {"title": "Chocolate Martini", "description": "Rich and indulgent chocolate cocktail", "ingredients": ["vodka", "chocolate liqueur", "cream"]},
                {"title": "Mulled Wine", "description": "Spiced warm wine perfect for cozy evenings", "ingredients": ["red wine", "cinnamon", "cloves", "orange"]},
                {"title": "Irish Coffee", "description": "Coffee with whiskey and cream", "ingredients": ["coffee", "whiskey", "cream", "sugar"]},
                {"title": "Butterbeer", "description": "Sweet, creamy drink inspired by Harry Potter", "ingredients": ["butterscotch", "cream soda", "whipped cream"]}
            ],
            "mocktails": [
                {"title": "Hot Chocolate", "description": "Rich and comforting hot chocolate with marshmallows", "ingredients": ["milk", "dark chocolate", "marshmallows", "whipped cream"]},
                {"title": "Golden Milk", "description": "Warming turmeric and honey drink", "ingredients": ["milk", "turmeric", "honey", "cinnamon", "ginger"]},
                {"title": "Apple Cider", "description": "Warm spiced apple cider", "ingredients": ["apple juice", "cinnamon", "cloves", "orange"]},
                {"title": "Herbal Tea", "description": "Soothing chamomile or lavender tea", "ingredients": ["chamomile tea", "honey", "lemon"]},
                {"title": "Hot Buttered Rum (Non-Alcoholic)", "description": "Warm spiced drink without alcohol", "ingredients": ["apple cider", "butter", "brown sugar", "spices"]}
            ],
            "music": [
                {"title": "Don't Stop Believin' - Journey", "description": "Uplifting anthem about hope and perseverance", "genre": "rock"},
                {"title": "Here Comes the Sun - The Beatles", "description": "Optimistic song about better days ahead", "genre": "pop"},
                {"title": "Good Life - OneRepublic", "description": "Positive song about appreciating what you have", "genre": "pop"},
                {"title": "Brave - Sara Bareilles", "description": "Empowering song about finding courage", "genre": "pop"},
                {"title": "Shake It Off - Taylor Swift", "description": "Upbeat song about moving past negativity", "genre": "pop"}
            ],
            "activities": [
                {"title": "Take a Warm Bath", "description": "Relax with essential oils and candles", "category": "self-care"},
                {"title": "Call a Friend", "description": "Reach out to someone who makes you smile", "category": "social"},
                {"title": "Listen to Upbeat Music", "description": "Create a happy playlist and dance", "category": "music"},
                {"title": "Cook Comfort Food", "description": "Make your favorite meal from scratch", "category": "cooking"},
                {"title": "Watch Funny Videos", "description": "Browse comedy clips on YouTube", "category": "entertainment"}
            ]
        },
        "happy": {
            "movies": [
                {"title": "The Greatest Showman", "description": "Energetic musical about following dreams", "category": "musical"},
                {"title": "Mamma Mia!", "description": "Fun ABBA musical with beautiful scenery", "category": "musical"},
                {"title": "The Devil Wears Prada", "description": "Chic comedy about fashion and ambition", "category": "comedy"},
                {"title": "Ocean's Eleven", "description": "Cool heist movie with great ensemble cast", "category": "thriller"},
                {"title": "The Intern", "description": "Heartwarming story about friendship and growth", "category": "comedy"}
            ],
            "cocktails": [
                {"title": "Mojito", "description": "Refreshing mint and lime cocktail", "ingredients": ["rum", "lime", "mint", "soda water"]},
                {"title": "Pina Colada", "description": "Tropical coconut and pineapple drink", "ingredients": ["rum", "coconut cream", "pineapple juice"]},
                {"title": "Margarita", "description": "Classic tequila and lime cocktail", "ingredients": ["tequila", "lime juice", "triple sec"]},
                {"title": "Bellini", "description": "Elegant peach and prosecco cocktail", "ingredients": ["prosecco", "peach puree"]},
                {"title": "French 75", "description": "Sophisticated gin and champagne cocktail", "ingredients": ["gin", "lemon juice", "champagne"]}
            ],
            "mocktails": [
                {"title": "Virgin Pina Colada", "description": "Tropical coconut and pineapple mocktail", "ingredients": ["coconut cream", "pineapple juice", "cream of coconut"]},
                {"title": "Strawberry Lemonade", "description": "Refreshing strawberry and lemon drink", "ingredients": ["strawberries", "lemon juice", "sugar", "water"]},
                {"title": "Mango Smoothie", "description": "Tropical mango and yogurt smoothie", "ingredients": ["mango", "yogurt", "honey", "milk"]},
                {"title": "Sparkling Grape Juice", "description": "Elegant sparkling grape drink", "ingredients": ["grape juice", "sparkling water", "lemon"]},
                {"title": "Tropical Punch", "description": "Colorful tropical fruit punch", "ingredients": ["pineapple juice", "orange juice", "cranberry juice", "sprite"]}
            ],
            "music": [
                {"title": "Happy - Pharrell Williams", "description": "Infectiously upbeat song about happiness", "genre": "pop"},
                {"title": "Walking on Sunshine - Katrina & The Waves", "description": "Energetic song about feeling great", "genre": "pop"},
                {"title": "Good Vibrations - The Beach Boys", "description": "Classic feel-good song", "genre": "pop"},
                {"title": "I Gotta Feeling - The Black Eyed Peas", "description": "Anthem for celebrating good times", "genre": "pop"},
                {"title": "Celebration - Kool & The Gang", "description": "Perfect party song for celebrations", "genre": "funk"}
            ],
            "activities": [
                {"title": "Plan a Trip", "description": "Research and plan your next adventure", "category": "travel"},
                {"title": "Try a New Recipe", "description": "Cook something you've never made before", "category": "cooking"},
                {"title": "Dance Party", "description": "Put on your favorite music and dance", "category": "music"},
                {"title": "Call Friends", "description": "Share your good mood with loved ones", "category": "social"},
                {"title": "Start a New Hobby", "description": "Begin learning something you've always wanted to try", "category": "learning"}
            ]
        },
        "anxious": {
            "movies": [
                {"title": "The Good Place", "description": "Philosophical comedy that's both smart and comforting", "category": "comedy"},
                {"title": "Parks and Recreation", "description": "Wholesome comedy about community", "category": "comedy"},
                {"title": "The Office", "description": "Relatable workplace comedy", "category": "comedy"},
                {"title": "Modern Family", "description": "Heartwarming family comedy", "category": "comedy"},
                {"title": "Friends", "description": "Classic sitcom about friendship and support", "category": "comedy"}
            ],
            "cocktails": [
                {"title": "Lavender Lemonade", "description": "Calming lavender with refreshing lemon", "ingredients": ["lavender syrup", "lemon juice", "sparkling water"]},
                {"title": "Chamomile Tea Cocktail", "description": "Soothing chamomile with honey", "ingredients": ["chamomile tea", "honey", "gin"]},
                {"title": "Blue Lagoon", "description": "Smooth and easy-drinking cocktail", "ingredients": ["vodka", "blue curacao", "lemonade"]},
                {"title": "Moscow Mule", "description": "Refreshing ginger and lime drink", "ingredients": ["vodka", "ginger beer", "lime"]},
                {"title": "White Russian", "description": "Smooth and creamy comfort drink", "ingredients": ["vodka", "coffee liqueur", "cream"]}
            ],
            "mocktails": [
                {"title": "Lavender Lemonade", "description": "Calming lavender with refreshing lemon", "ingredients": ["lavender syrup", "lemon juice", "sparkling water"]},
                {"title": "Chamomile Tea", "description": "Soothing chamomile with honey", "ingredients": ["chamomile tea", "honey", "lemon"]},
                {"title": "Blue Lagoon Mocktail", "description": "Smooth and easy-drinking mocktail", "ingredients": ["blue curacao syrup", "lemonade", "sprite"]},
                {"title": "Ginger Lemonade", "description": "Refreshing ginger and lemon drink", "ingredients": ["ginger syrup", "lemon juice", "sparkling water"]},
                {"title": "Vanilla Chai Latte", "description": "Smooth and creamy comfort drink", "ingredients": ["chai tea", "milk", "vanilla", "honey"]}
            ],
            "music": [
                {"title": "Weightless - Marconi Union", "description": "Scientifically proven to reduce anxiety", "genre": "ambient"},
                {"title": "Claire de Lune - Debussy", "description": "Peaceful classical piece", "genre": "classical"},
                {"title": "River Flows in You - Yiruma", "description": "Calming piano melody", "genre": "classical"},
                {"title": "The Scientist - Coldplay", "description": "Melancholic but soothing song", "genre": "alternative"},
                {"title": "Fix You - Coldplay", "description": "Comforting song about healing", "genre": "alternative"}
            ],
            "activities": [
                {"title": "Deep Breathing Exercise", "description": "Practice 4-7-8 breathing technique", "category": "wellness"},
                {"title": "Gentle Yoga", "description": "Try some calming yoga poses", "category": "exercise"},
                {"title": "Write in Journal", "description": "Express your thoughts and feelings", "category": "self-reflection"},
                {"title": "Take a Walk", "description": "Go for a peaceful walk in nature", "category": "outdoor"},
                {"title": "Listen to Calm Music", "description": "Put on some ambient or classical music", "category": "music"}
            ]
        },
        "excited": {
            "movies": [
                {"title": "Mission: Impossible", "description": "High-energy action and adventure", "category": "action"},
                {"title": "Mad Max: Fury Road", "description": "Intense and visually stunning action", "category": "action"},
                {"title": "Guardians of the Galaxy", "description": "Fun space adventure with great music", "category": "sci-fi"},
                {"title": "The Avengers", "description": "Epic superhero team-up", "category": "action"},
                {"title": "Jurassic Park", "description": "Thrilling dinosaur adventure", "category": "adventure"}
            ],
            "cocktails": [
                {"title": "Long Island Iced Tea", "description": "Strong and energizing cocktail", "ingredients": ["vodka", "gin", "rum", "tequila", "cola"]},
                {"title": "Red Bull Vodka", "description": "High-energy drink combination", "ingredients": ["vodka", "red bull"]},
                {"title": "Jagerbomb", "description": "Intense energy drink cocktail", "ingredients": ["jagermeister", "red bull"]},
                {"title": "Electric Lemonade", "description": "Bright and energizing blue cocktail", "ingredients": ["vodka", "blue curacao", "lemonade", "sprite"]},
                {"title": "Fireball Shot", "description": "Spicy and warming shot", "ingredients": ["fireball whiskey"]}
            ],
            "mocktails": [
                {"title": "Energy Drink Mocktail", "description": "High-energy non-alcoholic drink", "ingredients": ["red bull", "blue curacao syrup", "lemonade"]},
                {"title": "Electric Lemonade Mocktail", "description": "Bright and energizing blue mocktail", "ingredients": ["blue curacao syrup", "lemonade", "sprite"]},
                {"title": "Tropical Energy Punch", "description": "Energizing tropical fruit punch", "ingredients": ["pineapple juice", "orange juice", "energy drink", "sprite"]},
                {"title": "Berry Blast Smoothie", "description": "Energizing berry smoothie", "ingredients": ["mixed berries", "yogurt", "honey", "milk"]},
                {"title": "Citrus Sparkler", "description": "Bright and energizing citrus drink", "ingredients": ["orange juice", "lemon juice", "lime juice", "sparkling water"]}
            ],
            "music": [
                {"title": "Eye of the Tiger - Survivor", "description": "Epic motivational anthem", "genre": "rock"},
                {"title": "We Will Rock You - Queen", "description": "High-energy stadium anthem", "genre": "rock"},
                {"title": "Thunderstruck - AC/DC", "description": "Electrifying rock song", "genre": "rock"},
                {"title": "Can't Stop - Red Hot Chili Peppers", "description": "High-energy alternative rock", "genre": "alternative"},
                {"title": "Jump - Van Halen", "description": "Energetic classic rock", "genre": "rock"}
            ],
            "activities": [
                {"title": "Go Rock Climbing", "description": "Challenge yourself with indoor or outdoor climbing", "category": "adventure"},
                {"title": "Try a New Sport", "description": "Sign up for a class or join a team", "category": "sports"},
                {"title": "Plan a Party", "description": "Organize a celebration with friends", "category": "social"},
                {"title": "Learn to Dance", "description": "Take a dance class or learn online", "category": "learning"},
                {"title": "Go Skydiving", "description": "Experience the ultimate adrenaline rush", "category": "adventure"}
            ]
        }
    }
    
    async def generate_mood_recommendation(mood: str, user_profile: Dict[str, Any], description: str = None, activity_type: str = None) -> Dict[str, Any]:
        """
        Generate personalized recommendations based on mood, user profile, and what happened
        """
        # Always try to get fresh AI recommendations first
        if API_KEY:
            current_time = time.time()
            time_since_last_call = current_time - MoodAIService._last_api_call
            logging.info(f"Time since last API call: {time_since_last_call}s, cooldown: {MoodAIService._api_cooldown}s")
            
            if time_since_last_call >= MoodAIService._api_cooldown:
                try:
                    logging.info(f"Attempting fresh AI recommendation for mood: {mood}")
                    recommendation = await MoodAIService._generate_ai_recommendation(mood, user_profile, description, activity_type)
                    MoodAIService._last_api_call = current_time
                    logging.info(f"Successfully generated fresh AI recommendation for {mood}")
                    return recommendation
                except Exception as e:
                    logging.warning(f"AI service failed for {mood}: {e}")
                    logging.info(f"Falling back to local generation for {mood}")
                    return MoodAIService._generate_local_recommendation(mood, user_profile, activity_type)
            else:
                logging.info(f"API cooldown active ({time_since_last_call}s < {MoodAIService._api_cooldown}s), using local generation for {mood}")
                return MoodAIService._generate_local_recommendation(mood, user_profile, activity_type)
        
        logging.info(f"No API key available, using local generation for {mood}")
        return MoodAIService._generate_local_recommendation(mood, user_profile, activity_type)
    
    @staticmethod
    async def _generate_ai_recommendation(mood: str, user_profile: Dict[str, Any], description: str = None, activity_type: str = None) -> Dict[str, Any]:
        """Generate recommendation using AI service"""
        
        age = user_profile.get('age', 25)
        gender = user_profile.get('gender', 'unknown')
        nationality = user_profile.get('nationality', 'unknown')
        hobbies = user_profile.get('hobbies', [])
        
        # Build context about what happened
        context = ""
        if description:
            context = f"\nWhat happened: {description}"
        
        # Age restriction for alcohol
        age_restriction_note = ""
        if age and age < 18:
            age_restriction_note = f"\nIMPORTANT: User is {age} years old (under 18). DO NOT recommend alcoholic beverages. Instead, suggest non-alcoholic alternatives like mocktails, smoothies, or hot drinks."
        
        prompt = f"""You are a mood-based recommendation AI. Generate a personalized recommendation for a user who is feeling {mood}.{context}

User Profile:
- Age: {age}
- Gender: {gender}
- Nationality: {nationality}
- Hobbies: {', '.join(hobbies) if hobbies else 'Not specified'}{age_restriction_note}

Activity Type: {activity_type or 'any'}

Generate a JSON response with:
{{
    "recommendation": {{
        "type": "movie|cocktail|activity|music",
        "title": "Specific recommendation title",
        "description": "Why this is perfect for their mood and situation",
        "reasoning": "Explanation of why this matches their mood, what happened, and interests",
        "url": "Optional relevant URL",
        "category": "genre or category"
    }},
    "alternatives": [
        {{
            "type": "movie|cocktail|activity|music",
            "title": "Alternative option",
            "description": "Brief description"
        }}
    ]
}}

Provide 5 alternatives. Make it personal and contextual. Consider what happened to them, their age, interests, and cultural background. Be encouraging and supportive. If they're going through something difficult, offer comfort and hope.
"""
        
        try:
            if API_PROVIDER == "gemini":
                return await MoodAIService._generate_gemini_json(prompt)

            return await MoodAIService._generate_openai_json(prompt)
        except Exception as e:
            logging.error(f"AI service error: {e}")
            raise

    @staticmethod
    async def _generate_openai_json(prompt: str) -> Dict[str, Any]:
        async with httpx.AsyncClient(timeout=20.0) as client:
            response = await client.post(
                "https://api.openai.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": MODEL_NAME,
                    "messages": [
                        {"role": "system", "content": "Return valid JSON only."},
                        {"role": "user", "content": prompt}
                    ],
                    "response_format": {"type": "json_object"},
                    "max_completion_tokens": 1000
                }
            )

            if response.status_code == 429:
                MoodAIService._api_cooldown = min(60, MoodAIService._api_cooldown * 2)
                logging.warning(f"Rate limited by AI service. Increasing cooldown to {MoodAIService._api_cooldown}s")
                raise Exception("Rate limited by AI service")

            if response.status_code >= 400:
                logging.error(f"OpenAI error {response.status_code}: {response.text}")
                response.raise_for_status()

            response.raise_for_status()
            response_data = response.json()
            MoodAIService._api_cooldown = 3
            ai_response_content = response_data["choices"][0]["message"]["content"]
            return json.loads(ai_response_content)

    @staticmethod
    async def _generate_gemini_json(prompt: str) -> Dict[str, Any]:
        async with httpx.AsyncClient(timeout=20.0) as client:
            response = await client.post(
                f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_NAME}:generateContent?key={API_KEY}",
                headers={
                    "Content-Type": "application/json"
                },
                json={
                    "contents": [
                        {"role": "user", "parts": [{"text": prompt}]}
                    ],
                    "generationConfig": {
                        "temperature": 0.8,
                        "maxOutputTokens": 1000
                    }
                }
            )

            if response.status_code == 429:
                MoodAIService._api_cooldown = min(60, MoodAIService._api_cooldown * 2)
                logging.warning(f"Rate limited by AI service. Increasing cooldown to {MoodAIService._api_cooldown}s")
                raise Exception("Rate limited by AI service")

            response.raise_for_status()
            response_data = response.json()
            MoodAIService._api_cooldown = 3
            ai_response_content = response_data["candidates"][0]["content"]["parts"][0]["text"]
            return json.loads(ai_response_content)

    @staticmethod
    async def analyze_sentiment_and_counseling(entry_text: str, mood: str = None) -> Dict[str, Any]:
        """Provide sentiment analysis and supportive guidance."""
        if not API_KEY:
            return {
                "sentiment": "unknown",
                "risk_level": "unknown",
                "summary": "AI analysis unavailable without an API key.",
                "support": "Consider talking to someone you trust if you need support."
            }

        prompt = f"""
You are a supportive mental health assistant. Provide:
- A sentiment label: positive|neutral|negative
- A risk level: low|medium|high
- A short summary of what the user described
- Supportive, non-clinical guidance (no diagnosis, no medical claims)
- If high risk, encourage the user to reach out to local emergency services or a trusted person.

User entry:
Mood: {mood or 'unknown'}
Text: {entry_text}

Return JSON:
{{
  "sentiment": "positive|neutral|negative",
  "risk_level": "low|medium|high",
  "summary": "...",
  "support": "..."
}}
"""

        if API_PROVIDER == "gemini":
            return await MoodAIService._generate_gemini_json(prompt)

        return await MoodAIService._generate_openai_json(prompt)
    
    @staticmethod
    def _generate_local_recommendation(mood: str, user_profile: Dict[str, Any], description: str = None, activity_type: str = None) -> Dict[str, Any]:
        """Generate recommendation using local templates with enhanced personalization"""
        
        mood_lower = mood.lower()
        age = user_profile.get('age', 25)
        gender = user_profile.get('gender', 'unknown')
        nationality = user_profile.get('nationality', 'unknown')
        hobbies = user_profile.get('hobbies', [])
        
        # Use timestamp to make selections more varied
        timestamp = int(time.time())
        
        if mood_lower in MoodAIService.MOOD_RECOMMENDATIONS:
            mood_recs = MoodAIService.MOOD_RECOMMENDATIONS[mood_lower]
        else:
            mood_recs = MoodAIService.MOOD_RECOMMENDATIONS["happy"]
        
        # Enhanced age-based filtering
        if age and age < 18:
            if activity_type == "cocktail":
                activity_type = "mocktail"
            elif not activity_type:
                available_types = [k for k in mood_recs.keys() if k != "cocktails"]
                if available_types:
                    activity_type = available_types[timestamp % len(available_types)]
                else:
                    activity_type = "mocktail"
        elif age and age < 25:
            # Younger users might prefer more energetic content
            if not activity_type:
                energetic_types = ["music", "activities", "movies"]
                activity_type = energetic_types[timestamp % len(energetic_types)]
        
        if activity_type:
            rec_type = activity_type
        else:
            rec_type = list(mood_recs.keys())[timestamp % len(mood_recs.keys())]
        
        if rec_type in mood_recs:
            recommendation = MoodAIService._personalize_recommendation(
                mood_recs[rec_type], user_profile, rec_type, timestamp, description
            )
        else:
            recommendation = {
                "type": rec_type,
                "title": f"Custom {rec_type.title()} for {mood} mood",
                "description": f"A personalized {rec_type} recommendation based on your interests",
                "reasoning": f"This {rec_type} is selected to help improve your {mood} mood",
                "category": "general"
            }
        
        alternatives = []
        for alt_type in mood_recs.keys():
            if alt_type != rec_type:
                if age and age < 18 and alt_type == "cocktails":
                    continue
                    
                alt_recs = mood_recs[alt_type][:2]
                for alt_rec in alt_recs:
                    alternatives.append({
                        "type": alt_type,
                        "title": alt_rec["title"],
                        "description": alt_rec["description"]
                    })
        
        return {
            "recommendation": recommendation,
            "alternatives": alternatives[:5]
        }
    
    @staticmethod
    def _personalize_recommendation(recommendations: List[Dict], user_profile: Dict[str, Any], rec_type: str, timestamp: int, description: str = None) -> Dict[str, Any]:
        """Personalize recommendation based on user profile with enhanced logic"""
        # Filter recommendations based on user preferences
        filtered_recs = recommendations
        
        age = user_profile.get('age', 25)
        gender = user_profile.get('gender', 'unknown')
        nationality = user_profile.get('nationality', 'unknown')
        hobbies = [h.lower() for h in user_profile.get('hobbies', [])]
        
        # Enhanced age-based filtering
        if age and age < 25:
            # Younger users might prefer more energetic content
            energetic_keywords = ['energetic', 'upbeat', 'fun', 'exciting', 'adventure', 'party']
            energetic_recs = [r for r in filtered_recs if any(keyword in r.get('description', '').lower() for keyword in energetic_keywords)]
            if energetic_recs:
                filtered_recs = energetic_recs
        
        # Enhanced hobby-based filtering
        if hobbies:
            # Prioritize recommendations that match hobbies
            hobby_matches = [r for r in filtered_recs if any(hobby in r.get('description', '').lower() or hobby in r.get('title', '').lower() for hobby in hobbies)]
            if hobby_matches:
                filtered_recs = hobby_matches
        
        # Cultural/nationality-based filtering
        if nationality and nationality.lower() != 'unknown':
            # Could add cultural preferences here
            pass
        
        # Gender-based preferences (if relevant)
        if gender and gender.lower() != 'unknown':
            # Could add gender-specific preferences here
            pass
        
        # If no filtered results, use original list
        if not filtered_recs:
            filtered_recs = recommendations
        
        # Select recommendation using timestamp for variety
        timestamp_mod = timestamp % len(filtered_recs)
        rec = filtered_recs[timestamp_mod]
        
        # Build personalized reasoning
        reasoning_parts = []
        reasoning_parts.append(f"This {rec_type} is perfect for your {user_profile.get('mood', 'current')} mood")
        
        if description:
            reasoning_parts.append(f"Given what happened: '{description}'")
        
        if hobbies:
            reasoning_parts.append(f"Since you enjoy {', '.join(hobbies)}, this should resonate with your interests")
        
        if age:
            if age < 18:
                reasoning_parts.append("As a young person, this age-appropriate recommendation")
            elif age < 25:
                reasoning_parts.append("As a young adult, this energetic option")
            else:
                reasoning_parts.append(f"As a {age}-year-old, this mature choice")
        
        if nationality and nationality.lower() != 'unknown':
            reasoning_parts.append(f"Considering your {nationality} background")
        
        reasoning = ". ".join(reasoning_parts) + "."
        
        return {
            "title": rec["title"],
            "description": rec["description"],
            "type": rec_type,
            "category": rec.get("category", rec.get("genre", "general")),
            "url": rec.get("url"),
            "reasoning": reasoning
        }

    @staticmethod
    def analyze_user_feedback(user_id: str) -> Dict[str, Any]:
        """Analyze user feedback to improve future recommendations"""
        try:
            from models.mood_journal import UserFeedback, Recommendation
            from bson.objectid import ObjectId
            
            # Get user's feedback history
            feedback_history = UserFeedback.get_user_feedback_history(user_id)
            
            if not feedback_history:
                return {"preferences": {}, "improvements": []}
            
            # Analyze liked vs disliked recommendations
            liked_recommendations = []
            disliked_recommendations = []
            
            for feedback in feedback_history:
                if feedback.get('liked'):
                    liked_recommendations.append(feedback)
                else:
                    disliked_recommendations.append(feedback)
            
            # Extract patterns from liked recommendations
            liked_patterns = {}
            for feedback in liked_recommendations:
                mood = feedback.get('mood', '')
                if mood not in liked_patterns:
                    liked_patterns[mood] = {'count': 0, 'types': []}
                liked_patterns[mood]['count'] += 1
                
                # Get recommendation details
                rec = Recommendation.get_by_id(str(feedback.get('recommendation_id')))
                if rec:
                    rec_type = rec.get('activity_type', '')
                    if rec_type not in liked_patterns[mood]['types']:
                        liked_patterns[mood]['types'].append(rec_type)
            
            # Extract patterns from disliked recommendations
            disliked_patterns = {}
            for feedback in disliked_recommendations:
                mood = feedback.get('mood', '')
                if mood not in disliked_patterns:
                    disliked_patterns[mood] = {'count': 0, 'types': []}
                disliked_patterns[mood]['count'] += 1
                
                # Get recommendation details
                rec = Recommendation.get_by_id(str(feedback.get('recommendation_id')))
                if rec:
                    rec_type = rec.get('activity_type', '')
                    if rec_type not in disliked_patterns[mood]['types']:
                        disliked_patterns[mood]['types'].append(rec_type)
            
            # Generate improvement suggestions
            improvements = []
            
            # Suggest avoiding disliked types for specific moods
            for mood, pattern in disliked_patterns.items():
                if pattern['count'] >= 2:  # If user disliked 2+ of same type
                    for rec_type in pattern['types']:
                        improvements.append(f"Avoid {rec_type} recommendations when user is feeling {mood}")
            
            # Suggest focusing on liked types for specific moods
            for mood, pattern in liked_patterns.items():
                if pattern['count'] >= 2:  # If user liked 2+ of same type
                    for rec_type in pattern['types']:
                        improvements.append(f"Prioritize {rec_type} recommendations when user is feeling {mood}")
            
            return {
                "preferences": {
                    "liked_patterns": liked_patterns,
                    "disliked_patterns": disliked_patterns,
                    "total_feedback": len(feedback_history),
                    "like_ratio": len(liked_recommendations) / len(feedback_history) if feedback_history else 0
                },
                "improvements": improvements
            }
            
        except Exception as e:
            logging.error(f"Error analyzing user feedback: {e}")
            return {"preferences": {}, "improvements": []} 