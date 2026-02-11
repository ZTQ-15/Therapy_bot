from datetime import datetime, timezone
from bson.objectid import ObjectId
from flask import g

class MoodEntry:
    @staticmethod
    def create(user_id: str, mood: str, intensity: int, description: str = None, note: str = None, mood_date: datetime = None, is_public: bool = False):
        """Create a new mood entry"""
        # Use provided date or UTC time to ensure consistent date handling across timezones
        if mood_date is None:
            now = datetime.now(timezone.utc)
        else:
            now = mood_date
            
        mood_data = {
            'user_id': ObjectId(user_id),
            'mood': mood.lower(),
            'intensity': intensity,  
            'description': description, 
            'note': note,
            'is_public': is_public,
            'created_at': now,
            'date': now
        }
        result = g.db.mood_entries.insert_one(mood_data)
        return str(result.inserted_id)

    @staticmethod
    def get_user_moods(user_id: str, limit: int = 30):
        """Get user's mood history"""
        cursor = g.db.mood_entries.find(
            {'user_id': ObjectId(user_id)}
        ).sort('created_at', -1).limit(limit)
        return list(cursor)

    @staticmethod
    def get_mood_by_date(user_id: str, date):
        """Get mood entry for a specific date"""
        if hasattr(date, 'date'):
            date_to_find = date.replace(hour=0, minute=0, second=0, microsecond=0)
        else:
            date_to_find = datetime.combine(date, datetime.min.time())
        
        return g.db.mood_entries.find_one({
            'user_id': ObjectId(user_id),
            'date': date_to_find
        })

    @staticmethod
    def get_mood_stats(user_id: str, days: int = 7):
        """Get mood statistics for the last N days"""
        from datetime import timedelta
        start_date = datetime.now(timezone.utc) - timedelta(days=days)
        
        pipeline = [
            {
                '$match': {
                    'user_id': ObjectId(user_id),
                    'date': {'$gte': start_date}
                }
            },
            {
                '$group': {
                    '_id': '$mood',
                    'count': {'$sum': 1},
                    'avg_intensity': {'$avg': '$intensity'}
                }
            }
        ]
        
        return list(g.db.mood_entries.aggregate(pipeline))

class Recommendation:
    @staticmethod
    def create(user_id: str, mood: str, activity_type: str, title: str, description: str, 
               url: str = None, category: str = None):
        """Create a new recommendation"""
        recommendation_data = {
            'user_id': ObjectId(user_id),
            'mood': mood.lower(),
            'activity_type': activity_type,  
            'title': title,
            'description': description,
            'url': url,
            'category': category,
            'created_at': datetime.now(timezone.utc),
            'likes': 0,
            'dislikes': 0,
            'feedback_count': 0
        }
        result = g.db.recommendations.insert_one(recommendation_data)
        return str(result.inserted_id)

    @staticmethod
    def get_recommendations_for_mood(mood: str, activity_type: str = None, limit: int = 5):
        """Get recommendations for a specific mood"""
        query = {'mood': mood.lower()}
        if activity_type:
            query['activity_type'] = activity_type
            
        cursor = g.db.recommendations.find(query).sort('likes', -1).limit(limit)
        return list(cursor)

    @staticmethod
    def get_by_id(recommendation_id: str):
        """Get a recommendation by ID"""
        try:
            return g.db.recommendations.find_one({'_id': ObjectId(recommendation_id)})
        except:
            return None

    @staticmethod
    def add_feedback(recommendation_id: str, liked: bool):
        """Add user feedback to a recommendation"""
        update_data = {
            '$inc': {
                'feedback_count': 1
            }
        }
        
        if liked:
            update_data['$inc']['likes'] = 1
        else:
            update_data['$inc']['dislikes'] = 1
            
        g.db.recommendations.update_one(
            {'_id': ObjectId(recommendation_id)},
            update_data
        )

    @staticmethod
    def get_user_feedback_history(user_id: str):
        """Get user's feedback history"""
        return list(g.db.user_feedback.find({'user_id': ObjectId(user_id)}))

class UserFeedback:
    @staticmethod
    def create(user_id: str, recommendation_id: str, liked: bool, mood: str):
        """Create user feedback record"""
        feedback_data = {
            'user_id': ObjectId(user_id),
            'recommendation_id': ObjectId(recommendation_id),
            'liked': liked,
            'mood': mood.lower(),
            'created_at': datetime.now(timezone.utc)
        }
        result = g.db.user_feedback.insert_one(feedback_data)
        return str(result.inserted_id) 