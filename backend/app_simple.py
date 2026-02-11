import os
import json
from datetime import datetime
from bson import ObjectId
from flask import Flask, request, jsonify, g
from flask_cors import CORS
from pymongo import MongoClient
import logging
from dotenv import load_dotenv

from auth.routes import auth_bp
from api.v1.mood_journal import mood_journal_bp

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, datetime):
            return o.isoformat()
        return super().default(o)

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.json_encoder = CustomJSONEncoder

    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your-secret-key-change-in-production')
    app.config['MONGO_URI'] = os.getenv('MONGO_URI', 'mongodb://localhost:27017/mood_journal_db')

    allowed_origins = [
        os.getenv('FRONTEND_URL', 'http://localhost:8081'),
        'http://localhost:8081',
        'http://localhost:3000',
        'exp://192.168.0.116:8081'  
    ]
    
    CORS(app, origins=allowed_origins)

    @app.before_request
    def before_request():
        try:
            if 'db_client' not in g:
                mongo_uri = os.getenv("MONGO_URI")
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

    logging.basicConfig(level=logging.INFO)
    app.logger.setLevel(logging.INFO)

    app.register_blueprint(auth_bp)

    app.register_blueprint(mood_journal_bp, url_prefix='/api/v1/mood')
    
    from api.v1.community import community_bp
    app.register_blueprint(community_bp, url_prefix='/api/v1/community')

    @app.route('/health', methods=['GET'])
    def health_check():
        return jsonify({'status': 'healthy', 'message': 'Mood Journal API is running'}), 200

    return app

app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port, debug=True) 