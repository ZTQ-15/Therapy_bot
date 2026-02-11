import os
import logging
from datetime import timedelta
from dotenv import load_dotenv

# Load environment variables from .env.local first, then .env
load_dotenv('.env.local')
load_dotenv('.env')

# Configure logging to reduce MongoDB OCSP messages
logging.getLogger('pymongo.ocsp_support').setLevel(logging.WARNING)
logging.getLogger('pymongo').setLevel(logging.WARNING)

class Config:
    # Database Configuration
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/mood_journal_db')
    
    # JWT Configuration
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'your-secret-key-change-in-production')
    
    # AI Service Configuration
    API_PROVIDER = os.getenv('AI_PROVIDER', 'openai')
    AI_MODEL_NAME = os.getenv('AI_MODEL_NAME', 'gpt-4o-mini')
    API_KEY = os.getenv('API_KEY', '')
    
    # Server Configuration
    PORT = int(os.getenv('PORT', 8080))
    HOST = os.getenv('HOST', '0.0.0.0')
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
    
    # CORS Configuration
    FRONTEND_URL = os.getenv('FRONTEND_URL', 'http://localhost:3003')
    ALLOWED_ORIGINS = [
        FRONTEND_URL,
        'http://localhost:3000',
        'http://localhost:3001',
        'http://localhost:3002',
        'http://localhost:3003',
        'http://localhost:5173',
        'http://localhost:5174',
        'exp://192.168.0.116:8081'
    ]
    
    # Security Configuration
    BCRYPT_ROUNDS = int(os.getenv('BCRYPT_ROUNDS', 12))
    
    # Logging Configuration
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

# Create a development config that can be easily modified
class DevelopmentConfig(Config):
    DEBUG = True
    LOG_LEVEL = 'DEBUG'

# Create a production config
class ProductionConfig(Config):
    DEBUG = False
    LOG_LEVEL = 'WARNING'

# Default to development config
config = DevelopmentConfig()
