"""
Test script for Mood Journal API endpoints
Run this script to test the mood journal functionality
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8080"
API_BASE = f"{BASE_URL}/api/v1"

def test_register():
    """Test user registration"""
    print("🧪 Testing user registration...")
    
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "password123",
        "age": 25,
        "nationality": "American",
        "gender": "female",
        "hobbies": ["reading", "cooking", "travel"]
    }
    
    response = requests.post(f"{BASE_URL}/auth/register", json=user_data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    if response.status_code == 201:
        return response.json()['token']
    else:
        print("❌ Registration failed")
        return None

def test_login():
    """Test user login"""
    print("\n🧪 Testing user login...")
    
    login_data = {
        "identifier": "testuser",
        "password": "password123"
    }
    
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    if response.status_code == 200:
        return response.json()['token']
    else:
        print("❌ Login failed")
        return None

def test_log_mood(token):
    """Test logging a mood entry"""
    print("\n🧪 Testing mood logging...")
    
    headers = {"Authorization": f"Bearer {token}"}
    mood_data = {
        "mood": "sad",
        "intensity": 7,
        "note": "Feeling a bit down today"
    }
    
    response = requests.post(f"{API_BASE}/mood/mood", json=mood_data, headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    return response.status_code == 201

def test_get_mood_history(token):
    """Test getting mood history"""
    print("\n🧪 Testing mood history...")
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{API_BASE}/mood/mood", headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    return response.status_code == 200

def test_get_recommendation(token):
    """Test getting AI recommendation"""
    print("\n🧪 Testing AI recommendation...")
    
    headers = {"Authorization": f"Bearer {token}"}
    recommendation_data = {
        "mood": "sad",
        "activity_type": "movie"
    }
    
    response = requests.post(f"{API_BASE}/mood/recommend", json=recommendation_data, headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 200:
        return response.json()['recommendation']['id']
    else:
        print("❌ Recommendation failed")
        return None

def test_submit_feedback(token, recommendation_id):
    """Test submitting feedback"""
    print("\n🧪 Testing feedback submission...")
    
    headers = {"Authorization": f"Bearer {token}"}
    feedback_data = {
        "recommendation_id": recommendation_id,
        "liked": True,
        "mood": "sad"
    }
    
    response = requests.post(f"{API_BASE}/mood/feedback", json=feedback_data, headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    return response.status_code == 201

def test_get_profile(token):
    """Test getting user profile"""
    print("\n🧪 Testing profile retrieval...")
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{API_BASE}/mood/profile", headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    return response.status_code == 200

def test_update_profile(token):
    """Test updating user profile"""
    print("\n🧪 Testing profile update...")
    
    headers = {"Authorization": f"Bearer {token}"}
    update_data = {
        "age": 26,
        "hobbies": ["reading", "cooking", "travel", "photography"]
    }
    
    response = requests.put(f"{API_BASE}/mood/profile", json=update_data, headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    return response.status_code == 200

def main():
    """Run all tests"""
    print("🚀 Starting Mood Journal API Tests")
    print("=" * 50)
    
    # Test registration
    token = test_register()
    if not token:
        print("❌ Cannot proceed without authentication token")
        return
    
    # Test login
    login_token = test_login()
    if not login_token:
        print("❌ Login failed")
        return
    
    # Test mood logging
    if not test_log_mood(token):
        print("❌ Mood logging failed")
        return
    
    # Test mood history
    if not test_get_mood_history(token):
        print("❌ Mood history failed")
        return
    
    # Test recommendation
    recommendation_id = test_get_recommendation(token)
    if not recommendation_id:
        print("❌ Recommendation failed")
        return
    
    # Test feedback
    if not test_submit_feedback(token, recommendation_id):
        print("❌ Feedback submission failed")
        return
    
    # Test profile
    if not test_get_profile(token):
        print("❌ Profile retrieval failed")
        return
    
    # Test profile update
    if not test_update_profile(token):
        print("❌ Profile update failed")
        return
    
    print("\n✅ All tests completed successfully!")
    print("🎉 Mood Journal API is working correctly!")

if __name__ == "__main__":
    main() 