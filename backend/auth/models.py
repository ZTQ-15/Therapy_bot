from datetime import datetime, timedelta, timezone
import jwt
from flask import current_app, g
from werkzeug.exceptions import BadRequest
from bson.objectid import ObjectId

class User:
    @staticmethod
    def create(username: str, email: str, password_hash: str, age: int = None, nationality: str = None, gender: str = None, hobbies: list = None):
        user_data = {
            'username': username,
            'email': email,
            'password_hash': password_hash,
            'age': age,
            'nationality': nationality,
            'gender': gender,
            'hobbies': hobbies or [],
            'created_at': datetime.now(timezone.utc),
            'updated_at': datetime.now(timezone.utc),
            'last_login': None
        }
        result = g.db.users.insert_one(user_data)
        return str(result.inserted_id)

    @staticmethod
    def find_by_username_or_email(identifier: str):
        return g.db.users.find_one({
            '$or': [
                {'username': identifier},
                {'email': identifier}
            ]
        })

    @staticmethod
    def find_by_id(user_id: str):
        try:
            doc = g.db.users.find_one({'_id': ObjectId(user_id)})
            return doc
        except:
            return None

    @staticmethod
    def update_profile(user_id: str, update_data: dict):
        update_data['updated_at'] = datetime.now(timezone.utc)
        
        try:
            result = g.db.users.update_one(
                {'_id': ObjectId(user_id)},
                {'$set': update_data}
            )
            return result.modified_count > 0
        except Exception as e:
            print(f"Error updating profile: {e}")
            return False

    @staticmethod
    def update_last_login(user_id: str):
        g.db.users.update_one(
            {'_id': ObjectId(user_id)},
            {'$set': {'last_login': datetime.now(timezone.utc)}}
        )

    @staticmethod
    def generate_jwt_token(user_id: str):
        payload = {
            'user_id': str(user_id),
            'iat': datetime.now(timezone.utc),
            'exp': datetime.now(timezone.utc) + timedelta(days=7)
        }
        return jwt.encode(payload, current_app.config['JWT_SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_jwt_token(token: str):
        try:
            payload = jwt.decode(token, current_app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
            return payload['user_id']
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
        
        