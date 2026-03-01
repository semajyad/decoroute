#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import SessionLocal, engine, Base
from models import User
from routers.auth import get_password_hash
import traceback

def debug_registration():
    print("🔍 DEBUGGING REGISTRATION")
    print("=" * 40)
    
    # Test database connection
    try:
        db = SessionLocal()
        print("✅ Database connection successful")
        
        # Test if tables exist
        from sqlalchemy import inspect
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        print(f"📊 Tables found: {tables}")
        
        # Test password hashing
        try:
            hashed = get_password_hash("Test123")
            print(f"✅ Password hashing works: {hashed[:20]}...")
        except Exception as e:
            print(f"❌ Password hashing error: {e}")
            traceback.print_exc()
        
        # Test user creation manually
        try:
            test_user = User(
                email="test@example.com",
                username="testuser",
                hashed_password=get_password_hash("Test123"),
                full_name="Test User",
                certification_level="Open Water"
            )
            
            db.add(test_user)
            db.commit()
            db.refresh(test_user)
            
            print(f"✅ Manual user creation successful: {test_user.id}")
            
            # Clean up
            db.delete(test_user)
            db.commit()
            print("✅ Test user cleaned up")
            
        except Exception as e:
            print(f"❌ Manual user creation error: {e}")
            traceback.print_exc()
            db.rollback()
        
        db.close()
        
    except Exception as e:
        print(f"❌ Database connection error: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    debug_registration()
