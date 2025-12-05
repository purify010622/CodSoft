import json
import os
from datetime import datetime
from typing import List, Dict, Optional
from threading import Lock

class TaskManager:
    """Manages tasks using JSON file storage with thread-safe operations"""
    
    def __init__(self, data_file: str = "tasks.json"):
        self.data_file = data_file
        self.tasks: List[Dict] = []
        self.lock = Lock()  # Ensure thread-safe file operations
        self.load_tasks()
    
    def load_tasks(self):
        """Load tasks from JSON file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    self.tasks = json.load(f)
            except json.JSONDecodeError:
                self.tasks = []
        else:
            self.tasks = []
    
    def save_tasks(self):
        """Save tasks to JSON file"""
        with self.lock:
            with open(self.data_file, 'w') as f:
                json.dump(self.tasks, f, indent=2)
    
    def create_task(self, title: str, description: str = "", priority: str = "Medium", due_date: str = "") -> Dict:
        """Create a new task"""
        task = {
            "id": self._generate_id(),
            "title": title,
            "description": description,
            "priority": priority,
            "due_date": due_date,
            "completed": False,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.tasks.append(task)
        self.save_tasks()
        return task
    
    def update_task(self, task_id: int, **kwargs) -> bool:
        """Update an existing task"""
        for task in self.tasks:
            if task["id"] == task_id:
                for key, value in kwargs.items():
                    if key in task:
                        task[key] = value
                self.save_tasks()
                return True
        return False
    
    def delete_task(self, task_id: int) -> bool:
        """Delete a task"""
        for i, task in enumerate(self.tasks):
            if task["id"] == task_id:
                self.tasks.pop(i)
                self.save_tasks()
                return True
        return False
    
    def get_task(self, task_id: int) -> Optional[Dict]:
        """Get a specific task by ID"""
        for task in self.tasks:
            if task["id"] == task_id:
                return task
        return None
    
    def get_all_tasks(self) -> List[Dict]:
        """Get all tasks"""
        return self.tasks
    
    def toggle_complete(self, task_id: int) -> bool:
        """Toggle task completion status"""
        for task in self.tasks:
            if task["id"] == task_id:
                task["completed"] = not task["completed"]
                self.save_tasks()
                return True
        return False
    
    def search_tasks(self, query: str) -> List[Dict]:
        """Search tasks by title or description"""
        query = query.lower()
        return [
            task for task in self.tasks
            if query in task["title"].lower() or query in task["description"].lower()
        ]
    
    def filter_tasks(self, filter_type: str, filter_value: str = "") -> List[Dict]:
        """Filter tasks by status, priority, or due date"""
        if filter_type == "completed":
            return [task for task in self.tasks if task["completed"]]
        elif filter_type == "pending":
            return [task for task in self.tasks if not task["completed"]]
        elif filter_type == "priority":
            return [task for task in self.tasks if task["priority"] == filter_value]
        elif filter_type == "all":
            return self.tasks
        return []
    
    def _generate_id(self) -> int:
        """Generate a unique ID for a new task"""
        if not self.tasks:
            return 1
        return max(task["id"] for task in self.tasks) + 1
