"""
Cleanup script for Mood Journal App
Removes unnecessary files and directories from the original skill planner codebase
"""

import os
import shutil
from pathlib import Path

def remove_file(file_path):
    """Remove a file if it exists"""
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"🗑️  Removed: {file_path}")
    else:
        print(f"⚠️  File not found: {file_path}")

def remove_directory(dir_path):
    """Remove a directory if it exists"""
    if os.path.exists(dir_path):
        shutil.rmtree(dir_path)
        print(f"🗑️  Removed directory: {dir_path}")
    else:
        print(f"⚠️  Directory not found: {dir_path}")

def cleanup():
    """Remove unnecessary files and directories"""
    print("🧹 Starting cleanup for Mood Journal App...")
    print("=" * 50)
    
    # Files to remove from root
    files_to_remove = [
        "server.log",
        "server_test.log",
        "init_social_indexes.py",
        "README_BACKEND.md",
        "Procfile"
    ]
    
    # Directories to remove
    directories_to_remove = [
        "middleware",
        "schemas"
    ]
    
    # API endpoints to remove (keep only mood_journal.py)
    api_files_to_remove = [
        "api/v1/social.py",
        "api/v1/users.py",
        "api/v1/websocket.py",
        "api/v1/plans.py",
        "api/v1/skill_enhancement.py",
        "api/v1/skill_sharing.py",
        "api/v1/feed.py",
        "api/v1/follow.py",
        "api/v1/moderation.py",
        "api/v1/notifications.py",
        "api/v1/cache.py",
        "api/v1/collaboration.py",
        "api/v1/content_moderation.py",
        "api/v1/discovery.py",
        "api/v1/analytics.py",
        "api/v1/batch.py"
    ]
    
    # Services to remove (keep only mood_ai_service.py and resource_service.py)
    service_files_to_remove = [
        "services/user_profile_service.py",
        "services/websocket_service.py",
        "services/skill_service.py",
        "services/social_service.py",
        "services/stats_service.py",
        "services/unsplash_service.py",
        "services/notification_service.py",
        "services/search_service.py",
        "services/follow_service.py",
        "services/habit_service.py",
        "services/interaction_service.py",
        "services/moderation_service.py",
        "services/cache_service.py",
        "services/custom_task_service.py",
        "services/email_service.py",
        "services/ai_service.py",
        "services/analytics_service.py",
        "services/batch_processor.py",
        "services/activity_feed_service.py"
    ]
    
    # Repositories to remove (all of them - we're using models directly)
    repository_files_to_remove = [
        "repositories/shared_skill_repository.py",
        "repositories/skill_completion_repository.py",
        "repositories/skill_repository.py",
        "repositories/user_relationship_repository.py",
        "repositories/interaction_repository.py",
        "repositories/moderation_repository.py",
        "repositories/notification_repository.py",
        "repositories/comment_repository.py",
        "repositories/custom_task_repository.py",
        "repositories/habit_repository.py",
        "repositories/analytics_repository.py",
        "repositories/checkin_repository.py"
    ]
    
    # Remove root files
    print("\n📁 Removing unnecessary root files...")
    for file in files_to_remove:
        remove_file(file)
    
    # Remove directories
    print("\n📁 Removing unnecessary directories...")
    for directory in directories_to_remove:
        remove_directory(directory)
    
    # Remove API files
    print("\n📁 Removing unnecessary API endpoints...")
    for file in api_files_to_remove:
        remove_file(file)
    
    # Remove service files
    print("\n📁 Removing unnecessary services...")
    for file in service_files_to_remove:
        remove_file(file)
    
    # Remove repository files
    print("\n📁 Removing unnecessary repositories...")
    for file in repository_files_to_remove:
        remove_file(file)
    
    # Remove repositories directory if empty
    if os.path.exists("repositories") and not os.listdir("repositories"):
        remove_directory("repositories")
    
    # Rename cleaned files
    print("\n📝 Renaming cleaned files...")
    if os.path.exists("app.py"):
        os.rename("app.py", "app_original.py")
        print("📝 Renamed: app.py → app_original.py")
    
    if os.path.exists("app_clean.py"):
        os.rename("app_clean.py", "app.py")
        print("📝 Renamed: app_clean.py → app.py")
    
    if os.path.exists("requirements.txt"):
        os.rename("requirements.txt", "requirements_original.txt")
        print("📝 Renamed: requirements.txt → requirements_original.txt")
    
    if os.path.exists("requirements_clean.txt"):
        os.rename("requirements_clean.txt", "requirements.txt")
        print("📝 Renamed: requirements_clean.txt → requirements.txt")
    
    print("\n✅ Cleanup completed!")
    print("\n📋 Summary of what was kept:")
    print("✅ auth/ - Authentication system")
    print("✅ api/v1/mood_journal.py - Mood journal API")
    print("✅ models/mood_journal.py - Mood journal models")
    print("✅ services/mood_ai_service.py - AI recommendation service")
    print("✅ services/resource_service.py - Resource service (used by AI)")
    print("✅ app.py - Cleaned main application")
    print("✅ requirements.txt - Cleaned dependencies")
    print("✅ test_mood_journal.py - Test script")
    print("✅ README_MOOD_JOURNAL.md - Documentation")
    
    print("\n🚀 Your mood journal backend is now clean and ready!")

if __name__ == "__main__":
    cleanup() 