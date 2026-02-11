# Mood Journal: AI-Powered Emotional Wellness Application

## 📋 Problem Statement

In today's fast-paced world, mental health awareness and emotional well-being have become increasingly important. Many people struggle with:
- **Lack of emotional awareness**: Difficulty recognizing and tracking daily mood patterns
- **Limited coping strategies**: Not knowing what activities or resources can help improve their mood
- **Isolation**: Feeling alone in their emotional experiences without community support
- **Inconsistent tracking**: Difficulty maintaining regular mood logging habits
- **Generic recommendations**: One-size-fits-all suggestions that don't consider personal preferences and circumstances

The Mood Journal application addresses these challenges by providing a comprehensive, AI-powered platform for emotional wellness tracking and personalized recommendations.

## 🎯 Solution Overview

Mood Journal is a full-stack web and mobile application that combines mood tracking, AI-powered recommendations, and community features to support users' emotional well-being. The application provides personalized suggestions for movies, activities, music, and beverages based on users' current mood, personal preferences, and past feedback.

## 🚀 Core Features & Functionality

### 1. **User Authentication & Profiles**
- Secure JWT-based authentication system
- User registration with comprehensive profile creation
- Profile customization including age, nationality, gender, and hobbies
- Persistent login sessions with local storage

### 2. **Mood Tracking System**
- **Daily mood logging** with four primary emotions: Happy, Sad, Anxious, Excited
- **Intensity tracking** on a 1-10 scale for emotional depth
- **Contextual notes** to capture what triggered the mood
- **Calendar visualization** showing mood history over time
- **Date-specific logging** allowing users to log moods for past dates

### 3. **AI-Powered Recommendations**
- **Personalized suggestions** based on current mood and user profile
- **Multiple recommendation types**:
  - Movies and TV shows
  - Cocktails and mocktails (age-appropriate)
  - Music playlists
  - Activities and hobbies
- **Context-aware recommendations** considering what happened during the day
- **Feedback system** to improve future suggestions
- **Fallback recommendations** when AI service is unavailable

### 4. **Community Features**
- **Share recommendations** with the community
- **View community posts** from other users
- **Like and star** posts to show appreciation
- **Mood-based sharing** with context about emotional state

### 5. **Analytics & Insights**
- **Mood history visualization** through calendar interface
- **Pattern recognition** in emotional trends
- **Personalized insights** based on user behavior
- **Recommendation effectiveness tracking**

### 6. **Mobile-First Design**
- **Responsive interface** optimized for mobile devices
- **Touch-friendly interactions** with intuitive gestures
- **Offline capability** for basic mood logging
- **Cross-platform compatibility** via Lynx framework

## 🛠️ Development Tools & Technologies

### **Frontend Development**
- **Lynx Framework**: Modern React-based framework for cross-platform development
- **Rspeedy**: Build tool and development server for Lynx applications
- **TypeScript**: Type-safe JavaScript development
- **React**: Component-based UI library
- **CSS3**: Modern styling with gradients, animations, and responsive design

### **Backend Development**
- **Python 3.8+**: Core programming language
- **Flask**: Lightweight web framework for API development
- **Flask-CORS**: Cross-origin resource sharing support
- **Werkzeug**: WSGI utility library
- **Python-dotenv**: Environment variable management

### **Database & Storage**
- **MongoDB**: NoSQL database for flexible data storage
- **PyMongo**: MongoDB driver for Python
- **ObjectId**: Unique identifier system for documents

### **Authentication & Security**
- **JWT (JSON Web Tokens)**: Stateless authentication
- **PyJWT**: JWT implementation for Python
- **Bcrypt**: Password hashing and verification
- **Marshmallow**: Data serialization and validation

### **AI & External Services**
- **OpenRouter API**: AI model integration for recommendations
- **HTTPX**: Async HTTP client for API calls
- **JSON**: Data format for API communication

### **Development Environment**
- **Node.js 18+**: JavaScript runtime for frontend development
- **npm**: Package manager for Node.js dependencies
- **Git**: Version control system
- **VS Code**: Integrated development environment

## 📚 Libraries & Dependencies

### **Frontend Libraries**
```json
{
  "@lynx-js/react": "^0.112.4",
  "@lynx-js/web-elements": "^0.8.4",
  "@lynx-js/preact-devtools": "^5.0.1-6664329",
  "@lynx-js/qrcode-rsbuild-plugin": "^0.4.1",
  "@lynx-js/react-rsbuild-plugin": "^0.10.13",
  "@lynx-js/rspeedy": "^0.10.8",
  "@lynx-js/types": "3.3.0",
  "typescript": "~5.9.2",
  "vitest": "^3.2.4"
}
```

### **Backend Libraries**
```python
Flask>=2.0
Flask-Cors
python-dotenv
marshmallow
pymongo
bcrypt
PyJWT
werkzeug==2.0.2
httpx==0.27.0
redis>=4.5.0
```

### **Development Tools**
- **Biome**: Code formatting and linting
- **Prettier**: Code formatting
- **Vitest**: Unit testing framework
- **TypeScript**: Static type checking

## 🔌 APIs & External Services

### **1. OpenRouter API**
- **Purpose**: AI-powered recommendation generation
- **Integration**: Async HTTP requests for mood-based suggestions
- **Fallback**: Local recommendation templates when API unavailable
- **Rate Limiting**: Intelligent cooldown system to manage API calls

### **2. MongoDB Atlas (Production)**
- **Purpose**: Cloud database hosting
- **Collections**: users, moods, recommendations, community_posts, feedback
- **Indexing**: Optimized queries for user data and mood history

### **3. Local MongoDB (Development)**
- **Purpose**: Local development database
- **Connection**: mongodb://localhost:27017/mood_journal_db
- **Data Persistence**: Local file storage

## 🎨 Assets & Design Elements

### **Visual Assets**
- **Emoji Icons**: Mood representation (😊, 😢, 😰, 🤩)
- **Color Scheme**: 
  - Happy: #FFD700 (Gold)
  - Sad: #87CEEB (Sky Blue)
  - Anxious: #DDA0DD (Plum)
  - Excited: #FF6B6B (Coral Red)
- **Gradients**: Modern gradient backgrounds for UI elements
- **Typography**: Clean, readable fonts optimized for mobile

### **UI Components**
- **Calendar Grid**: Interactive mood tracking calendar
- **Mood Selector**: Touch-friendly emotion selection
- **Intensity Slider**: Visual intensity scale (1-10)
- **Recommendation Cards**: Rich media cards for suggestions
- **Community Feed**: Social media-style post display

### **Animations & Interactions**
- **Smooth Transitions**: CSS transitions for state changes
- **Hover Effects**: Interactive feedback on buttons and cards
- **Loading States**: Visual feedback during API calls
- **Touch Gestures**: Swipe and tap interactions

## 🏗️ Architecture & Data Flow

### **System Architecture**
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Lynx Frontend │    │  Flask Backend  │    │    MongoDB      │
│   (Port 3000)   │◄──►│   (Port 8080)   │◄──►│   (Port 27017)  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │  OpenRouter AI  │
                       │     API         │
                       └─────────────────┘
```

### **Data Models**

#### **User Model**
```javascript
{
  _id: ObjectId,
  username: String,
  email: String,
  password_hash: String,
  age: Number,
  gender: String,
  nationality: String,
  hobbies: Array,
  created_at: Date,
  updated_at: Date
}
```

#### **Mood Entry Model**
```javascript
{
  _id: ObjectId,
  user_id: ObjectId,
  mood: String,
  intensity: Number,
  description: String,
  note: String,
  date: Date,
  created_at: Date
}
```

#### **Recommendation Model**
```javascript
{
  _id: ObjectId,
  user_id: ObjectId,
  mood: String,
  activity_type: String,
  title: String,
  description: String,
  reasoning: String,
  category: String,
  created_at: Date
}
```

## 🔒 Security & Privacy

### **Authentication Security**
- **JWT Tokens**: Secure, stateless authentication
- **Password Hashing**: Bcrypt with configurable rounds
- **Token Expiration**: Automatic token refresh system
- **CORS Protection**: Configured origins for API access

### **Data Privacy**
- **User Consent**: Explicit consent for data collection
- **Data Encryption**: Sensitive data encryption at rest
- **Access Control**: User-specific data isolation
- **Audit Logging**: User action tracking for security

## 📱 Platform Support

### **Web Platform**
- **Modern Browsers**: Chrome, Firefox, Safari, Edge
- **Responsive Design**: Mobile-first approach
- **Progressive Web App**: Offline capability
- **Touch Support**: Mobile-optimized interactions

### **Mobile Platform**
- **Lynx Framework**: Cross-platform mobile development
- **Native Performance**: Optimized for mobile devices
- **QR Code Access**: Easy mobile app access
- **Push Notifications**: Mood reminder capabilities

## 🚀 Deployment & Scalability

### **Development Environment**
- **Local MongoDB**: Development database
- **Hot Reloading**: Real-time code updates
- **Debug Mode**: Enhanced error reporting
- **Environment Variables**: Configuration management

### **Production Readiness**
- **MongoDB Atlas**: Cloud database hosting
- **Load Balancing**: Horizontal scaling capability
- **Caching**: Redis integration for performance
- **Monitoring**: Health check endpoints
- **Logging**: Comprehensive error tracking

## 🎯 Impact & Benefits

### **User Benefits**
- **Emotional Awareness**: Better understanding of mood patterns
- **Coping Strategies**: Personalized recommendations for mood improvement
- **Community Support**: Connection with others experiencing similar emotions
- **Consistency**: Easy-to-use interface encourages regular tracking
- **Personalization**: AI-driven suggestions based on individual preferences

### **Technical Benefits**
- **Scalable Architecture**: Modular design for easy expansion
- **Cross-Platform**: Single codebase for web and mobile
- **AI Integration**: Intelligent recommendation system
- **Real-time Updates**: Live data synchronization
- **Offline Capability**: Basic functionality without internet

## 🔮 Future Enhancements

### **Planned Features**
- **Mood Analytics**: Advanced pattern recognition and insights
- **Social Features**: Friend connections and mood sharing
- **Integration APIs**: Calendar and health app integration
- **Voice Input**: Speech-to-text for mood logging
- **Machine Learning**: Improved recommendation algorithms

### **Technical Improvements**
- **Microservices**: Service-oriented architecture
- **GraphQL**: Efficient data fetching
- **Real-time Chat**: WebSocket integration
- **Push Notifications**: Mood reminder system
- **Data Export**: User data portability

---

**Mood Journal represents a comprehensive solution for emotional wellness tracking, combining modern web technologies, AI capabilities, and user-centered design to create a powerful tool for mental health awareness and support.**
