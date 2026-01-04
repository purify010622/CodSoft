"""
Main Flask application entry point
Initializes Flask app, Socket.IO, MongoDB, and registers routes
"""
from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize Flask app
# Initialize Flask app
app = Flask(__name__)
# DEMO MODE CONFIGURATION
app.config['SECRET_KEY'] = 'demo_mode_secret_key'
os.environ['CORS_ORIGIN'] = 'http://localhost:3000'
os.environ['ASYNC_MODE'] = 'threading'

# Enable CORS
# Enable CORS
cors_origin = os.getenv('CORS_ORIGIN', 'http://localhost:3000')
CORS(app, resources={r"/api/*": {"origins": cors_origin}})

# Initialize Socket.IO
# Initialize Socket.IO
socketio = SocketIO(app, cors_allowed_origins=cors_origin, async_mode=os.getenv('ASYNC_MODE', 'eventlet'))

# Import and initialize database
from utils.database import init_db
db = init_db()

# Import routes
from routes import auth_routes, game_routes, user_routes, admin_routes, leaderboard_routes

# Register blueprints
app.register_blueprint(auth_routes.bp, url_prefix='/api/auth')
app.register_blueprint(game_routes.bp, url_prefix='/api/game')
app.register_blueprint(user_routes.bp, url_prefix='/api/user')
app.register_blueprint(admin_routes.bp, url_prefix='/api/admin')
app.register_blueprint(leaderboard_routes.bp, url_prefix='/api/leaderboard')

# Import Socket.IO handlers
from socket_handler import register_socket_handlers
register_socket_handlers(socketio)

@app.route('/')
def index():
    """Health check endpoint"""
    return {'status': 'ok', 'message': 'Rock Paper Scissors API is running'}

@app.route('/api/health')
def health():
    """Detailed health check"""
    return {
        'status': 'healthy',
        'database': 'connected' if db else 'disconnected',
        'version': '1.0.0'
    }

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug_mode = os.getenv('FLASK_ENV') == 'development'
    socketio.run(app, host='0.0.0.0', port=port, debug=debug_mode)
