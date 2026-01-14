from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.db.models import User

def list_users():
    db = SessionLocal()
    try:
        users = db.query(User).all()
        print(f"Total Users: {len(users)}")
        for user in users:
            print(f"ID: {user.id}, Email: {user.email}, Active: {user.is_active}")
            # print(f"Hash: {user.hashed_password}") 
    finally:
        db.close()

if __name__ == "__main__":
    list_users()
