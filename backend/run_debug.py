#!/usr/bin/env python3
"""
Debug runner for Flask application
This script starts the Flask app with debugging enabled and additional debug features
"""

import os
import sys
from debug_config import debug_config

# Set environment variables for debugging
os.environ['FLASK_ENV'] = 'development'
os.environ['FLASK_DEBUG'] = '1'
os.environ['DEBUG'] = 'True'

# Import and run the app with debug config
from app import create_app

def main():
    print("🚀 Starting Flask app in DEBUG mode...")
    print(f"📍 Host: {debug_config.HOST}")
    print(f"🔌 Port: {debug_config.PORT}")
    print(f"🐛 Debug: {debug_config.DEBUG}")
    print(f"📝 Log Level: {debug_config.LOG_LEVEL}")
    print("=" * 50)
    
    app = create_app()
    
    # Override config with debug settings
    app.config['DEBUG'] = True
    app.config['TESTING'] = False
    
    # Start the app
    app.run(
        host=debug_config.HOST,
        port=debug_config.PORT,
        debug=True,  # Force debug mode
        use_reloader=True,  # Auto-reload on code changes
        threaded=True  # Enable threading for better debugging
    )

if __name__ == '__main__':
    main() 