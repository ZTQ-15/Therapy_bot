import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class DebugConfig:
    # Database Configuration
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/mood_journal_db')
    
    # JWT Configuration
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'debug-secret-key')
    
    # AI Service Configuration
    OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY', '')
    AI_MODEL_NAME = os.getenv('AI_MODEL_NAME', 'deepseek/deepseek-r1-0528:free')
    
    # Server Configuration - Debug Mode
    PORT = int(os.getenv('PORT', 8080))
    HOST = os.getenv('HOST', '0.0.0.0')
    DEBUG = True  # Always True for debugging
    
    # CORS Configuration
    FRONTEND_URL = os.getenv('FRONTEND_URL', 'http://localhost:3003')
    ALLOWED_ORIGINS = [
        FRONTEND_URL,
        'http://localhost:3000',
        'http://localhost:3001',
        'http://localhost:3002',
        'http://localhost:3003',
        'exp://192.168.0.116:8081'
    ]
    
    # Security Configuration
    BCRYPT_ROUNDS = int(os.getenv('BCRYPT_ROUNDS', 12))
    
    # Logging Configuration - Debug Level
    LOG_LEVEL = 'DEBUG'  # Always DEBUG for debugging

# Debug configuration instance
debug_config = DebugConfig() 