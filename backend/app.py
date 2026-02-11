import os
import json
from datetime import datetime
from bson import ObjectId
from flask import Flask, request, jsonify, g
from flask_cors import CORS
from pymongo import MongoClient
from config import config
import logging
import pdb  # Python debugger

# Import blueprints with proper paths
try:
    from auth.routes import auth_bp
    from api.v1.mood_journal import mood_journal_bp
    from api.v1.community import community_bp
except ImportError:
    # Fallback for when running from parent directory
    import sys
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from auth.routes import auth_bp
    from api.v1.mood_journal import mood_journal_bp
    from api.v1.community import community_bp

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, datetime):
            return o.isoformat()
        return super().default(o)

def create_app():
    app = Flask(__name__)
    app.json_encoder = CustomJSONEncoder

    # Use configuration from config.py
    app.config['JWT_SECRET_KEY'] = config.JWT_SECRET_KEY
    app.config['MONGO_URI'] = config.MONGO_URI

    # Configure CORS with allowed origins from config
    CORS(app, origins=config.ALLOWED_ORIGINS)

    @app.before_request
    def before_request():
        try:
            if 'db_client' not in g:
                mongo_uri = config.MONGO_URI
                if not mongo_uri:
                    raise ValueError("MONGO_URI environment variable not set.")
                g.db_client = MongoClient(mongo_uri)
                g.db = g.db_client.get_default_database()
        except Exception as e:
            app.logger.critical(f"Could not connect to MongoDB: {e}")
            g.db = None 

    @app.teardown_request
    def teardown_request(exception):
        db_client = g.pop('db_client', None)
        if db_client is not None:
            db_client.close()

    # Configure logging
    logging.basicConfig(level=getattr(logging, config.LOG_LEVEL))
    app.logger.setLevel(getattr(logging, config.LOG_LEVEL))

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/v1/auth')
    app.register_blueprint(mood_journal_bp, url_prefix='/api/v1/mood')
    app.register_blueprint(community_bp, url_prefix='/api/v1/community')

    @app.route('/health', methods=['GET'])
    def health_check():
        # Debugger breakpoint - uncomment the next line to pause execution here
        # pdb.set_trace()
        
        return jsonify({
            'status': 'healthy', 
            'message': 'Mood Journal API is running',
            'config': {
                'mongo_connected': g.db is not None,
                'ai_service_configured': bool(config.API_KEY),
                'debug_mode': config.DEBUG
            }
        }), 200

    return app

app = create_app()

if __name__ == '__main__':
    app.run(
        host=config.HOST, 
        port=config.PORT, 
        debug=config.DEBUG
    ) 