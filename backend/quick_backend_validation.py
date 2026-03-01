"""
⚡ QUICK BACKEND VALIDATION
Fast validation script to catch common backend issues

Run with: python quick_backend_validation.py
"""

import requests
import json
import sys
from datetime import datetime, timedelta

# Configuration
BACKEND_URL = "https://decoroute.onrender.com"  # Production backend

def test_endpoint(url, method="GET", data=None, expected_status=200, description=""):
    """Test a single endpoint"""
    try:
        if method == "GET":
            response = requests.get(url, timeout=10)
        elif method == "POST":
            response = requests.post(url, json=data, timeout=10)
        else:
            return False, f"Unsupported method: {method}"
            
        if response.status_code == expected_status:
            return True, f"✅ {description}: {response.status_code}"
        else:
            return False, f"❌ {description}: Expected {expected_status}, got {response.status_code} - {response.text[:100]}"
            
    except Exception as e:
        return False, f"❌ {description}: Exception - {str(e)}"

def run_validation():
    """Run comprehensive backend validation"""
    print("⚡ QUICK BACKEND VALIDATION")
    print("=" * 40)
    print(f"Testing: {BACKEND_URL}")
    print()
    
    results = []
    
    # Test 1: Health Check
    success, message = test_endpoint(
        f"{BACKEND_URL}/health",
        description="Health Check"
    )
    results.append((success, message))
    
    # Test 2: API Root
    success, message = test_endpoint(
        f"{BACKEND_URL}/",
        description="API Root"
    )
    results.append((success, message))
    
    # Test 3: User Registration (correct fields)
    user_data = {
        "email": "test@example.com",
        "username": "testuser123",
        "password": "testpass123",
        "full_name": "Test User",
        "certification_level": "Open Water"
    }
    success, message = test_endpoint(
        f"{BACKEND_URL}/api/auth/register",
        method="POST",
        data=user_data,
        description="User Registration"
    )
    results.append((success, message))
    
    # Test 4: User Registration (missing fields)
    incomplete_data = {
        "email": "test2@example.com",
        "username": "testuser2",
        "password": "testpass123"
        # Missing full_name
    }
    success, message = test_endpoint(
        f"{BACKEND_URL}/api/auth/register",
        method="POST",
        data=incomplete_data,
        expected_status=422,
        description="User Registration (missing fields)"
    )
    results.append((success, message))
    
    # Test 5: Login
    login_data = {
        "username": "testuser123",
        "password": "testpass123"
    }
    success, message = test_endpoint(
        f"{BACKEND_URL}/api/auth/login",
        method="POST",
        data=login_data,
        description="User Login"
    )
    results.append((success, message))
    
    # Test 6: Dive Sites
    success, message = test_endpoint(
        f"{BACKEND_URL}/api/dive-sites/",
        description="Dive Sites List"
    )
    results.append((success, message))
    
    # Test 7: Dive Site Search
    success, message = test_endpoint(
        f"{BACKEND_URL}/api/dive-sites/search/coral",
        description="Dive Sites Search"
    )
    results.append((success, message))
    
    # Test 8: Transit Safety Check
    now = datetime.now()
    transit_data = {
        "dives": [
            {
                "dive_site_id": 1,
                "dive_datetime": now.isoformat(),
                "max_depth": 25.0,
                "bottom_time": 45
            }
        ],
        "flight_datetime": (now + timedelta(hours=20)).isoformat()
    }
    success, message = test_endpoint(
        f"{BACKEND_URL}/api/transit/check-safety",
        method="POST",
        data=transit_data,
        description="Transit Safety Check"
    )
    results.append((success, message))
    
    # Test 9: CORS Headers
    try:
        response = requests.options(
            f"{BACKEND_URL}/api/auth/register",
            headers={"Origin": "https://semajyad.github.io"},
            timeout=10
        )
        if response.status_code in [200, 405]:
            has_cors = "access-control-allow-origin" in response.headers or "Access-Control-Allow-Origin" in response.headers
            if has_cors:
                results.append((True, "✅ CORS Headers: Present"))
            else:
                results.append((False, "❌ CORS Headers: Missing"))
        else:
            results.append((False, f"❌ CORS Headers: Unexpected status {response.status_code}"))
    except Exception as e:
        results.append((False, f"❌ CORS Headers: Exception - {str(e)}"))
    
    # Test 10: Invalid Endpoint (should return 404, not crash)
    success, message = test_endpoint(
        f"{BACKEND_URL}/api/nonexistent",
        expected_status=404,
        description="Invalid Endpoint (404 test)"
    )
    results.append((success, message))
    
    # Print results
    print("RESULTS:")
    print("-" * 40)
    
    passed = 0
    failed = 0
    
    for success, message in results:
        print(message)
        if success:
            passed += 1
        else:
            failed += 1
    
    print("-" * 40)
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Total: {len(results)}")
    
    if failed == 0:
        print("\n🎉 ALL VALIDATIONS PASSED!")
        print("✅ Backend is production-ready!")
        return True
    else:
        print(f"\n❌ {failed} VALIDATIONS FAILED")
        print("🔧 Fix issues before deploying to production")
        return False

if __name__ == "__main__":
    success = run_validation()
    sys.exit(0 if success else 1)
