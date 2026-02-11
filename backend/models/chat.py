from datetime import datetime
from bson import ObjectId
from flask import g


class ChatConversation:
    @staticmethod
    def _participants_key(user_id: str, other_user_id: str):
        participants = sorted([str(user_id), str(other_user_id)])
        return participants

    @staticmethod
    def create_or_get(user_id: str, other_user_id: str):
        participants = ChatConversation._participants_key(user_id, other_user_id)
        existing = g.db.chat_conversations.find_one({
            "participants": participants
        })
        if existing:
            return str(existing["_id"])

        data = {
            "participants": participants,
            "created_at": datetime.utcnow(),
            "last_message_at": None,
            "last_message_sender_id": None,
            "participant_usernames": ChatConversation._get_participant_usernames(participants)
        }
        result = g.db.chat_conversations.insert_one(data)
        return str(result.inserted_id)

    @staticmethod
    def _get_participant_usernames(participants):
        usernames = {}
        for participant_id in participants:
            user = g.db.users.find_one({"_id": ObjectId(participant_id)})
            if user:
                usernames[str(participant_id)] = user.get("username", "User")
        return usernames

    @staticmethod
    def list_for_user(user_id: str):
        cursor = g.db.chat_conversations.find({
            "participants": str(user_id)
        }).sort("last_message_at", -1)
        return list(cursor)

    @staticmethod
    def get_by_id(conversation_id: str):
        return g.db.chat_conversations.find_one({"_id": ObjectId(conversation_id)})


class ChatMessage:
    @staticmethod
    def create(conversation_id: str, sender_id: str, text: str, client_id: str = None):
        message_data = {
            "conversation_id": ObjectId(conversation_id),
            "sender_id": ObjectId(sender_id),
            "text": text,
            "client_id": client_id,
            "created_at": datetime.utcnow()
        }
        result = g.db.chat_messages.insert_one(message_data)

        g.db.chat_conversations.update_one(
            {"_id": ObjectId(conversation_id)},
            {
                "$set": {
                    "last_message_at": message_data["created_at"],
                    "last_message_sender_id": ObjectId(sender_id)
                }
            }
        )

        return str(result.inserted_id)

    @staticmethod
    def get_messages(conversation_id: str, since: datetime = None, limit: int = 50):
        query = {"conversation_id": ObjectId(conversation_id)}
        if since:
            query["created_at"] = {"$gt": since}

        cursor = g.db.chat_messages.find(query).sort("created_at", 1).limit(limit)
        return list(cursor)
