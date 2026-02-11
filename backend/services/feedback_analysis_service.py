import logging
from typing import Dict, Any, List
from models.mood_journal import UserFeedback, Recommendation

class FeedbackAnalysisService:
    
    @staticmethod
    def get_user_insights(user_id: str) -> Dict[str, Any]:
        """Get insights about user's feedback patterns"""
        try:
            # Get user's feedback history
            feedback_history = Recommendation.get_user_feedback_history(user_id)
            
            if not feedback_history:
                return {
                    "total_feedback": 0,
                    "like_ratio": 0,
                    "favorite_moods": [],
                    "least_favorite_moods": [],
                    "recommendations": []
                }
            
            # Analyze feedback patterns
            mood_feedback = {}
            type_feedback = {}
            liked_count = 0
            
            for feedback in feedback_history:
                mood = feedback.get('mood', '')
                liked = feedback.get('liked', False)
                
                if liked:
                    liked_count += 1
                
                # Track mood preferences
                if mood not in mood_feedback:
                    mood_feedback[mood] = {'liked': 0, 'disliked': 0}
                
                if liked:
                    mood_feedback[mood]['liked'] += 1
                else:
                    mood_feedback[mood]['disliked'] += 1
                
                # Track recommendation type preferences
                rec = Recommendation.get_by_id(str(feedback.get('recommendation_id')))
                if rec:
                    rec_type = rec.get('activity_type', '')
                    if rec_type not in type_feedback:
                        type_feedback[rec_type] = {'liked': 0, 'disliked': 0}
                    
                    if liked:
                        type_feedback[rec_type]['liked'] += 1
                    else:
                        type_feedback[rec_type]['disliked'] += 1
            
            # Calculate insights
            total_feedback = len(feedback_history)
            like_ratio = liked_count / total_feedback if total_feedback > 0 else 0
            
            # Find favorite and least favorite moods
            favorite_moods = []
            least_favorite_moods = []
            
            for mood, stats in mood_feedback.items():
                total_mood_feedback = stats['liked'] + stats['disliked']
                if total_mood_feedback >= 2:  # Only consider moods with multiple feedback
                    mood_ratio = stats['liked'] / total_mood_feedback
                    if mood_ratio >= 0.7:  # 70% or higher like ratio
                        favorite_moods.append(mood)
                    elif mood_ratio <= 0.3:  # 30% or lower like ratio
                        least_favorite_moods.append(mood)
            
            # Generate recommendations
            recommendations = []
            
            if like_ratio < 0.5:
                recommendations.append("Consider providing more diverse recommendation types")
            
            if favorite_moods:
                recommendations.append(f"User tends to like recommendations when feeling: {', '.join(favorite_moods)}")
            
            if least_favorite_moods:
                recommendations.append(f"User tends to dislike recommendations when feeling: {', '.join(least_favorite_moods)}")
            
            # Find best performing recommendation types
            best_types = []
            for rec_type, stats in type_feedback.items():
                total_type_feedback = stats['liked'] + stats['disliked']
                if total_type_feedback >= 2:
                    type_ratio = stats['liked'] / total_type_feedback
                    if type_ratio >= 0.6:
                        best_types.append(rec_type)
            
            if best_types:
                recommendations.append(f"User prefers these types: {', '.join(best_types)}")
            
            return {
                "total_feedback": total_feedback,
                "like_ratio": round(like_ratio, 2),
                "favorite_moods": favorite_moods,
                "least_favorite_moods": least_favorite_moods,
                "best_recommendation_types": best_types,
                "recommendations": recommendations,
                "mood_breakdown": mood_feedback,
                "type_breakdown": type_feedback
            }
            
        except Exception as e:
            logging.error(f"Error getting user insights: {e}")
            return {
                "total_feedback": 0,
                "like_ratio": 0,
                "favorite_moods": [],
                "least_favorite_moods": [],
                "recommendations": ["Unable to analyze feedback at this time"]
            }
    
    @staticmethod
    def get_user_preferences(user_id: str) -> Dict[str, Any]:
        """Get user's recommendation preferences based on feedback"""
        try:
            insights = FeedbackAnalysisService.get_user_insights(user_id)
            
            preferences = {
                "preferred_moods": insights.get('favorite_moods', []),
                "avoided_moods": insights.get('least_favorite_moods', []),
                "preferred_types": insights.get('best_recommendation_types', []),
                "overall_satisfaction": insights.get('like_ratio', 0)
            }
            
            return preferences
            
        except Exception as e:
            logging.error(f"Error getting user preferences: {e}")
            return {
                "preferred_moods": [],
                "avoided_moods": [],
                "preferred_types": [],
                "overall_satisfaction": 0
            } 