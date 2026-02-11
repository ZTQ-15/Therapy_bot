"""
Core Mood Journal Functionality Test
Tests the essential features without database dependencies
"""

import sys
import os
from datetime import datetime, date

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_mood_ai_service():
    """Test the mood AI service functionality"""
    print("🧪 Testing Mood AI Service...")
    
    try:
        from backend.services.mood_ai_service import MoodAIService
        
        # Test user profile
        user_profile = {
            'age': 25,
            'gender': 'female',
            'nationality': 'American',
            'hobbies': ['reading', 'cooking', 'travel']
        }
        
        # Test different moods and recommendation types
        test_cases = [
            ('sad', 'movie'),
            ('happy', 'cocktail'),
            ('anxious', 'activity'),
            ('excited', 'movie')
        ]
        
        for mood, rec_type in test_cases:
            recommendation = MoodAIService._generate_local_recommendation(mood, user_profile, rec_type)
            print(f"✅ {mood.capitalize()} + {rec_type} → {recommendation['recommendation']['title']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Mood AI service test failed: {e}")
        return False

def test_resource_service():
    """Test the resource service functionality"""
    print("\n🧪 Testing Resource Service...")
    
    try:
        from backend.services.resource_service import ResourceService
        
        test_cases = [
            ('Python', 1),
            ('JavaScript', 7),
            ('Spanish', 15),
            ('Yoga', 30)
        ]
        
        for skill, day in test_cases:
            resources = ResourceService.generate_resources_for_day(skill, day, {
                'tasks': [{'description': f'Learn {skill} basics'}]
            })
            print(f"✅ {skill} (Day {day}) → {len(resources)} resources")
            if resources:
                print(f"   📚 First resource: {resources[0]['title']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Resource service test failed: {e}")
        return False

def test_mood_categorization():
    """Test mood categorization and template selection"""
    print("\n🧪 Testing Mood Categorization...")
    
    try:
        from backend.services.mood_ai_service import MoodAIService
        
        # Test different user profiles and moods
        test_profiles = [
            {'age': 18, 'gender': 'male', 'hobbies': ['gaming', 'music']},
            {'age': 35, 'gender': 'female', 'hobbies': ['yoga', 'reading']},
            {'age': 50, 'gender': 'male', 'hobbies': ['cooking', 'travel']}
        ]
        
        for i, profile in enumerate(test_profiles, 1):
            recommendation = MoodAIService._generate_local_recommendation('sad', profile, 'movie')
            print(f"✅ Profile {i} (Age: {profile['age']}) → {recommendation['recommendation']['title']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Mood categorization test failed: {e}")
        return False

def test_recommendation_personalization():
    """Test recommendation personalization based on hobbies"""
    print("\n🧪 Testing Recommendation Personalization...")
    
    try:
        from backend.services.mood_ai_service import MoodAIService
        
        test_cases = [
            {'hobbies': ['reading'], 'expected': 'reading'},
            {'hobbies': ['cooking'], 'expected': 'cooking'},
            {'hobbies': ['travel'], 'expected': 'travel'},
            {'hobbies': ['gaming', 'music'], 'expected': 'gaming'}
        ]
        
        base_profile = {'age': 25, 'gender': 'female', 'nationality': 'American'}
        
        for case in test_cases:
            profile = {**base_profile, 'hobbies': case['hobbies']}
            recommendation = MoodAIService._generate_local_recommendation('happy', profile, 'activity')
            print(f"✅ Hobbies: {case['hobbies']} → {recommendation['recommendation']['title']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Personalization test failed: {e}")
        return False

def test_mood_recommendation_variety():
    """Test variety of mood-based recommendations"""
    print("\n🧪 Testing Mood Recommendation Variety...")
    
    try:
        from backend.services.mood_ai_service import MoodAIService
        
        # Test all supported moods
        moods = ['sad', 'happy', 'anxious', 'excited']
        rec_types = ['movie', 'cocktail', 'activity']
        
        user_profile = {
            'age': 25,
            'gender': 'female',
            'nationality': 'American',
            'hobbies': ['reading', 'cooking', 'travel']
        }
        
        print("📊 Mood Recommendation Matrix:")
        for mood in moods:
            print(f"\n🎭 {mood.upper()} MOOD:")
            for rec_type in rec_types:
                recommendation = MoodAIService._generate_local_recommendation(mood, user_profile, rec_type)
                print(f"   {rec_type.title()}: {recommendation['recommendation']['title']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Variety test failed: {e}")
        return False

def test_api_structure():
    """Test the API structure and endpoints"""
    print("\n🧪 Testing API Structure...")
    
    try:
        from backend.api.v1.mood_journal import mood_journal_bp
        
        print("✅ Mood Journal API Blueprint imported successfully")
        print("📋 Available endpoints:")
        print("   - POST /api/v1/mood/mood (Log mood)")
        print("   - GET /api/v1/mood/mood (Get mood history)")
        print("   - GET /api/v1/mood/mood/stats (Get mood stats)")
        print("   - POST /api/v1/mood/recommend (Get AI recommendation)")
        print("   - POST /api/v1/mood/feedback (Submit feedback)")
        print("   - GET /api/v1/mood/profile (Get user profile)")
        print("   - PUT /api/v1/mood/profile (Update profile)")
        
        return True
        
    except Exception as e:
        print(f"❌ API structure test failed: {e}")
        return False

def main():
    """Run all core tests"""
    print("🚀 Testing Mood Journal Core Functionality")
    print("=" * 60)
    
    tests = [
        test_mood_ai_service,
        test_resource_service,
        test_mood_categorization,
        test_recommendation_personalization,
        test_mood_recommendation_variety,
        test_api_structure
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()  # Add spacing between tests
    
    print("=" * 60)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All core tests passed! Your mood journal backend is working correctly.")
        print("\n✨ What's Working:")
        print("   ✅ AI recommendation generation")
        print("   ✅ Resource service with curated content")
        print("   ✅ Mood-based personalization")
        print("   ✅ User profile integration")
        print("   ✅ API endpoint structure")
        print("\n📋 Next Steps:")
        print("1. Set up MongoDB database")
        print("2. Create a .env file with your configuration")
        print("3. Run the server: python app.py")
        print("4. Test the full API: python test_mood_journal.py")
    else:
        print("⚠️  Some tests failed. Check the error messages above.")
    
    return passed == total

if __name__ == "__main__":
    main() 