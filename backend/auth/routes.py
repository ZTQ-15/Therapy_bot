from flask import Blueprint, request, jsonify, current_app, g
from werkzeug.exceptions import BadRequest
from functools import wraps
import jwt
from auth.models import User
from auth.utils import hash_password, verify_password

auth_bp = Blueprint("auth_bp", __name__)

def require_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers and request.headers['Authorization'].startswith('Bearer '):
            token = request.headers['Authorization'].split(' ')[1]

        if not token:
            return jsonify({'error': 'Authentication token is missing!'}), 401

        try:
            user_id = User.verify_jwt_token(token)
            if not user_id:
                return jsonify({'error': 'Invalid or expired token!'}), 401
            
            user = User.find_by_id(user_id)
            if not user:
                return jsonify({'error': 'User not found!'}), 401

            g.current_user = user
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token!'}), 401

        return f(*args, **kwargs)
    return decorated_function

@auth_bp.route("/register", methods=["POST"])
def register():
    try:
        data = request.get_json() or {}
        current_app.logger.info(f"Registration attempt with data: {data}")
        
        username = data.get("username", "").strip()
        email = data.get("email", "").strip()
        password = data.get("password", "")
        age = data.get("age")
        nationality = data.get("nationality", "").strip()
        gender = data.get("gender", "").strip()
        hobbies = data.get("hobbies", [])

        current_app.logger.info(f"Parsed data - username: '{username}', email: '{email}', password length: {len(password)}, age: {age}, nationality: '{nationality}', gender: '{gender}', hobbies: {hobbies}")

        if not all([username, email, password]):
            current_app.logger.error(f"Missing required fields - username: '{username}', email: '{email}', password: '{password}'")
            return jsonify({'error': 'Username, email, and password are required'}), 400
        if len(password) < 6:
            current_app.logger.error(f"Password too short: {len(password)} characters")
            return jsonify({'error': 'Password must be at least 6 characters'}), 400
        if User.find_by_username_or_email(username) or User.find_by_username_or_email(email):
            current_app.logger.error(f"Username or email already exists: {username}, {email}")
            return jsonify({'error': 'Username or email already exists'}), 409
        
        if age is not None and (not isinstance(age, int) or age < 1 or age > 120):
            current_app.logger.error(f"Invalid age: {age} (type: {type(age)})")
            return jsonify({'error': 'Age must be an integer between 1-120'}), 400
        
        if not isinstance(hobbies, list):
            current_app.logger.error(f"Invalid hobbies type: {type(hobbies)}")
            return jsonify({'error': 'Hobbies must be a list'}), 400
        
        pw_hash = hash_password(password)
        user_id = User.create(username, email, pw_hash, age, nationality, gender, hobbies)
        token = User.generate_jwt_token(user_id)
        current_app.logger.info(f"User created successfully: {user_id}")
        return jsonify({
            'message': 'User created successfully',
            'token': token,
            'user': {
                'id': user_id,
                'username': username,
                'email': email,
                'age': age,
                'nationality': nationality,
                'gender': gender,
                'hobbies': hobbies
            }
        }), 201
    except Exception as e:
        current_app.logger.error(f"Registration error: {str(e)}")
        return jsonify({'error': 'Registration failed'}), 500

@auth_bp.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json() or {}
        identifier = data.get("identifier", "").strip()
        password = data.get("password", "")
        if not all([identifier, password]):
            return jsonify({'error': 'All fields are required'}), 400
        user_doc = User.find_by_username_or_email(identifier)
        if not user_doc or not verify_password(password, user_doc["password_hash"]):
            return jsonify({'error': 'Invalid credentials'}), 401
        User.update_last_login(user_doc['_id'])
        token = User.generate_jwt_token(str(user_doc['_id']))
        user_safe = {
            'id': str(user_doc['_id']),
            'username': user_doc['username'],
            'email': user_doc['email'],
            'age': user_doc.get('age', 25),
            'nationality': user_doc.get('nationality', 'Unknown'),
            'gender': user_doc.get('gender', 'Prefer not to say'),
            'hobbies': user_doc.get('hobbies', ['reading', 'music'])
        }
        return jsonify({'message': 'Login successful', 'token': token, 'user': user_safe}), 200
    except Exception as e:
        current_app.logger.error(f"Login error: {str(e)}")
        return jsonify({'error': 'Login failed'}), 500

@auth_bp.route("/profile", methods=["PUT"])
@require_auth
def update_profile():
    try:
        data = request.get_json() or {}
        current_app.logger.info(f"Profile update attempt for user {g.current_user['_id']} with data: {data}")
        
        username = data.get("username", "").strip()
        age = data.get("age", 25)
        nationality = data.get("nationality", "").strip()
        gender = data.get("gender", "").strip()
        hobbies = data.get("hobbies", [])

        if not username:
            return jsonify({'error': 'Username is required'}), 400
        
        if age is not None and (not isinstance(age, int) or age < 1 or age > 120):
            return jsonify({'error': 'Age must be an integer between 1-120'}), 400
        
        if not isinstance(hobbies, list):
            return jsonify({'error': 'Hobbies must be a list'}), 400

        # Check if username is already taken by another user
        existing_user = User.find_by_username_or_email(username)
        if existing_user and existing_user['_id'] != g.current_user['_id']:
            return jsonify({'error': 'Username already exists'}), 409

        # Update user profile
        update_data = {
            'username': username,
            'age': age,
            'nationality': nationality,
            'gender': gender,
            'hobbies': hobbies
        }
        
        success = User.update_profile(g.current_user['_id'], update_data)
        if not success:
            return jsonify({'error': 'Failed to update profile'}), 500

        current_app.logger.info(f"Profile updated successfully for user {g.current_user['_id']}")
        return jsonify({
            'message': 'Profile updated successfully',
            'user': {
                'id': str(g.current_user['_id']),
                'username': username,
                'email': g.current_user['email'],
                'age': g.current_user.get('age', 25),
                'nationality': nationality,
                'gender': gender,
                'hobbies': hobbies
            }
        }), 200
    except Exception as e:
        current_app.logger.error(f"Profile update error: {str(e)}")
        return jsonify({'error': 'Profile update failed'}), 500

@auth_bp.route("/profile", methods=["GET"])
@require_auth
def get_profile():
    """Get user profile data"""
    try:
        current_app.logger.info(f"Profile retrieval request for user {g.current_user['_id']}")
        
        return jsonify({
            'message': 'Profile retrieved successfully',
            'user': {
                'id': str(g.current_user['_id']),
                'username': g.current_user['username'],
                'email': g.current_user['email'],
                'age': g.current_user.get('age', 25),
                'nationality': g.current_user.get('nationality', 'Unknown'),
                'gender': g.current_user.get('gender', 'Prefer not to say'),
                'hobbies': g.current_user.get('hobbies', ['reading', 'music'])
            }
        }), 200
    except Exception as e:
        current_app.logger.error(f"Profile retrieval error: {str(e)}")
        return jsonify({'error': 'Profile retrieval failed'}), 500

@auth_bp.route("/verify", methods=["POST"])
def verify_token():
    try:
        data = request.get_json() or {}
        token = data.get('token')
        if not token:
            return jsonify({'error': 'Token required'}), 400
        user_id = User.verify_jwt_token(token)
        if not user_id:
            return jsonify({'error': 'Invalid or expired token'}), 401
        user = User.find_by_id(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        return jsonify({
            'valid': True,
            'user': {
                'id': str(user['_id']),
                'username': user['username'],
                'email': user['email']
            }
        }), 200
    except Exception as e:
        current_app.logger.error(f"Token verification error: {str(e)}")
        return jsonify({'error': 'Token verification failed'}), 500
    