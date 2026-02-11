# Mood Journal API Documentation

## 🎯 Overview

The Mood Journal API is a comprehensive backend system for tracking daily moods and providing AI-powered recommendations for activities, movies, cocktails, and more based on the user's emotional state and personal preferences.

## 🚀 Features

### Core Features
- **Daily Mood Tracking**: Log moods with intensity levels and notes
- **AI Recommendations**: Get personalized suggestions based on mood and profile
- **User Profiles**: Store age, nationality, gender, and hobbies for better recommendations
- **Feedback System**: Rate recommendations to improve future suggestions
- **Mood Analytics**: Track mood patterns and statistics

### AI Recommendation Types
- **Movies**: Curated film suggestions for different moods
- **Cocktails**: Drink recommendations with ingredients
- **Activities**: Personalized activity suggestions
- **Music**: Mood-based music recommendations

## 📋 API Endpoints

### Authentication

#### Register User
```http
POST /auth/register
```

**Request Body:**
```json
{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "password123",
  "age": 25,
  "nationality": "American",
  "gender": "male",
  "hobbies": ["reading", "cooking", "travel"]
}
```

**Response:**
```json
{
  "message": "User created successfully",
  "token": "jwt_token_here",
  "user": {
    "id": "user_id",
    "username": "johndoe",
    "email": "john@example.com",
    "age": 25,
    "nationality": "American",
    "gender": "male",
    "hobbies": ["reading", "cooking", "travel"]
  }
}
```

#### Login
```http
POST /auth/login
```

**Request Body:**
```json
{
  "identifier": "johndoe",
  "password": "password123"
}
```

### Mood Journal

#### Log Mood
```http
POST /api/v1/mood/mood
```

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Request Body:**
```json
{
  "mood": "sad",
  "intensity": 7,
  "note": "Feeling a bit down today"
}
```

**Response:**
```json
{
  "message": "Mood logged successfully",
  "mood_id": "mood_entry_id",
  "mood": "sad",
  "intensity": 7,
  "date": "2024-01-15"
}
```

#### Get Mood History
```http
GET /api/v1/mood/mood?limit=30
```

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Response:**
```json
{
  "moods": [
    {
      "_id": "mood_id",
      "user_id": "user_id",
      "mood": "sad",
      "intensity": 7,
      "note": "Feeling a bit down today",
      "created_at": "2024-01-15T10:30:00Z",
      "date": "2024-01-15"
    }
  ],
  "count": 1
}
```

#### Get Mood Statistics
```http
GET /api/v1/mood/mood/stats?days=7
```

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Response:**
```json
{
  "stats": [
    {
      "_id": "sad",
      "count": 3,
      "avg_intensity": 6.5
    },
    {
      "_id": "happy",
      "count": 4,
      "avg_intensity": 8.2
    }
  ],
  "period_days": 7
}
```

### AI Recommendations

#### Get Recommendation
```http
POST /api/v1/mood/recommend
```

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Request Body:**
```json
{
  "mood": "sad",
  "activity_type": "movie"
}
```

**Response:**
```json
{
  "recommendation": {
    "id": "recommendation_id",
    "type": "movie",
    "title": "The Secret Life of Walter Mitty",
    "description": "An uplifting adventure about finding purpose",
    "reasoning": "This feel-good movie is perfect for lifting your spirits when feeling down",
    "category": "feel-good"
  },
  "alternatives": [
    {
      "type": "cocktail",
      "title": "Hot Toddy",
      "description": "Warm, comforting drink with honey and whiskey"
    },
    {
      "type": "activity",
      "title": "Take a Warm Bath",
      "description": "Relax with essential oils and candles"
    }
  ]
}
```

#### Submit Feedback
```http
POST /api/v1/mood/feedback
```

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Request Body:**
```json
{
  "recommendation_id": "recommendation_id",
  "liked": true,
  "mood": "sad"
}
```

**Response:**
```json
{
  "message": "Feedback submitted successfully",
  "feedback_id": "feedback_id",
  "liked": true
}
```

### User Profile

#### Get Profile
```http
GET /api/v1/mood/profile
```

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Response:**
```json
{
  "username": "johndoe",
  "email": "john@example.com",
  "age": 25,
  "gender": "male",
  "nationality": "American",
  "hobbies": ["reading", "cooking", "travel"],
  "created_at": "2024-01-01T00:00:00Z"
}
```

#### Update Profile
```http
PUT /api/v1/mood/profile
```

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Request Body:**
```json
{
  "age": 26,
  "hobbies": ["reading", "cooking", "travel", "photography"]
}
```

**Response:**
```json
{
  "message": "Profile updated successfully",
  "updated_fields": ["age", "hobbies"]
}
```

## 🎭 Supported Moods

The AI system recognizes and provides recommendations for these moods:

- **Sad**: Comforting movies, warm drinks, self-care activities
- **Happy**: Energetic films, celebratory cocktails, adventure activities
- **Anxious**: Calming content, soothing drinks, relaxation activities
- **Excited**: High-energy content, strong drinks, adrenaline activities

## 🍹 Cocktail Recommendations

Each cocktail recommendation includes:
- **Title**: Name of the cocktail
- **Description**: Why it's perfect for the mood
- **Ingredients**: List of ingredients needed
- **Category**: Type of drink (comfort, celebration, etc.)

## 🎬 Movie Recommendations

Movie recommendations include:
- **Title**: Film name
- **Description**: Brief synopsis and mood fit
- **Category**: Genre (comedy, feel-good, action, etc.)
- **Reasoning**: Why it matches the user's mood and interests

## 🏃 Activity Recommendations

Activity suggestions include:
- **Title**: Activity name
- **Description**: What the activity involves
- **Category**: Type (self-care, social, outdoor, etc.)

## 🛠️ Setup Instructions

### Prerequisites
- Python 3.8+
- MongoDB
- Redis (optional, for caching)

### Environment Variables
Create a `.env` file:

```bash
# Database
MONGO_URI=mongodb://localhost:27017/mood_journal_db

# JWT & Security
JWT_SECRET_KEY=your-super-secret-jwt-key-here

# AI Service (Optional)
OPENROUTER_API_KEY=your-openrouter-api-key-here
AI_MODEL_NAME=deepseek/deepseek-r1-0528:free
```

### Installation
```bash
cd backend
pip install -r requirements.txt
python app.py
```

### Testing
```bash
python test_mood_journal.py
```

## 🔧 Technical Details

### AI Service Architecture
- **Primary**: OpenRouter AI API for personalized recommendations
- **Fallback**: Curated recommendation templates
- **Caching**: In-memory cache to reduce API calls
- **Rate Limiting**: 30-second cooldown between AI requests

### Database Collections
- `users`: User profiles and authentication
- `mood_entries`: Daily mood logs
- `recommendations`: AI-generated recommendations
- `user_feedback`: User ratings and feedback

### Security Features
- JWT token authentication
- Password hashing with bcrypt
- Input validation and sanitization
- Rate limiting on API endpoints

## 🎯 Use Cases

### Example Flow
1. **User Registration**: Create account with profile info
2. **Daily Mood Log**: Log current mood and intensity
3. **AI Recommendation**: Get personalized suggestion
4. **Try Activity**: User follows the recommendation
5. **Provide Feedback**: Rate how well it worked
6. **Improved Suggestions**: AI learns from feedback

### Sample User Journey
```
User feels sad → Logs mood (sad, intensity 7) 
→ AI suggests "The Secret Life of Walter Mitty" 
→ User watches movie → Provides positive feedback 
→ Future sad moods get similar uplifting recommendations
```

## 🚀 Future Enhancements

- **Mood Patterns**: Advanced analytics and insights
- **Social Features**: Share mood journeys with friends
- **Integration**: Connect with calendar and weather apps
- **Machine Learning**: More sophisticated recommendation algorithms
- **Voice Integration**: Voice-based mood logging
- **Mood Triggers**: Identify what causes mood changes

## 📞 Support

For questions or issues, please refer to the main project documentation or create an issue in the repository. 