from flask import Blueprint, request, jsonify, g
from datetime import datetime, date, timezone
from auth.models import User
from models.mood_journal import MoodEntry, Recommendation, UserFeedback
from services.mood_ai_service import MoodAIService
import asyncio
import logging

mood_journal_bp = Blueprint('mood_journal', __name__)

@mood_journal_bp.route('/mood', methods=['POST'])
def log_mood():
    """Log a new mood entry"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        # Get user from JWT token
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({"error": "Authorization header required"}), 401
        
        token = auth_header.split(' ')[1]
        user_id = User.verify_jwt_token(token)
        if not user_id:
            return jsonify({"error": "Invalid or expired token"}), 401
        
        # Validate required fields
        mood = data.get('mood', '').strip()
        intensity = data.get('intensity')
        description = data.get('description', '').strip()
        note = data.get('note', '').strip()
        is_public = data.get('is_public', False)
        
        # Get optional date parameter (for logging moods on specific dates)
        mood_date = data.get('date')
        if mood_date:
            try:
                # Parse the date string from frontend
                mood_date = datetime.fromisoformat(mood_date.replace('Z', '+00:00'))
            except ValueError:
                return jsonify({"error": "Invalid date format"}), 400
        else:
            # Use current UTC time if no date provided
            mood_date = datetime.now(timezone.utc)

        # Prevent logging for future dates
        today_utc = datetime.now(timezone.utc).date()
        if mood_date.date() > today_utc:
            return jsonify({"error": "Cannot log mood entries for future dates"}), 400
        
        if not mood:
            return jsonify({"error": "mood is required"}), 400
        
        if intensity is None or not isinstance(intensity, int) or intensity < 1 or intensity > 10:
            return jsonify({"error": "intensity must be an integer between 1-10"}), 400

        if not isinstance(is_public, bool):
            return jsonify({"error": "is_public must be a boolean"}), 400
        
        # Create mood entry (allow multiple moods per day)
        mood_id = MoodEntry.create(user_id, mood, intensity, description, note, mood_date, is_public)

        # Optionally share to community feed
        if is_public:
            from models.community_posts import CommunityPost
            CommunityPost.create(
                user_id=user_id,
                mood=mood,
                activity_title="Mood Journal Entry",
                activity_description=description or "Shared a mood journal entry",
                activity_type="mood_journal",
                mood_intensity=intensity,
                description=description,
                note=note,
                is_public=True,
                source_type="mood_entry",
                mood_entry_id=mood_id
            )
        
        return jsonify({
            "message": "Mood logged successfully",
            "mood_id": mood_id,
            "mood": mood,
            "intensity": intensity,
            "description": description,
            "date": mood_date.isoformat(),
            "is_public": is_public
        }), 201
        
    except Exception as e:
        logging.error(f"Error logging mood: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@mood_journal_bp.route('/mood', methods=['GET'])
def get_mood_history():
    """Get user's mood history"""
    try:
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({"error": "Authorization header required"}), 401
        
        token = auth_header.split(' ')[1]
        user_id = User.verify_jwt_token(token)
        if not user_id:
            return jsonify({"error": "Invalid or expired token"}), 401
        
        limit = request.args.get('limit', 30, type=int)
        if limit > 100:
            limit = 100
        
        moods = MoodEntry.get_user_moods(user_id, limit)
        
        for mood in moods:
            mood['_id'] = str(mood['_id'])
            mood['user_id'] = str(mood['user_id'])
            mood['created_at'] = mood['created_at'].isoformat()
            mood['date'] = mood['date'].isoformat()
        
        return jsonify({
            "moods": moods,
            "count": len(moods)
        }), 200
        
    except Exception as e:
        logging.error(f"Error getting mood history: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@mood_journal_bp.route('/mood/stats', methods=['GET'])
def get_mood_stats():
    """Get mood statistics"""
    try:
        # Get user from JWT token
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({"error": "Authorization header required"}), 401
        
        token = auth_header.split(' ')[1]
        user_id = User.verify_jwt_token(token)
        if not user_id:
            return jsonify({"error": "Invalid or expired token"}), 401
        
        # Get query parameters
        days = request.args.get('days', 7, type=int)
        if days > 30:
            days = 30
        
        # Get mood statistics
        stats = MoodEntry.get_mood_stats(user_id, days)
        
        return jsonify({
            "stats": stats,
            "period_days": days
        }), 200
        
    except Exception as e:
        logging.error(f"Error getting mood stats: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@mood_journal_bp.route('/recommend', methods=['POST'])
def get_recommendation():
    """Get AI recommendation based on mood"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({"error": "Authorization header required"}), 401
        
        token = auth_header.split(' ')[1]
        user_id = User.verify_jwt_token(token)
        if not user_id:
            return jsonify({"error": "Invalid or expired token"}), 401
        
        user = User.find_by_id(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        mood = data.get('mood', '').strip()
        description = data.get('description', '').strip()
        activity_type = data.get('activity_type', '').strip() or None
        
        if not mood:
            return jsonify({"error": "mood is required"}), 400
        
        user_profile = {
            'age': user.get('age'),
            'gender': user.get('gender'),
            'nationality': user.get('nationality'),
            'hobbies': user.get('hobbies', [])
        }
        
        recommendation_data = asyncio.run(
            MoodAIService.generate_mood_recommendation(mood, user_profile, description, activity_type)
        )
        
        main_rec = recommendation_data['recommendation']
        rec_id = Recommendation.create(
            user_id=user_id,
            mood=mood,
            activity_type=main_rec['type'],
            title=main_rec['title'],
            description=main_rec['description'],
            url=main_rec.get('url'),
            category=main_rec.get('category')
        )
        
        recommendation_data['recommendation']['id'] = rec_id
        
        return jsonify(recommendation_data), 200
        
    except Exception as e:
        logging.error(f"Error getting recommendation: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@mood_journal_bp.route('/chat', methods=['POST'])
def chat_support():
    """Sentiment analysis and supportive guidance"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400

        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({"error": "Authorization header required"}), 401

        token = auth_header.split(' ')[1]
        user_id = User.verify_jwt_token(token)
        if not user_id:
            return jsonify({"error": "Invalid or expired token"}), 401

        entry_text = data.get('entry_text', '').strip()
        mood = data.get('mood', '').strip()
        if not entry_text:
            return jsonify({"error": "entry_text is required"}), 400

        analysis = asyncio.run(
            MoodAIService.analyze_sentiment_and_counseling(entry_text, mood)
        )

        return jsonify(analysis), 200

    except Exception as e:
        logging.error(f"Error running chat support: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@mood_journal_bp.route('/feedback', methods=['POST'])
def submit_feedback():
    """Submit feedback for a recommendation"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        # Get user from JWT token
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({"error": "Authorization header required"}), 401
        
        token = auth_header.split(' ')[1]
        user_id = User.verify_jwt_token(token)
        if not user_id:
            return jsonify({"error": "Invalid or expired token"}), 401
        
        # Validate required fields
        recommendation_id = data.get('recommendation_id', '').strip()
        liked = data.get('liked')
        mood = data.get('mood', '').strip()
        
        if not recommendation_id:
            return jsonify({"error": "recommendation_id is required"}), 400
        
        if liked is None or not isinstance(liked, bool):
            return jsonify({"error": "liked must be a boolean"}), 400
        
        # Update recommendation feedback
        Recommendation.add_feedback(recommendation_id, liked)
        
        # Create user feedback record
        feedback_id = UserFeedback.create(user_id, recommendation_id, liked, mood)
        
        return jsonify({
            "message": "Feedback submitted successfully",
            "feedback_id": feedback_id,
            "liked": liked
        }), 201
        
    except Exception as e:
        logging.error(f"Error submitting feedback: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@mood_journal_bp.route('/profile', methods=['GET'])
def get_profile():
    """Get user profile"""
    try:
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({"error": "Authorization header required"}), 401
        
        token = auth_header.split(' ')[1]
        user_id = User.verify_jwt_token(token)
        if not user_id:
            return jsonify({"error": "Invalid or expired token"}), 401
        
        user = User.find_by_id(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        profile_data = {
            "username": user.get('username'),
            "email": user.get('email'),
            "age": user.get('age'),
            "gender": user.get('gender'),
            "nationality": user.get('nationality'),
            "hobbies": user.get('hobbies', []),
            "created_at": user.get('created_at').isoformat() if user.get('created_at') else None
        }
        
        return jsonify(profile_data), 200
        
    except Exception as e:
        logging.error(f"Error getting profile: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@mood_journal_bp.route('/profile', methods=['PUT'])
def update_profile():
    """Update user profile"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        # Get user from JWT token
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({"error": "Authorization header required"}), 401
        
        token = auth_header.split(' ')[1]
        user_id = User.verify_jwt_token(token)
        if not user_id:
            return jsonify({"error": "Invalid or expired token"}), 401
        
        # Validate and extract fields
        age = data.get('age')
        nationality = data.get('nationality', '').strip()
        gender = data.get('gender', '').strip()
        hobbies = data.get('hobbies', [])
        
        # Validate age
        if age is not None and (not isinstance(age, int) or age < 1 or age > 120):
            return jsonify({"error": "age must be an integer between 1-120"}), 400
        
        # Validate hobbies
        if not isinstance(hobbies, list):
            return jsonify({"error": "hobbies must be a list"}), 400
        
        # Update profile
        User.update_profile(user_id, age, nationality, gender, hobbies)
        
        return jsonify({
            "message": "Profile updated successfully",
            "updated_fields": [k for k, v in data.items() if v is not None]
        }), 200
        
    except Exception as e:
        logging.error(f"Error updating profile: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500 

@mood_journal_bp.route('/insights', methods=['GET'])
def get_user_insights():
    """Get user insights and feedback analysis"""
    try:
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({"error": "Authorization header required"}), 401
        
        token = auth_header.split(' ')[1]
        user_id = User.verify_jwt_token(token)
        if not user_id:
            return jsonify({"error": "Invalid or expired token"}), 401
        
        try:
            from services.feedback_analysis_service import FeedbackAnalysisService
            insights = FeedbackAnalysisService.get_user_insights(user_id)
            preferences = FeedbackAnalysisService.get_user_preferences(user_id)
            
            return jsonify({
                "insights": insights,
                "preferences": preferences
            }), 200
        except ImportError:
            return jsonify({
                "message": "Feedback analysis service not available",
                "insights": {},
                "preferences": {}
            }), 200
        
    except Exception as e:
        logging.error(f"Error getting user insights: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500 

@mood_journal_bp.route('/share', methods=['POST'])
def share_recommendation():
    """Share a recommendation to the community"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        # Get user from JWT token
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({"error": "Authorization header required"}), 401
        
        token = auth_header.split(' ')[1]
        user_id = User.verify_jwt_token(token)
        if not user_id:
            return jsonify({"error": "Invalid or expired token"}), 401
        
        # Validate required fields
        recommendation_id = data.get('recommendation_id')
        mood = data.get('mood', '').strip()
        mood_intensity = data.get('mood_intensity')
        description = data.get('description', '').strip()
        
        if not recommendation_id:
            return jsonify({"error": "recommendation_id is required"}), 400
        
        if not mood:
            return jsonify({"error": "mood is required"}), 400
        
        if mood_intensity is None or not isinstance(mood_intensity, int) or mood_intensity < 1 or mood_intensity > 10:
            return jsonify({"error": "mood_intensity must be an integer between 1-10"}), 400
        
        # Get the recommendation details
        recommendation = Recommendation.get_by_id(recommendation_id)
        if not recommendation:
            return jsonify({"error": "Recommendation not found"}), 404
        
        # Import CommunityPost here to avoid circular imports
        from models.community_posts import CommunityPost
        
        # Create a community post from the recommendation
        post_id = CommunityPost.create(
            user_id=user_id,
            mood=mood,
            activity_title=recommendation.get('title', 'Shared Recommendation'),
            activity_description=recommendation.get('description', ''),
            activity_type=recommendation.get('type', 'recommendation'),
            mood_intensity=mood_intensity,
            description=description,
            note=f"Shared from mood journal - {recommendation.get('reasoning', '')}",
            is_public=True
        )
        
        return jsonify({
            "message": "Recommendation shared successfully",
            "post_id": post_id
        }), 201
        
    except Exception as e:
        logging.error(f"Error sharing recommendation: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@mood_journal_bp.route('/share-ai-recommendation', methods=['POST'])
def share_ai_recommendation():
    """Share an AI-generated recommendation to the community"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        # Get user from JWT token
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({"error": "Authorization header required"}), 401
        
        token = auth_header.split(' ')[1]
        user_id = User.verify_jwt_token(token)
        if not user_id:
            return jsonify({"error": "Invalid or expired token"}), 401
        
        # Validate required fields for AI recommendations
        recommendation_title = data.get('recommendation_title', '').strip()
        recommendation_type = data.get('recommendation_type', '').strip()
        recommendation_description = data.get('recommendation_description', '').strip()
        mood_data = data.get('mood_data', {})
        description = data.get('description', '').strip()
        
        if not recommendation_title:
            return jsonify({"error": "recommendation_title is required"}), 400
        
        if not mood_data or not mood_data.get('mood'):
            return jsonify({"error": "mood_data with mood is required"}), 400
        
        mood = mood_data.get('mood', '').strip()
        mood_intensity = mood_data.get('intensity', 5)  # Default to 5 if not provided
        
        # Import CommunityPost here to avoid circular imports
        from models.community_posts import CommunityPost
        
        # Create a community post from the AI recommendation
        post_id = CommunityPost.create(
            user_id=user_id,
            mood=mood,
            activity_title=recommendation_title,
            activity_description=recommendation_description,
            activity_type=recommendation_type or 'recommendation',
            mood_intensity=mood_intensity,
            description=description,
            note=f"Shared AI recommendation - {recommendation_description}",
            is_public=True
        )
        
        return jsonify({
            "message": "AI recommendation shared successfully",
            "post_id": post_id,
            "recommendation_title": recommendation_title
        }), 201
        
    except Exception as e:
        logging.error(f"Error sharing AI recommendation: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@mood_journal_bp.route('/recommendation/feedback', methods=['POST'])
def submit_recommendation_feedback():
    """Submit like/dislike feedback for a recommendation"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        # Get user from JWT token
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({"error": "Authorization header required"}), 401
        
        token = auth_header.split(' ')[1]
        user_id = User.verify_jwt_token(token)
        if not user_id:
            return jsonify({"error": "Invalid or expired token"}), 401
        
        # Validate required fields
        recommendation_id = data.get('recommendation_id')
        liked = data.get('liked')  # True for like, False for dislike
        mood = data.get('mood', '').strip()
        
        if not recommendation_id:
            return jsonify({"error": "recommendation_id is required"}), 400
        
        if liked is None:
            return jsonify({"error": "liked field is required (true/false)"}), 400
        
        if not mood:
            return jsonify({"error": "mood is required"}), 400
        
        # Check if recommendation exists
        recommendation = Recommendation.get_by_id(recommendation_id)
        if not recommendation:
            return jsonify({"error": "Recommendation not found"}), 404
        
        # Add feedback to recommendation
        Recommendation.add_feedback(recommendation_id, liked)
        
        # Create user feedback record
        feedback_id = UserFeedback.create(user_id, recommendation_id, liked, mood)
        
        return jsonify({
            "message": "Feedback submitted successfully",
            "feedback_id": feedback_id,
            "liked": liked
        }), 201
        
    except Exception as e:
        logging.error(f"Error submitting recommendation feedback: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@mood_journal_bp.route('/ai-recommendation/feedback', methods=['POST'])
def submit_ai_recommendation_feedback():
    """Submit like/dislike feedback for AI-generated recommendations"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        # Get user from JWT token
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({"error": "Authorization header required"}), 401
        
        token = auth_header.split(' ')[1]
        user_id = User.verify_jwt_token(token)
        if not user_id:
            return jsonify({"error": "Invalid or expired token"}), 401
        
        # Validate required fields
        recommendation_title = data.get('recommendation_title', '').strip()
        recommendation_type = data.get('recommendation_type', '').strip()
        recommendation_description = data.get('recommendation_description', '').strip()
        liked = data.get('liked')  # True for like, False for dislike
        mood = data.get('mood', '').strip()
        
        if not recommendation_title:
            return jsonify({"error": "recommendation_title is required"}), 400
        
        if liked is None:
            return jsonify({"error": "liked field is required (true/false)"}), 400
        
        if not mood:
            return jsonify({"error": "mood is required"}), 400
        
        # For AI recommendations, we'll store the feedback in a simple way
        # You could extend this to store in a separate collection for AI feedback
        feedback_data = {
            'user_id': user_id,
            'recommendation_title': recommendation_title,
            'recommendation_type': recommendation_type,
            'recommendation_description': recommendation_description,
            'liked': liked,
            'mood': mood,
            'created_at': datetime.now(),
            'is_ai_recommendation': True
        }
        
        # For now, just log the feedback (you could store it in a database later)
        logging.info(f"AI Recommendation Feedback: {feedback_data}")
        
        return jsonify({
            "message": "AI recommendation feedback submitted successfully",
            "liked": liked,
            "recommendation_title": recommendation_title
        }), 201
        
    except Exception as e:
        logging.error(f"Error submitting AI recommendation feedback: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@mood_journal_bp.route('/recommendation/feedback/history', methods=['GET'])
def get_feedback_history():
    """Get user's feedback history"""
    try:
        # Get user from JWT token
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({"error": "Authorization header required"}), 401
        
        token = auth_header.split(' ')[1]
        user_id = User.verify_jwt_token(token)
        if not user_id:
            return jsonify({"error": "Invalid or expired token"}), 401
        
        # Get feedback history
        feedback_history = Recommendation.get_user_feedback_history(user_id)
        
        # Convert ObjectIds to strings
        for feedback in feedback_history:
            feedback['_id'] = str(feedback['_id'])
            feedback['user_id'] = str(feedback['user_id'])
            feedback['recommendation_id'] = str(feedback['recommendation_id'])
            feedback['created_at'] = feedback['created_at'].isoformat()
        
        return jsonify({
            "feedback_history": feedback_history,
            "count": len(feedback_history)
        }), 200
        
    except Exception as e:
        logging.error(f"Error getting feedback history: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500 