from pymongo import MongoClient
import random
from datetime import datetime, timedelta
import uuid

def seed_rps(client):
    print("--------------------------------")
    print("Seeding Rock Paper Scissors...")
    db = client['rock_paper_scissors']
    
    # Mock Users
    mock_users = [
        ("GrandMaster_John", "https://api.dicebear.com/7.x/avataaars/svg?seed=John"),
        ("RPS_Queen", "https://api.dicebear.com/7.x/avataaars/svg?seed=Queen"),
        ("The_Rock", "https://api.dicebear.com/7.x/avataaars/svg?seed=Rock"),
        ("Paper_Plane", "https://api.dicebear.com/7.x/avataaars/svg?seed=Paper"),
        ("Scissor_Hands", "https://api.dicebear.com/7.x/avataaars/svg?seed=Hands"),
        ("Alex_Fast", "https://api.dicebear.com/7.x/avataaars/svg?seed=Alex"),
        ("Sarah_Win", "https://api.dicebear.com/7.x/avataaars/svg?seed=Sarah"),
        ("Pro_Gamer_2024", "https://api.dicebear.com/7.x/avataaars/svg?seed=Pro"),
        ("NoobMaster69", "https://api.dicebear.com/7.x/avataaars/svg?seed=Noob"),
        ("Guest_Warrior", "https://api.dicebear.com/7.x/avataaars/svg?seed=Guest")
    ]
    
    for i, (name, photo) in enumerate(mock_users):
        uid = f"mock_user_{i}"
        
        # Stats
        curr_games = random.randint(50, 500)
        wins = int(curr_games * random.uniform(0.4, 0.8))
        losses = int(curr_games * random.uniform(0.1, 0.4))
        ties = curr_games - wins - losses
        if ties < 0: ties = 0; wins = curr_games - losses
        
        user_doc = {
            'firebase_uid': uid,
            'email': f"{name.lower()}@example.com",
            'username': name,
            'photo_url': photo,
            'created_at': datetime.utcnow(),
            'last_login': datetime.utcnow(),
            'stats': {
                'wins': wins,
                'losses': losses,
                'ties': ties,
                'total_games': curr_games,
                'win_rate': round((wins/curr_games)*100, 2)
            }
        }
        
        # Upsert User
        db.users.update_one({'firebase_uid': uid}, {'$set': user_doc}, upsert=True)
        
        # Upsert Leaderboard
        lb_doc = {
            'user_id': uid,
            'total_wins': wins,
            'total_games': curr_games,
            'win_rate': round((wins/curr_games)*100, 2),
            'updated_at': datetime.utcnow()
        }
        db.leaderboard.update_one({'user_id': uid}, {'$set': lb_doc}, upsert=True)
        
    print(f"✓ Seeded {len(mock_users)} users and leaderboard entries.")

def seed_todo(client):
    print("--------------------------------")
    print("Seeding To Do List...")
    db = client['taskflow_db']
    
    # Generic Tasks for Demonstration
    tasks_data = [
        ("Design System Architecture", "High", 2, False),
        ("Client Meeting Preparation", "High", 1, False),
        ("Buy Groceries", "Medium", 0, True),
        ("Update Portfolio Website", "Medium", 5, False),
        ("Morning Jog", "Low", 0, True),
        ("Read Tech Documentation", "Low", 3, False),
        ("Fix Login Bug", "High", 1, False),
        ("Team Sync Call", "Medium", 1, True)
    ]
    
    # UIDs to seed for
    # 1. 'demo_user' (for generic login if available)
    # 2. 'hceDtdAkDtfLiHPbAwvj0VFaCi42' (From tasks.json)
    target_uids = ['demo_user', 'hceDtdAkDtfLiHPbAwvj0VFaCi42']
    
    count = 0
    for uid in target_uids:
        for title, prio, days_offset, comp in tasks_data:
            due = (datetime.now() + timedelta(days=days_offset)).strftime("%Y-%m-%d")
            
            task_doc = {
                'id': random.randint(10000, 99999), 
                'title': title,
                'description': f"Automated task generated for {title}",
                'priority': prio,
                'due_date': due,
                'completed': comp,
                'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'user_id': uid
            }
            # Insert (don't upsert as IDs are random, just append)
            db.tasks.insert_one(task_doc)
            count += 1
            
    print(f"✓ Seeded {count} tasks into 'taskflow_db'.")

if __name__ == '__main__':
    try:
        client = MongoClient('mongodb://localhost:27017/')
        seed_rps(client)
        seed_todo(client)
        print("--------------------------------")
        print("Done! Mock datasets are ready.")
    except Exception as e:
        print(f"Error: {e}")
