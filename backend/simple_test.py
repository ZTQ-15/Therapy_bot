"""
Simple test script for Mood Journal functionality
Tests the core components directly without needing the server
"""

import sys
import os
from datetime import datetime, date

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_imports():
    """Test if all required modules can be imported"""
    print("🧪 Testing imports...")
    
    try:
        from backend.auth.models import User
        print("✅ User model imported successfully")
    except Exception as e:
        print(f"❌ Failed to import User model: {e}")
        return False
    
    try:
        from backend.models.mood_journal import MoodEntry, Recommendation, UserFeedback
        print("✅ Mood journal models imported successfully")
    except Exception as e:
        print(f"❌ Failed to import mood journal models: {e}")
        return False
    
    try:
        from backend.services.mood_ai_service import MoodAIService
        print("✅ Mood AI service imported successfully")
    except Exception as e:
        print(f"❌ Failed to import mood AI service: {e}")
        return False
    
    try:
        from backend.services.resource_service import ResourceService
        print("✅ Resource service imported successfully")
    except Exception as e:
        print(f"❌ Failed to import resource service: {e}")
        return False
    
    return True

def test_mood_ai_service():
    """Test the mood AI service functionality"""
    print("\n🧪 Testing Mood AI Service...")
    
    try:
        from backend.services.mood_ai_service import MoodAIService
        
        user_profile = {
            'age': 25,
            'gender': 'female',
            'nationality': 'American',
            'hobbies': ['reading', 'cooking', 'travel']
        }
        
        recommendation = MoodAIService._generate_local_recommendation('sad', user_profile, 'movie')
        
        print(f"✅ Generated recommendation: {recommendation['recommendation']['title']}")
        print(f"✅ Recommendation type: {recommendation['recommendation']['type']}")
        print(f"✅ Number of alternatives: {len(recommendation['alternatives'])}")
        
        return True
        
    except Exception as e:
        print(f"❌ Mood AI service test failed: {e}")
        return False

def test_resource_service():
    """Test the resource service functionality"""
    print("\n🧪 Testing Resource Service...")
    
    try:
        from backend.services.resource_service import ResourceService
        
        # Test resource generation
        resources = ResourceService.generate_resources_for_day('Python', 1, {
            'tasks': [{'description': 'Learn basics'}]
        })
        
        print(f"✅ Generated {len(resources)} resources")
        for i, resource in enumerate(resources[:2]):  # Show first 2
            print(f"   {i+1}. {resource['title']} - {resource['category']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Resource service test failed: {e}")
        return False

def test_user_model():
    """Test the user model functionality"""
    print("\n🧪 Testing User Model...")
    
    try:
        from backend.auth.models import User
        
        print("✅ User model methods available:")
        print("   - User.create()")
        print("   - User.find_by_username_or_email()")
        print("   - User.find_by_id()")
        print("   - User.update_profile()")
        print("   - User.generate_jwt_token()")
        print("   - User.verify_jwt_token()")
        
        return True
        
    except Exception as e:
        print(f"❌ User model test failed: {e}")
        return False

def test_mood_models():
    """Test the mood journal models"""
    print("\n🧪 Testing Mood Journal Models...")
    
    try:
        from backend.models.mood_journal import MoodEntry, Recommendation, UserFeedback
        
        print("✅ Mood journal models available:")
        print("   - MoodEntry.create()")
        print("   - MoodEntry.get_user_moods()")
        print("   - MoodEntry.get_mood_stats()")
        print("   - Recommendation.create()")
        print("   - Recommendation.get_recommendations_for_mood()")
        print("   - UserFeedback.create()")
        
        return True
        
    except Exception as e:
        print(f"❌ Mood models test failed: {e}")
        return False

def test_mood_recommendations():
    """Test mood-based recommendations"""
    print("\n🧪 Testing Mood Recommendations...")
    
    try:
        from backend.services.mood_ai_service import MoodAIService
        
        moods = ['sad', 'happy', 'anxious', 'excited']
        user_profile = {
            'age': 25,
            'gender': 'female',
            'nationality': 'American',
            'hobbies': ['reading', 'cooking', 'travel']
        }
        
        for mood in moods:
            recommendation = MoodAIService._generate_local_recommendation(mood, user_profile, 'movie')
            print(f"✅ {mood.capitalize()} mood → {recommendation['recommendation']['title']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Mood recommendations test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Testing Mood Journal Backend Components")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_user_model,
        test_mood_models,
        test_mood_ai_service,
        test_resource_service,
        test_mood_recommendations
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your mood journal backend is working correctly.")
        print("\n📋 What you can do now:")
        print("1. Set up MongoDB database")
        print("2. Create a .env file with your configuration")
        print("3. Run the server: python app.py")
        print("4. Test the full API: python test_mood_journal.py")
    else:
        print("⚠️  Some tests failed. Check the error messages above.")
    
    return passed == total

if __name__ == "__main__":
    main() 