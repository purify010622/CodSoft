from flask import Flask, request, jsonify
from flask_cors import CORS
from task_manager import TaskManager
from mongodb_manager import MongoDBManager
from functools import wraps
import os

app = Flask(__name__)

# Enable CORS for frontend requests
CORS(app, resources={
    r"/api/*": {
        "origins": "*",
        "methods": ["GET", "POST", "PUT", "DELETE", "PATCH"],
        "allow_headers": ["Content-Type"]
    }
})

# Initialize task managers (MongoDB + JSON fallback)
data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "tasks.json")
task_manager = TaskManager(data_path)
mongo_manager = MongoDBManager()

# Decorator for consistent error handling
def handle_errors(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    return decorated_function

@app.route('/api/tasks', methods=['GET'])
@handle_errors
def get_tasks():
    """Get all tasks with optional filtering"""
    user_id = request.args.get('user_id')
    filter_type = request.args.get('filter', 'all')
    priority = request.args.get('priority', 'All')
    search = request.args.get('search', '')
    
    # Use MongoDB if available, otherwise use JSON storage
    if mongo_manager.client:
        if search:
            tasks = mongo_manager.search_tasks(search, user_id)
        else:
            tasks = mongo_manager.get_all_tasks(user_id)
    else:
        if search:
            tasks = task_manager.search_tasks(search)
        else:
            tasks = task_manager.filter_tasks(filter_type)
    
    # Filter by user for JSON storage
    if user_id and not mongo_manager.client:
        tasks = [task for task in tasks if task.get('user_id') == user_id]
    
    # Apply status filter
    if filter_type == 'completed':
        tasks = [task for task in tasks if task.get('completed')]
    elif filter_type == 'pending':
        tasks = [task for task in tasks if not task.get('completed')]
    
    # Apply priority filter
    if priority != 'All':
        tasks = [task for task in tasks if task.get('priority') == priority]
    
    return jsonify(tasks)

@app.route('/api/tasks/<int:task_id>', methods=['GET'])
@handle_errors
def get_task(task_id):
    """Get a specific task"""
    task = task_manager.get_task(task_id)
    if task:
        return jsonify(task)
    return jsonify({"error": "Task not found"}), 404

@app.route('/api/tasks', methods=['POST'])
@handle_errors
def create_task():
    """Create a new task"""
    data = request.json
    
    # Create task in JSON storage
    task = task_manager.create_task(
        title=data.get('title'),
        description=data.get('description', ''),
        priority=data.get('priority', 'Medium'),
        due_date=data.get('due_date', '')
    )
    
    # Associate task with user
    task['user_id'] = data.get('user_id', '')
    task_manager.update_task(task['id'], user_id=task['user_id'])
    
    # Sync to MongoDB if available
    if mongo_manager.client:
        mongo_manager.create_task(task)
    
    return jsonify(task), 201

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
@handle_errors
def update_task(task_id):
    """Update a task"""
    data = request.json
    user_id = data.get('user_id')
    
    # Update in JSON
    success = task_manager.update_task(task_id, **data)
    
    # Update in MongoDB if available
    if mongo_manager.client:
        mongo_manager.update_task(task_id, data, user_id)
    
    if success:
        task = task_manager.get_task(task_id)
        return jsonify(task)
    return jsonify({"error": "Task not found"}), 404

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
@handle_errors
def delete_task(task_id):
    """Delete a task"""
    user_id = request.args.get('user_id')
    
    # Delete from JSON
    success = task_manager.delete_task(task_id)
    
    # Delete from MongoDB if available
    if mongo_manager.client:
        mongo_manager.delete_task(task_id, user_id)
    
    if success:
        return jsonify({"message": "Task deleted successfully"})
    return jsonify({"error": "Task not found"}), 404

@app.route('/api/tasks/<int:task_id>/toggle', methods=['PATCH'])
@handle_errors
def toggle_task(task_id):
    """Toggle task completion status"""
    user_id = request.args.get('user_id')
    
    # Toggle in JSON
    success = task_manager.toggle_complete(task_id)
    
    if success:
        task = task_manager.get_task(task_id)
        
        # Update in MongoDB if available
        if mongo_manager.client:
            mongo_manager.update_task(task_id, {'completed': task['completed']}, user_id)
        
        return jsonify(task)
    return jsonify({"error": "Task not found"}), 404

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
