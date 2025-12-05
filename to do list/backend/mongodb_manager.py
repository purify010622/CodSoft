from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from datetime import datetime
from typing import List, Dict, Optional
import os

class MongoDBManager:
    """Manages tasks using MongoDB with automatic fallback to JSON"""
    
    def __init__(self, connection_string: str = "mongodb://localhost:27017/"):
        try:
            # Connect to MongoDB with timeout
            self.client = MongoClient(
                connection_string,
                serverSelectionTimeoutMS=5000,
                connectTimeoutMS=5000
            )
            
            # Verify connection
            self.client.admin.command('ping')
            
            # Setup database and collection
            self.db = self.client['taskflow_db']
            self.tasks_collection = self.db['tasks']
            
            # Create indexes for faster queries
            self.tasks_collection.create_index([('user_id', 1)])
            self.tasks_collection.create_index([('id', 1)])
            
            print("✓ MongoDB connected successfully")
        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            print(f"✗ MongoDB connection failed: {e}")
            print("  App will use JSON file storage instead")
            self.client = None
    
    def create_task(self, task_data: Dict) -> Dict:
        """Create a new task"""
        if not self.client:
            return None
        
        task_data['created_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        result = self.tasks_collection.insert_one(task_data)
        task_data['_id'] = str(result.inserted_id)
        return task_data
    
    def get_all_tasks(self, user_id: str = None) -> List[Dict]:
        """Get all tasks for a user"""
        if not self.client:
            return []
        
        query = {'user_id': user_id} if user_id else {}
        tasks = list(self.tasks_collection.find(query))
        
        # Convert MongoDB ObjectId to string
        for task in tasks:
            task['_id'] = str(task['_id'])
        
        return tasks
    
    def get_task(self, task_id: int, user_id: str = None) -> Optional[Dict]:
        """Get a specific task by ID"""
        if not self.client:
            return None
        
        query = {'id': task_id}
        if user_id:
            query['user_id'] = user_id
        
        task = self.tasks_collection.find_one(query)
        if task:
            task['_id'] = str(task['_id'])
        return task
    
    def update_task(self, task_id: int, update_data: Dict, user_id: str = None) -> bool:
        """Update a task"""
        if not self.client:
            return False
        
        query = {'id': task_id}
        if user_id:
            query['user_id'] = user_id
        
        result = self.tasks_collection.update_one(
            query,
            {'$set': update_data}
        )
        return result.modified_count > 0
    
    def delete_task(self, task_id: int, user_id: str = None) -> bool:
        """Delete a task"""
        if not self.client:
            return False
        
        query = {'id': task_id}
        if user_id:
            query['user_id'] = user_id
        
        result = self.tasks_collection.delete_one(query)
        return result.deleted_count > 0
    
    def search_tasks(self, query: str, user_id: str = None) -> List[Dict]:
        """Search tasks by title or description"""
        if not self.client:
            return []
        
        search_query = {
            '$or': [
                {'title': {'$regex': query, '$options': 'i'}},
                {'description': {'$regex': query, '$options': 'i'}}
            ]
        }
        
        if user_id:
            search_query['user_id'] = user_id
        
        tasks = list(self.tasks_collection.find(search_query))
        for task in tasks:
            task['_id'] = str(task['_id'])
        
        return tasks
