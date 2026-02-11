from datetime import datetime
from bson import ObjectId
from flask import g

class CommunityPost:
    @staticmethod
    def create(user_id: str, mood: str, activity_title: str, activity_description: str, 
               activity_type: str, mood_intensity: int, description: str = None, note: str = None,
               is_public: bool = True, source_type: str = None, mood_entry_id: str = None):
        """Create a new community post"""
        post_data = {
            'user_id': ObjectId(user_id),
            'mood': mood.lower(),
            'activity_title': activity_title,
            'activity_description': activity_description,
            'activity_type': activity_type,  
            'mood_intensity': mood_intensity,
            'description': description,  
            'note': note,
            'is_public': is_public,
            'source_type': source_type,
            'mood_entry_id': ObjectId(mood_entry_id) if mood_entry_id else None,
            'created_at': datetime.utcnow(),
            'likes': 0,
            'stars': 0,
            'comments_count': 0,
            'user_username': None  
        }
        
        user = g.db.users.find_one({'_id': ObjectId(user_id)})
        if user:
            post_data['user_username'] = user.get('username', 'Anonymous')
        
        result = g.db.community_posts.insert_one(post_data)
        return str(result.inserted_id)

    @staticmethod
    def get_posts(limit: int = 20, skip: int = 0, mood_filter: str = None, activity_type_filter: str = None):
        """Get community posts with optional filters"""
        query = {'is_public': True}
        
        if mood_filter:
            query['mood'] = mood_filter.lower()
        
        if activity_type_filter:
            query['activity_type'] = activity_type_filter
        
        cursor = g.db.community_posts.find(query).sort('created_at', -1).skip(skip).limit(limit)
        return list(cursor)

    @staticmethod
    def get_user_posts(user_id: str, limit: int = 20):
        """Get posts by a specific user"""
        cursor = g.db.community_posts.find({
            'user_id': ObjectId(user_id)
        }).sort('created_at', -1).limit(limit)
        return list(cursor)

    @staticmethod
    def get_post_by_id(post_id: str):
        """Get a specific post by ID"""
        return g.db.community_posts.find_one({'_id': ObjectId(post_id)})

    @staticmethod
    def like_post(post_id: str, user_id: str):
        """Like a post"""
        
        existing_like = g.db.post_likes.find_one({
            'post_id': ObjectId(post_id),
            'user_id': ObjectId(user_id)
        })
        
        if existing_like:
            return False  
        
        
        g.db.post_likes.insert_one({
            'post_id': ObjectId(post_id),
            'user_id': ObjectId(user_id),
            'created_at': datetime.utcnow()
        })
        
        
        g.db.community_posts.update_one(
            {'_id': ObjectId(post_id)},
            {'$inc': {'likes': 1}}
        )
        
        return True

    @staticmethod
    def unlike_post(post_id: str, user_id: str):
        """Unlike a post"""
        result = g.db.post_likes.delete_one({
            'post_id': ObjectId(post_id),
            'user_id': ObjectId(user_id)
        })
        
        if result.deleted_count > 0:
            g.db.community_posts.update_one(
                {'_id': ObjectId(post_id)},
                {'$inc': {'likes': -1}}
            )
            return True
        
        return False

    @staticmethod
    def star_post(post_id: str, user_id: str):
        """Star a post (bookmark/favorite)"""
        
        existing_star = g.db.post_stars.find_one({
            'post_id': ObjectId(post_id),
            'user_id': ObjectId(user_id)
        })
        
        if existing_star:
            return False 
        
        
        g.db.post_stars.insert_one({
            'post_id': ObjectId(post_id),
            'user_id': ObjectId(user_id),
            'created_at': datetime.utcnow()
        })
        
        
        g.db.community_posts.update_one(
            {'_id': ObjectId(post_id)},
            {'$inc': {'stars': 1}}
        )
        
        return True

    @staticmethod
    def unstar_post(post_id: str, user_id: str):
        """Unstar a post"""
        result = g.db.post_stars.delete_one({
            'post_id': ObjectId(post_id),
            'user_id': ObjectId(user_id)
        })
        
        if result.deleted_count > 0:
            g.db.community_posts.update_one(
                {'_id': ObjectId(post_id)},
                {'$inc': {'stars': -1}}
            )
            return True
        
        return False

    @staticmethod
    def get_user_liked_posts(user_id: str, limit: int = 20):
        """Get posts that a user has liked"""
        liked_post_ids = g.db.post_likes.find({'user_id': ObjectId(user_id)}).distinct('post_id')
        
        if not liked_post_ids:
            return []
        
        cursor = g.db.community_posts.find({
            '_id': {'$in': liked_post_ids}
        }).sort('created_at', -1).limit(limit)
        
        return list(cursor)

    @staticmethod
    def get_user_starred_posts(user_id: str, limit: int = 20):
        """Get posts that a user has starred"""
        starred_post_ids = g.db.post_stars.find({'user_id': ObjectId(user_id)}).distinct('post_id')
        
        if not starred_post_ids:
            return []
        
        cursor = g.db.community_posts.find({
            '_id': {'$in': starred_post_ids}
        }).sort('created_at', -1).limit(limit)
        
        return list(cursor)

    @staticmethod
    def is_post_liked_by_user(post_id: str, user_id: str):
        """Check if a user has liked a specific post"""
        like = g.db.post_likes.find_one({
            'post_id': ObjectId(post_id),
            'user_id': ObjectId(user_id)
        })
        return like is not None

    @staticmethod
    def is_post_starred_by_user(post_id: str, user_id: str):
        """Check if a user has starred a specific post"""
        star = g.db.post_stars.find_one({
            'post_id': ObjectId(post_id),
            'user_id': ObjectId(user_id)
        })
        return star is not None

class PostComment:
    @staticmethod
    def create(post_id: str, user_id: str, comment: str, thread_user_id: str, parent_comment_id: str = None, is_owner_reply: bool = False):
        """Create a comment on a post"""
        comment_data = {
            'post_id': ObjectId(post_id),
            'user_id': ObjectId(user_id),
            'thread_user_id': ObjectId(thread_user_id),
            'comment': comment,
            'created_at': datetime.utcnow(),
            'user_username': None,
            'parent_comment_id': ObjectId(parent_comment_id) if parent_comment_id else None,
            'is_owner_reply': is_owner_reply
        }
        
        
        user = g.db.users.find_one({'_id': ObjectId(user_id)})
        if user:
            comment_data['user_username'] = user.get('username', 'Anonymous')
        
        result = g.db.post_comments.insert_one(comment_data)
        
        g.db.community_posts.update_one(
            {'_id': ObjectId(post_id)},
            {'$inc': {'comments_count': 1}}
        )
        
        return str(result.inserted_id)

    @staticmethod
    def get_post_comments(post_id: str, limit: int = 50, thread_user_id: str = None):
        """Get comments for a specific post"""
        query = {'post_id': ObjectId(post_id)}
        if thread_user_id:
            query['thread_user_id'] = ObjectId(thread_user_id)

        cursor = g.db.post_comments.find(query).sort('created_at', -1).limit(limit)
        
        return list(cursor) 