# Mood Journal Backend

A clean, focused backend API for a mood journal application with AI-powered recommendations.

## 🎯 Features

- **User Authentication**: Register and login with JWT tokens
- **Mood Tracking**: Log daily moods with intensity and notes
- **AI Recommendations**: Get personalized suggestions for movies, cocktails, and activities
- **User Profiles**: Store age, nationality, gender, and hobbies
- **Feedback System**: Rate recommendations to improve future suggestions

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- MongoDB

### Installation

1. **Clone and navigate to backend:**

   ```bash
   cd backend
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   Create a `.env` file:

   ```bash
   MONGO_URI=mongodb://localhost:27017/mood_journal_db
   JWT_SECRET_KEY=your-super-secret-jwt-key-here
   AI_PROVIDER=openai
   AI_MODEL_NAME=gpt-4o-mini
   API_KEY=your-api-key-here

   ```

4. **Run the server:**

   ```bash
   python app.py
   ```

5. **Test the API:**
   ```bash
   python test_mood_journal.py
   ```

## 📋 API Endpoints

### Authentication

- `POST /auth/register` - Register new user
- `POST /auth/login` - Login user

### Mood Journal

- `POST /api/v1/mood/mood` - Log daily mood
- `GET /api/v1/mood/mood` - Get mood history
- `GET /api/v1/mood/mood/stats` - Get mood analytics

### AI Recommendations

- `POST /api/v1/mood/recommend` - Get personalized suggestions
- `POST /api/v1/mood/feedback` - Rate recommendations
- `POST /api/v1/mood/chat` - Sentiment analysis and supportive guidance

### User Profile

- `GET /api/v1/mood/profile` - Get user profile
- `PUT /api/v1/mood/profile` - Update profile

## 🧹 Cleanup

If you want to remove all unnecessary files from the original codebase:

```bash
python cleanup.py
```

This will remove all skill planner related files and keep only the mood journal functionality.

## 📚 Documentation

For detailed API documentation, see [README_MOOD_JOURNAL.md](README_MOOD_JOURNAL.md).

## 🛠️ Tech Stack

- **Framework**: Flask
- **Database**: MongoDB
- **Authentication**: JWT
- **AI**: Optional integration (disabled if no API key)
- **Caching**: Redis (optional)

## 📱 Frontend Ready

This backend is designed to work with any frontend framework:

- React Native
- React/Next.js
- Flutter
- Vue.js
- Any HTTP client
