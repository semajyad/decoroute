"""
🧪 MODEL VALIDATION TESTS
Tests to catch model field mismatches and validation issues

Run with: python model_validation_tests.py
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_user_model_fields():
    """Test User model field definitions"""
    try:
        from models import User
        from sqlalchemy import inspect
        
        # Get model columns
        mapper = inspect(User)
        columns = [column.key for column in mapper.columns]
        
        print("User model columns:")
        for col in columns:
            print(f"  - {col}")
        
        # Expected fields
        expected_fields = [
            'id', 'email', 'username', 'hashed_password', 'full_name',
            'certification_level', 'total_dives', 'created_at', 'updated_at', 'is_active'
        ]
        
        # Check for missing fields
        missing_fields = [field for field in expected_fields if field not in columns]
        if missing_fields:
            print(f"❌ Missing User model fields: {missing_fields}")
            return False
        
        # Check for extra fields
        extra_fields = [field for field in columns if field not in expected_fields]
        if extra_fields:
            print(f"⚠️  Extra User model fields: {extra_fields}")
        
        # Check for correct password field name
        if 'hashed_password' not in columns:
            print("❌ User model missing 'hashed_password' field")
            return False
        
        if 'password_hash' in columns:
            print("❌ User model has incorrect 'password_hash' field (should be 'hashed_password')")
            return False
        
        print("✅ User model fields are correct")
        return True
        
    except Exception as e:
        print(f"❌ Error testing User model: {e}")
        return False

def test_dive_site_model_fields():
    """Test DiveSite model field definitions"""
    try:
        from models import DiveSite
        from sqlalchemy import inspect
        
        # Get model columns
        mapper = inspect(DiveSite)
        columns = [column.key for column in mapper.columns]
        
        print("DiveSite model columns:")
        for col in columns:
            print(f"  - {col}")
        
        # Expected fields
        expected_fields = [
            'id', 'name', 'description', 'location', 'country',
            'latitude', 'longitude', 'max_depth', 'water_type',
            'difficulty_level', 'marine_life_highlights', 'best_season',
            'certification_required', 'average_visibility', 'current_strength',
            'is_active', 'created_at'
        ]
        
        # Check for missing fields
        missing_fields = [field for field in expected_fields if field not in columns]
        if missing_fields:
            print(f"❌ Missing DiveSite model fields: {missing_fields}")
            return False
        
        print("✅ DiveSite model fields are correct")
        return True
        
    except Exception as e:
        print(f"❌ Error testing DiveSite model: {e}")
        return False

def test_user_creation():
    """Test User model creation with correct field names"""
    try:
        from models import User
        from datetime import datetime
        
        # Test creating a User with correct field names
        user_data = {
            'email': 'test@example.com',
            'username': 'testuser',
            'hashed_password': 'hashed_password_here',
            'full_name': 'Test User',
            'certification_level': 'Open Water',
            'total_dives': 0,
            'created_at': datetime.now(),
            'is_active': True
        }
        
        try:
            user = User(**user_data)
            print("✅ User creation with correct fields works")
        except Exception as e:
            print(f"❌ User creation failed: {e}")
            return False
        
        # Test creating a User with incorrect field names
        try:
            incorrect_data = user_data.copy()
            incorrect_data['password_hash'] = 'incorrect_field_name'
            del incorrect_data['hashed_password']
            
            user = User(**incorrect_data)
            print("❌ User creation with incorrect field names should have failed")
            return False
            
        except TypeError as e:
            if "password_hash" in str(e):
                print("✅ User creation correctly rejects 'password_hash' field")
            else:
                print(f"❌ Unexpected error: {e}")
                return False
        except Exception as e:
            print(f"❌ Unexpected error type: {e}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing user creation: {e}")
        return False

def test_auth_router_field_usage():
    """Test that auth router uses correct field names"""
    try:
        # Read the auth router file
        with open('routers/auth.py', 'r') as f:
            content = f.read()
        
        # Check for correct field usage
        if 'password_hash=' in content:
            print("❌ Auth router uses incorrect 'password_hash' field")
            return False
        
        if 'hashed_password=' not in content:
            print("❌ Auth router doesn't use 'hashed_password' field")
            return False
        
        # Check for User model instantiation
        import re
        user_instantiations = re.findall(r'User\(', content)
        
        if len(user_instantiations) == 0:
            print("⚠️  No User model instantiations found")
            return True
        
        print("✅ Auth router uses correct field names")
        return True
        
    except Exception as e:
        print(f"❌ Error checking auth router: {e}")
        return False

def test_database_initialization():
    """Test database initialization code"""
    try:
        # Read the main.py file
        with open('main.py', 'r') as f:
            content = f.read()
        
        # Check for database initialization
        if 'Base.metadata.create_all' not in content:
            print("❌ Database initialization not found in main.py")
            return False
        
        # Check for startup event
        if '@app.on_event("startup")' not in content:
            print("❌ Startup event not found in main.py")
            return False
        
        print("✅ Database initialization code is present")
        return True
        
    except Exception as e:
        print(f"❌ Error checking database initialization: {e}")
        return False

def run_all_validation_tests():
    """Run all model validation tests"""
    print("🧪 MODEL VALIDATION TESTS")
    print("=" * 40)
    
    tests = [
        ("User Model Fields", test_user_model_fields),
        ("DiveSite Model Fields", test_dive_site_model_fields),
        ("User Creation", test_user_creation),
        ("Auth Router Field Usage", test_auth_router_field_usage),
        ("Database Initialization", test_database_initialization),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        print(f"\n🔍 {test_name}:")
        print("-" * 30)
        
        try:
            if test_func():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ Test crashed: {e}")
            failed += 1
    
    print("\n" + "=" * 40)
    print(f"RESULTS: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("🎉 ALL MODEL VALIDATION TESTS PASSED!")
        print("✅ Models are correctly defined!")
        return True
    else:
        print(f"❌ {failed} MODEL VALIDATION TESTS FAILED")
        print("🔧 Fix model issues before deploying")
        return False

if __name__ == "__main__":
    success = run_all_validation_tests()
    sys.exit(0 if success else 1)
