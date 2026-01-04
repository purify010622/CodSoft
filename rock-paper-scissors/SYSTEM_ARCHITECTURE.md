# Rock Paper Scissors - System Architecture

## Overview

The Rock Paper Scissors multiplayer game is a real-time web application built with modern technologies. It features a React frontend, Flask backend with Socket.IO for real-time communication, Firebase authentication, and MongoDB for persistent data storage. The architecture is designed for scalability, real-time performance, and seamless user experience.

## Architecture Design

### 1. High-Level System Architecture
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   React Client  │◄──►│   Flask API     │◄──►│   MongoDB       │
│   + Socket.IO   │    │   + Socket.IO   │    │   Database      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ Firebase Auth   │    │ Game Engine     │    │ Real-time       │
│ Google OAuth    │    │ Match Making    │    │ Event Store     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### 2. Microservices Architecture
```
┌─────────────────────────────────────────────────────────────────┐
│                        Frontend Layer                           │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐│
│  │    Game     │ │    Auth     │ │ Leaderboard │ │   Profile   ││
│  │ Components  │ │ Components  │ │ Components  │ │ Components  ││
│  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘│
└─────────────────────────────────────────────────────────────────┘
                                │
┌─────────────────────────────────────────────────────────────────┐
│                         API Gateway                             │
│                      (Flask Application)                        │
└─────────────────────────────────────────────────────────────────┘
                                │
┌─────────────────────────────────────────────────────────────────┐
│                      Service Layer                              │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐│
│  │    Auth     │ │    Game     │ │    User     │ │   Admin     ││
│  │   Service   │ │   Service   │ │   Service   │ │   Service   ││
│  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘│
└─────────────────────────────────────────────────────────────────┘
                                │
┌─────────────────────────────────────────────────────────────────┐
│                        Data Layer                               │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐│
│  │   Users     │ │    Games    │ │   Stats     │ │ Leaderboard ││
│  │ Collection  │ │ Collection  │ │ Collection  │ │ Collection  ││
│  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘│
└─────────────────────────────────────────────────────────────────┘
```

## Technical Specifications

### Frontend Architecture (React + Vite)
```javascript
// Core Technologies
React 18.2.0              // UI framework with hooks
Vite 7.3.0                // Build tool and dev server
Tailwind CSS 3.3.6        // Utility-first CSS framework

// Real-time Communication
Socket.IO Client 4.5.4     // WebSocket client for real-time events

// Authentication & HTTP
Firebase 10.7.1            // Authentication and user management
Axios 1.6.2               // HTTP client for API requests

// UI Enhancement
Framer Motion 10.16.16     // Animation library
React Router 6.20.0        // Client-side routing
```

### Backend Architecture (Flask + Socket.IO)
```python
# Core Framework
Flask 3.0.0               # Web framework
Flask-SocketIO 5.3.5      # Real-time WebSocket support
Flask-CORS 4.0.0          # Cross-origin resource sharing

# Database & Storage
PyMongo 4.6.1             # MongoDB driver
MongoDB Atlas/Local        # Document database

# Authentication & Security
Firebase Admin 6.3.0      # Firebase server-side SDK
python-dotenv 1.0.0       # Environment variable management
bcrypt 4.1.2              # Password hashing (if needed)

# Production Server
Gunicorn 21.2.0           # WSGI HTTP server
Eventlet 0.33.3           # Async networking library
```

## Real-Time Communication Architecture

### Socket.IO Event System
```python
# Client to Server Events
join_game(game_id)         # Join a specific game room
make_move(move_data)       # Submit rock/paper/scissors move
leave_game(game_id)        # Leave current game
player_ready()             # Signal ready to start

# Server to Client Events
game_joined(game_data)     # Confirmation of joining game
opponent_found(opponent)   # Matched with another player
move_received(move_info)   # Opponent made a move
round_result(result)       # Result of current round
game_ended(final_result)   # Game completion with stats
player_disconnected()      # Opponent left the game
```

### Real-Time Data Flow
```
Player Action → Frontend → Socket.IO Client → Server → Game Engine
                                                          │
Game State Update ← Frontend ← Socket.IO Server ← Game Logic
```

## Database Architecture

### MongoDB Collections Schema

#### Users Collection
```javascript
{
  _id: ObjectId,
  firebase_uid: String,      // Firebase user ID
  email: String,
  display_name: String,
  avatar_url: String,
  created_at: Date,
  last_active: Date,
  stats: {
    games_played: Number,
    games_won: Number,
    games_lost: Number,
    games_tied: Number,
    win_rate: Number,
    current_streak: Number,
    best_streak: Number
  },
  preferences: {
    preferred_mode: String,
    notifications: Boolean,
    sound_effects: Boolean
  }
}
```

#### Games Collection
```javascript
{
  _id: ObjectId,
  game_id: String,           // Unique game identifier
  mode: String,              // quick_play, best_of_3, best_of_5, etc.
  status: String,            // waiting, active, completed, abandoned
  players: [
    {
      user_id: String,
      display_name: String,
      ready: Boolean,
      connected: Boolean
    }
  ],
  rounds: [
    {
      round_number: Number,
      moves: {
        player1: String,     // rock, paper, scissors
        player2: String
      },
      result: String,        // player1_wins, player2_wins, tie
      timestamp: Date
    }
  ],
  final_result: {
    winner: String,
    scores: {
      player1: Number,
      player2: Number,
      ties: Number
    }
  },
  created_at: Date,
  completed_at: Date
}
```

#### Leaderboard Collection
```javascript
{
  _id: ObjectId,
  user_id: String,
  display_name: String,
  total_games: Number,
  wins: Number,
  win_rate: Number,
  current_streak: Number,
  best_streak: Number,
  rank: Number,
  last_updated: Date
}
```

## Game Engine Architecture

### Game State Management
```python
class GameEngine:
    def __init__(self):
        self.active_games = {}     # In-memory game states
        self.waiting_players = []  # Matchmaking queue
        
    def create_game(self, player, mode):
        # Create new game instance
        # Add to active games
        # Return game ID
        
    def join_game(self, game_id, player):
        # Add player to existing game
        # Check if game can start
        # Notify players
        
    def make_move(self, game_id, player_id, move):
        # Validate move
        # Store move in game state
        # Check if round complete
        # Calculate result if both moves received
        
    def calculate_result(self, move1, move2):
        # Rock Paper Scissors logic
        # Return winner or tie
```

### Matchmaking System
```python
class MatchmakingService:
    def __init__(self):
        self.waiting_queues = {
            'quick_play': [],
            'best_of_3': [],
            'best_of_5': [],
            'best_of_7': []
        }
        
    def find_match(self, player, mode):
        # Add to appropriate queue
        # Try to match with waiting player
        # Create game if match found
        
    def remove_from_queue(self, player_id):
        # Remove player from all queues
        # Clean up abandoned matches
```

## Security Architecture

### Authentication Flow
```
1. User clicks "Sign in with Google"
2. Firebase handles OAuth flow
3. Frontend receives Firebase ID token
4. Token sent to backend with each request
5. Backend verifies token with Firebase Admin SDK
6. User session established
```

### API Security Measures
- **Token Validation**: Every API request validates Firebase token
- **CORS Configuration**: Controlled cross-origin access
- **Input Sanitization**: All user inputs validated and sanitized
- **Rate Limiting**: Prevent abuse of API endpoints
- **Secure Headers**: Security headers for XSS and CSRF protection

### Real-Time Security
- **Socket Authentication**: Socket.IO connections require valid tokens
- **Room Isolation**: Players can only access their game rooms
- **Move Validation**: Server validates all game moves
- **Anti-Cheating**: Server-side game logic prevents manipulation

## Performance Architecture

### Frontend Performance
- **Code Splitting**: Lazy loading of game components
- **State Optimization**: Efficient React state management
- **Asset Optimization**: Vite-based build optimization
- **Caching Strategy**: Browser caching for static assets

### Backend Performance
- **Connection Pooling**: MongoDB connection management
- **In-Memory Game State**: Fast access to active games
- **Async Processing**: Non-blocking I/O operations
- **Database Indexing**: Optimized queries with proper indexes

### Real-Time Performance
- **WebSocket Optimization**: Efficient Socket.IO configuration
- **Event Batching**: Batch multiple events when possible
- **Connection Management**: Handle disconnections gracefully
- **Latency Optimization**: Minimize round-trip times

## Scalability Architecture

### Horizontal Scaling
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Load Balancer │◄──►│   Flask App 1   │◄──►│   MongoDB       │
│     (Nginx)     │    │   + Socket.IO   │    │   Replica Set   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │              ┌─────────────────┐              │
         └─────────────►│   Flask App 2   │◄─────────────┘
                        │   + Socket.IO   │
                        └─────────────────┘
```

### Socket.IO Scaling with Redis
```python
# Redis adapter for Socket.IO clustering
socketio = SocketIO(
    app, 
    message_queue='redis://localhost:6379',
    cors_allowed_origins="*"
)
```

### Database Scaling
- **MongoDB Sharding**: Horizontal partitioning for large datasets
- **Read Replicas**: Distribute read operations across replicas
- **Indexing Strategy**: Compound indexes for complex queries
- **Connection Pooling**: Efficient connection management

## Deployment Architecture

### Development Environment
```yaml
# docker-compose.yml
version: '3.8'
services:
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      - VITE_API_URL=http://localhost:5000
      
  backend:
    build: ./backend
    ports:
      - "5000:5000"
    environment:
      - MONGODB_URI=mongodb://mongo:27017/rps
      
  mongo:
    image: mongo:latest
    ports:
      - "27017:27017"
```

### Production Environment
```yaml
# docker-compose.prod.yml
version: '3.8'
services:
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile.prod
    ports:
      - "80:80"
      
  backend:
    build: ./backend
    ports:
      - "5000:5000"
    environment:
      - MONGODB_URI=${MONGODB_ATLAS_URI}
      - REDIS_URL=${REDIS_CLOUD_URL}
```

## Monitoring and Observability

### Application Metrics
- **Game Statistics**: Active games, players online, match completion rates
- **Performance Metrics**: Response times, Socket.IO latency, database query times
- **Error Tracking**: Exception monitoring and alerting
- **User Analytics**: Feature usage, user retention, game mode preferences

### Infrastructure Monitoring
- **Server Health**: CPU, memory, disk usage
- **Database Performance**: Query performance, connection counts
- **Network Metrics**: Bandwidth usage, connection quality
- **Real-Time Metrics**: WebSocket connection counts, message throughput

## Error Handling and Recovery

### Frontend Error Handling
```javascript
// Network error recovery
const handleNetworkError = (error) => {
  if (error.code === 'NETWORK_ERROR') {
    // Attempt reconnection
    // Show user-friendly message
    // Retry failed operations
  }
};

// Socket.IO reconnection
socket.on('disconnect', () => {
  // Show connection lost message
  // Attempt automatic reconnection
  // Restore game state when reconnected
});
```

### Backend Error Handling
```python
# Graceful error handling
@app.errorhandler(Exception)
def handle_error(error):
    # Log error details
    # Return appropriate error response
    # Notify monitoring systems
    
# Socket.IO error handling
@socketio.on_error_default
def default_error_handler(e):
    # Log Socket.IO errors
    # Attempt recovery
    # Notify client of issues
```

## Testing Strategy

### Frontend Testing
- **Unit Tests**: Component testing with Jest and React Testing Library
- **Integration Tests**: API integration and Socket.IO communication
- **E2E Tests**: Full game flow testing with Cypress
- **Performance Tests**: Bundle size and runtime performance

### Backend Testing
- **Unit Tests**: Individual function and class testing
- **API Tests**: Endpoint testing with proper authentication
- **Socket.IO Tests**: Real-time event testing
- **Load Tests**: Concurrent user simulation

### Game Logic Testing
- **Move Validation**: Test all rock-paper-scissors combinations
- **Game State**: Test state transitions and edge cases
- **Matchmaking**: Test queue management and matching logic
- **Scoring**: Validate scoring algorithms and statistics

## Future Enhancement Architecture

### Advanced Features
- **Tournament System**: Bracket-style competitions
- **Spectator Mode**: Watch live games with real-time updates
- **Custom Game Modes**: User-defined rules and variations
- **AI Opponents**: Multiple difficulty levels with machine learning

### Technical Improvements
- **Microservices**: Split into smaller, focused services
- **GraphQL**: More flexible API with real-time subscriptions
- **Progressive Web App**: Offline capability and mobile optimization
- **Machine Learning**: Player behavior analysis and AI improvements

### Infrastructure Evolution
- **Kubernetes**: Container orchestration for better scaling
- **Service Mesh**: Advanced networking and security
- **Event Sourcing**: Complete game event history
- **CQRS**: Separate read and write models for optimization

This architecture ensures the Rock Paper Scissors game remains performant, scalable, and maintainable while providing an excellent real-time gaming experience for users.