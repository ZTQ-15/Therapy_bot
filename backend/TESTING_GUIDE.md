# 🧪 Complete Testing Guide for Mood Journal App

## 📋 **Overview**
This guide teaches you how to systematically test every feature of your mood journal app, from basic health checks to advanced AI recommendations.

## 🎯 **Testing Philosophy**
- **Start Simple**: Begin with basic connectivity
- **Test Incrementally**: Build up from simple to complex features
- **Verify Data**: Always check that data is saved and retrieved correctly
- **Test Edge Cases**: Try invalid inputs and error conditions
- **Document Results**: Keep track of what works and what doesn't

---

## 🚀 **Step 1: Health Check Testing**

### **Purpose**: Verify the server is running and accessible
### **Why Important**: Foundation for all other tests

```bash
# Test basic connectivity
curl -X GET http://localhost:8080/health

# Expected Response:
{
  "message": "Mood Journal API is running",
  "status": "healthy"
}
```

### **What to Check**:
- ✅ Server responds (status 200)
- ✅ Response format is correct JSON
- ✅ No error messages

---

## 🔐 **Step 2: Authentication Testing**

### **Purpose**: Ensure users can register, login, and access protected endpoints
### **Why Important**: Security foundation for the app

### **2.1 User Registration**
```bash
curl -X POST http://localhost:8080/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "newuser",
    "email": "newuser@example.com",
    "password": "password123",
    "age": 25,
    "nationality": "American",
    "gender": "female",
    "hobbies": ["reading", "music"]
  }'
```

### **2.2 User Login**
```bash
curl -X POST http://localhost:8080/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "identifier": "newuser",
    "password": "password123"
  }'
```

### **2.3 Token Verification**
```bash
curl -X POST http://localhost:8080/auth/verify \
  -H "Content-Type: application/json" \
  -d '{
    "token": "YOUR_JWT_TOKEN_HERE"
  }'
```

### **What to Check**:
- ✅ Registration creates user successfully
- ✅ Login returns valid JWT token
- ✅ Token can be verified
- ✅ Invalid credentials are rejected
- ✅ Protected endpoints require valid token

---

## 📝 **Step 3: Mood Journal Testing**

### **Purpose**: Test core mood logging functionality
### **Why Important**: This is the main feature of your app

### **3.1 Log a Mood**
```bash
curl -X POST http://localhost:8080/api/v1/mood/mood \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "mood": "happy",
    "intensity": 8,
    "description": "Had a great day at work",
    "note": "Everything went perfectly!"
  }'
```

### **3.2 Get Mood History**
```bash
curl -X GET http://localhost:8080/api/v1/mood/mood \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### **3.3 Get Mood Statistics**
```bash
curl -X GET http://localhost:8080/api/v1/mood/mood/stats \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### **What to Check**:
- ✅ Mood is saved with all fields (mood, intensity, description, note)
- ✅ Mood history shows all logged moods
- ✅ Statistics are calculated correctly
- ✅ Duplicate mood entries for same day are prevented
- ✅ Invalid intensity values are rejected

---

## 🤖 **Step 4: AI Recommendation Testing**

### **Purpose**: Test AI-powered recommendation system
### **Why Important**: This is your app's unique value proposition

### **4.1 Get Recommendation**
```bash
curl -X POST http://localhost:8080/api/v1/mood/recommend \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "mood": "sad",
    "description": "I broke up with my girlfriend today",
    "activity_type": "movie"
  }'
```

### **4.2 Test Different Moods**
```bash
# Test happy mood
curl -X POST http://localhost:8080/api/v1/mood/recommend \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "mood": "happy",
    "description": "Got promoted at work!",
    "activity_type": "cocktail"
  }'

# Test anxious mood
curl -X POST http://localhost:8080/api/v1/mood/recommend \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "mood": "anxious",
    "description": "Big presentation tomorrow",
    "activity_type": "activity"
  }'
```

### **What to Check**:
- ✅ Recommendations are generated for different moods
- ✅ Context (description) influences recommendations
- ✅ Different activity types work (movie, cocktail, activity)
- ✅ Recommendations include reasoning
- ✅ Fallback works when AI service is unavailable

---

## 👍 **Step 5: Feedback System Testing**

### **Purpose**: Test user feedback on recommendations
### **Why Important**: This enables the app to learn and improve

### **5.1 Submit Positive Feedback**
```bash
curl -X POST http://localhost:8080/api/v1/mood/feedback \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "recommendation_id": "RECOMMENDATION_ID",
    "liked": true,
    "mood": "happy"
  }'
```

### **5.2 Submit Negative Feedback**
```bash
curl -X POST http://localhost:8080/api/v1/mood/feedback \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "recommendation_id": "RECOMMENDATION_ID",
    "liked": false,
    "mood": "sad"
  }'
```

### **What to Check**:
- ✅ Feedback is saved correctly
- ✅ Like/dislike counts are updated
- ✅ Feedback is associated with correct recommendation
- ✅ Multiple feedback entries work

---

## 👥 **Step 6: Community Features Testing**

### **Purpose**: Test social features where users share experiences
### **Why Important**: Builds community and engagement

### **6.1 Create Community Post**
```bash
curl -X POST http://localhost:8080/api/v1/community/posts \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "mood": "excited",
    "activity_title": "Watched The Greatest Showman",
    "activity_description": "Amazing musical that really lifted my spirits!",
    "activity_type": "movie",
    "mood_intensity": 8,
    "description": "Needed something uplifting after a tough week",
    "note": "The music and story were so inspiring!"
  }'
```

### **6.2 Get Community Posts**
```bash
curl -X GET http://localhost:8080/api/v1/community/posts
```

### **6.3 Like a Post**
```bash
curl -X POST http://localhost:8080/api/v1/community/posts/POST_ID/like \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### **6.4 Star a Post**
```bash
curl -X POST http://localhost:8080/api/v1/community/posts/POST_ID/star \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### **6.5 Add Comment**
```bash
curl -X POST http://localhost:8080/api/v1/community/posts/POST_ID/comments \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "comment": "This movie is amazing! The soundtrack is incredible!"
  }'
```

### **What to Check**:
- ✅ Posts are created with all fields
- ✅ Posts are retrieved correctly
- ✅ Like/star functionality works
- ✅ Comments are added and retrieved
- ✅ User interactions are tracked

---

## 📊 **Step 7: User Insights Testing**

### **Purpose**: Test analytics and feedback analysis
### **Why Important**: Shows the app's intelligence and learning capabilities

### **7.1 Get User Insights**
```bash
curl -X GET http://localhost:8080/api/v1/mood/insights \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### **What to Check**:
- ✅ Mood patterns are analyzed
- ✅ Preferred activities are identified
- ✅ Recommendation effectiveness is calculated
- ✅ User preferences are tracked
- ✅ Insights are personalized per user

---

## 🔍 **Step 8: Error Handling Testing**

### **Purpose**: Test how the app handles invalid inputs and errors
### **Why Important**: Ensures app stability and user experience

### **8.1 Test Invalid Authentication**
```bash
# Test without token
curl -X GET http://localhost:8080/api/v1/mood/mood

# Test with invalid token
curl -X GET http://localhost:8080/api/v1/mood/mood \
  -H "Authorization: Bearer invalid_token"
```

### **8.2 Test Invalid Data**
```bash
# Test invalid mood intensity
curl -X POST http://localhost:8080/api/v1/mood/mood \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "mood": "happy",
    "intensity": 15,
    "description": "Test"
  }'

# Test missing required fields
curl -X POST http://localhost:8080/api/v1/mood/mood \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "mood": "happy"
  }'
```

### **What to Check**:
- ✅ Proper error messages are returned
- ✅ HTTP status codes are correct (400, 401, 404, 500)
- ✅ App doesn't crash on invalid input
- ✅ Validation works for all required fields

---

## 🧪 **Step 9: Integration Testing**

### **Purpose**: Test complete user workflows
### **Why Important**: Ensures features work together seamlessly

### **9.1 Complete User Journey**
```bash
# 1. Register user
# 2. Login and get token
# 3. Log a mood
# 4. Get recommendation
# 5. Submit feedback
# 6. Create community post
# 7. Get insights
```

### **What to Check**:
- ✅ All features work together
- ✅ Data flows correctly between features
- ✅ User experience is smooth
- ✅ No conflicts between features

---

## 📈 **Step 10: Performance Testing**

### **Purpose**: Test app performance under load
### **Why Important**: Ensures app can handle real users

### **10.1 Response Time Testing**
```bash
# Test response times
time curl -X GET http://localhost:8080/health
time curl -X GET http://localhost:8080/api/v1/mood/mood \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### **10.2 Load Testing**
```bash
# Test multiple requests
for i in {1..10}; do
  curl -X GET http://localhost:8080/health &
done
wait
```

### **What to Check**:
- ✅ Response times are reasonable (< 1 second)
- ✅ App handles multiple requests
- ✅ No memory leaks
- ✅ Database queries are efficient

---

## 🛠️ **Testing Tools and Tips**

### **Essential Tools**:
1. **curl**: Command-line HTTP client
2. **jq**: JSON processor for formatting responses
3. **Postman**: GUI tool for API testing
4. **Browser DevTools**: For frontend testing

### **Testing Best Practices**:
1. **Start with happy path**: Test normal usage first
2. **Test edge cases**: Try boundary values and invalid inputs
3. **Document everything**: Keep track of test results
4. **Automate when possible**: Create test scripts
5. **Test regularly**: Run tests after every change

### **Sample Test Script**:
```bash
#!/bin/bash
# test_mood_journal.sh

echo "🧪 Starting Mood Journal Tests..."

# Health check
echo "1. Testing health check..."
curl -s http://localhost:8080/health | jq '.'

# Login
echo "2. Testing login..."
TOKEN=$(curl -s -X POST http://localhost:8080/auth/login \
  -H "Content-Type: application/json" \
  -d '{"identifier": "testuser", "password": "password123"}' \
  | jq -r '.token')

echo "Token: $TOKEN"

# Log mood
echo "3. Testing mood logging..."
curl -s -X POST http://localhost:8080/api/v1/mood/mood \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"mood": "happy", "intensity": 8, "description": "Test mood"}' \
  | jq '.'

echo "✅ Tests completed!"
```

---

## 🎯 **Testing Checklist**

### **Before Demo/Deployment**:
- [ ] All endpoints respond correctly
- [ ] Authentication works properly
- [ ] Data is saved and retrieved correctly
- [ ] AI recommendations are generated
- [ ] Feedback system works
- [ ] Community features function
- [ ] Error handling is robust
- [ ] Performance is acceptable
- [ ] No security vulnerabilities
- [ ] Documentation is complete

### **Regular Testing**:
- [ ] Run health check daily
- [ ] Test new features immediately
- [ ] Verify data integrity weekly
- [ ] Check performance monthly
- [ ] Update test scripts as needed

---

## 🚀 **Next Steps**

1. **Create automated test scripts** for regular testing
2. **Set up monitoring** for production deployment
3. **Add unit tests** for individual functions
4. **Implement integration tests** for complete workflows
5. **Add performance benchmarks** for optimization

---

**Remember**: Good testing is the foundation of a reliable app. Test early, test often, and test thoroughly! 🎉 