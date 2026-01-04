from pymongo import MongoClient
import os

_db = None
_client = None

def init_db():
    global _db, _client
    if _db is not None:
        return _db

    # Use localhost by default
    mongo_uri = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
    db_name = os.getenv('DB_NAME', 'rock_paper_scissors')
    
    try:
        _client = MongoClient(mongo_uri)
        # Verify connection
        _client.admin.command('ping')
        _db = _client[db_name]
        print(f"✓ Connected to MongoDB: {db_name}")
        
        # Create indexes
        _db.users.create_index("firebase_uid", unique=True)
        _db.games.create_index("game_id", unique=True)
        _db.leaderboard.create_index("user_id", unique=True)
        
    except Exception as e:
        print(f"✗ MongoDB Connection Error: {e}")
        # We generally should raise error or exit if DB is strictly required
        # but for robustness we could let it crash later
        raise e
        
    return _db

def get_db():
    global _db
    if _db is None:
        return init_db()
    return _db
