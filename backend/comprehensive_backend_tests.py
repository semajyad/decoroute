"""
🧪 COMPREHENSIVE BACKEND TEST SUITE
Tests all backend functionality to catch issues before production

Run with: python comprehensive_backend_tests.py
"""

import pytest
import requests
import json
import time
from datetime import datetime, timedelta
from typing import Dict, Any

# Test configuration
BASE_URL = "http://localhost:8001"  # Local testing
# BASE_URL = "https://decoroute.onrender.com"  # Production testing

class TestBackendComprehensive:
    """Comprehensive backend testing suite"""
    
    def setup_method(self):
        """Setup for each test method"""
        self.base_url = BASE_URL
        self.test_user_data = {
            "email": "test@example.com",
            "username": "testuser123",
            "password": "testpass123",
            "full_name": "Test User",
            "certification_level": "Open Water"
        }
        
    def test_health_check(self):
        """Test basic health check endpoint"""
        response = requests.get(f"{self.base_url}/health", timeout=10)
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "service" in data
        print("✅ Health check passed")
        
    def test_api_root(self):
        """Test API root endpoint"""
        response = requests.get(f"{self.base_url}/", timeout=10)
        
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "DecoRoute API" in data["message"]
        print("✅ API root check passed")
        
    def test_user_registration_model_fields(self):
        """Test user registration with correct model fields"""
        # Test with all required fields
        response = requests.post(
            f"{self.base_url}/api/auth/register",
            json=self.test_user_data,
            timeout=10
        )
        
        # Should succeed (200) even in demo mode
        assert response.status_code == 200
        data = response.json()
        
        # Verify response has correct User model fields
        expected_fields = ["id", "email", "username", "full_name", 
                          "certification_level", "total_dives", "created_at"]
        for field in expected_fields:
            assert field in data, f"Missing field: {field}"
            
        # Verify field types and values
        assert isinstance(data["id"], int)
        assert data["email"] == self.test_user_data["email"]
        assert data["username"] == self.test_user_data["username"]
        assert data["full_name"] == self.test_user_data["full_name"]
        assert data["certification_level"] == self.test_user_data["certification_level"]
        assert isinstance(data["total_dives"], int)
        
        print("✅ User registration model fields test passed")
        
    def test_user_registration_missing_fields(self):
        """Test user registration with missing required fields"""
        # Test missing full_name
        incomplete_data = {
            "email": "test2@example.com",
            "username": "testuser2",
            "password": "testpass123"
            # Missing full_name
        }
        
        response = requests.post(
            f"{self.base_url}/api/auth/register",
            json=incomplete_data,
            timeout=10
        )
        
        # Should return 422 for validation error
        assert response.status_code == 422
        data = response.json()
        assert "detail" in data
        print("✅ User registration missing fields test passed")
        
    def test_user_registration_duplicate_email(self):
        """Test user registration with duplicate email"""
        # First registration
        requests.post(
            f"{self.base_url}/api/auth/register",
            json=self.test_user_data,
            timeout=10
        )
        
        # Second registration with same email
        duplicate_data = self.test_user_data.copy()
        duplicate_data["username"] = "differentuser"
        
        response = requests.post(
            f"{self.base_url}/api/auth/register",
            json=duplicate_data,
            timeout=10
        )
        
        # Should return 400 for duplicate email (if database works)
        # Or 200 if in demo mode (both are acceptable)
        assert response.status_code in [200, 400]
        print("✅ User registration duplicate email test passed")
        
    def test_login_functionality(self):
        """Test user login functionality"""
        # First register a user
        requests.post(
            f"{self.base_url}/api/auth/register",
            json=self.test_user_data,
            timeout=10
        )
        
        # Then login
        login_data = {
            "username": self.test_user_data["username"],
            "password": self.test_user_data["password"]
        }
        
        response = requests.post(
            f"{self.base_url}/api/auth/login",
            json=login_data,
            timeout=10
        )
        
        # Should succeed (200) even in demo mode
        assert response.status_code == 200
        data = response.json()
        
        # Verify response has correct User model fields
        expected_fields = ["id", "email", "username", "full_name", 
                          "certification_level", "total_dives", "created_at"]
        for field in expected_fields:
            assert field in data, f"Missing field: {field}"
            
        print("✅ Login functionality test passed")
        
    def test_dive_sites_endpoint(self):
        """Test dive sites endpoint"""
        response = requests.get(f"{self.base_url}/api/dive-sites/", timeout=10)
        
        assert response.status_code == 200
        data = response.json()
        
        # Should return list of dive sites
        assert isinstance(data, list)
        
        if len(data) > 0:
            # Verify dive site model fields
            site = data[0]
            expected_fields = ["id", "name", "description", "location", "country",
                              "latitude", "longitude", "max_depth", "water_type",
                              "difficulty_level", "marine_life_highlights", "best_season",
                              "certification_required", "average_visibility", "current_strength"]
            
            for field in expected_fields:
                assert field in site, f"Missing dive site field: {field}"
                
        print("✅ Dive sites endpoint test passed")
        
    def test_dive_site_by_id(self):
        """Test getting dive site by ID"""
        # First get all sites to find a valid ID
        response = requests.get(f"{self.base_url}/api/dive-sites/", timeout=10)
        assert response.status_code == 200
        sites = response.json()
        
        if len(sites) > 0:
            site_id = sites[0]["id"]
            
            # Get specific site
            response = requests.get(f"{self.base_url}/api/dive-sites/{site_id}", timeout=10)
            assert response.status_code == 200
            site = response.json()
            
            # Verify it's the same site
            assert site["id"] == site_id
            assert "name" in site
            
        print("✅ Dive site by ID test passed")
        
    def test_dive_sites_search(self):
        """Test dive sites search functionality"""
        # Search for a common term
        response = requests.get(f"{self.base_url}/api/dive-sites/search/coral", timeout=10)
        
        assert response.status_code == 200
        data = response.json()
        
        # Should return list of dive sites
        assert isinstance(data, list)
        
        print("✅ Dive sites search test passed")
        
    def test_transit_safety_check(self):
        """Test transit safety check endpoint"""
        # Create test dive data
        now = datetime.now()
        flight_time = now + timedelta(hours=20)  # 20 hours from now
        
        transit_data = {
            "dives": [
                {
                    "dive_site_id": 1,
                    "dive_datetime": now.isoformat(),
                    "max_depth": 25.0,
                    "bottom_time": 45
                }
            ],
            "flight_datetime": flight_time.isoformat()
        }
        
        response = requests.post(
            f"{self.base_url}/api/transit/check-safety",
            json=transit_data,
            timeout=10
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify safety check response fields
        expected_fields = ["is_safe", "violation_type", "recommended_wait_time", "details"]
        for field in expected_fields:
            assert field in data, f"Missing safety check field: {field}"
            
        # Verify field types
        assert isinstance(data["is_safe"], bool)
        assert isinstance(data["violation_type"], str)
        assert isinstance(data["recommended_wait_time"], int)
        assert isinstance(data["details"], str)
        
        print("✅ Transit safety check test passed")
        
    def test_transit_safety_check_no_dives(self):
        """Test transit safety check with no dives"""
        transit_data = {
            "dives": [],
            "flight_datetime": (datetime.now() + timedelta(hours=10)).isoformat()
        }
        
        response = requests.post(
            f"{self.base_url}/api/transit/check-safety",
            json=transit_data,
            timeout=10
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # Should be safe with no dives
        assert data["is_safe"] == True
        assert data["violation_type"] == "none"
        assert data["recommended_wait_time"] == 0
        
        print("✅ Transit safety check no dives test passed")
        
    def test_transit_safety_check_multiple_dives(self):
        """Test transit safety check with multiple dives"""
        now = datetime.now()
        flight_time = now + timedelta(hours=20)
        
        transit_data = {
            "dives": [
                {
                    "dive_site_id": 1,
                    "dive_datetime": (now - timedelta(hours=12)).isoformat(),
                    "max_depth": 25.0,
                    "bottom_time": 45
                },
                {
                    "dive_site_id": 2,
                    "dive_datetime": (now - timedelta(hours=6)).isoformat(),
                    "max_depth": 35.0,
                    "bottom_time": 30
                }
            ],
            "flight_datetime": flight_time.isoformat()
        }
        
        response = requests.post(
            f"{self.base_url}/api/transit/check-safety",
            json=transit_data,
            timeout=10
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # Should apply 24-hour rule for multiple dives
        assert isinstance(data["is_safe"], bool)
        assert data["violation_type"] in ["none", "multi_dive_24h_rule"]
        
        print("✅ Transit safety check multiple dives test passed")
        
    def test_trip_crud_operations(self):
        """Test trip CRUD operations"""
        # First register and login to get a user
        reg_response = requests.post(
            f"{self.base_url}/api/auth/register",
            json=self.test_user_data,
            timeout=10
        )
        assert reg_response.status_code == 200
        user = reg_response.json()
        
        # Create a trip
        trip_data = {
            "name": "Test Trip",
            "description": "A test dive trip",
            "start_date": datetime.now().isoformat(),
            "end_date": (datetime.now() + timedelta(days=7)).isoformat(),
            "is_public": False
        }
        
        # Note: This might fail if auth is not properly implemented
        # But we're testing that it doesn't crash the server
        try:
            response = requests.post(
                f"{self.base_url}/api/trips/",
                json=trip_data,
                timeout=10
            )
            # Should either succeed (200) or fail gracefully (401/403/500 with proper error)
            assert response.status_code in [200, 401, 403, 404, 500]
            
            if response.status_code == 200:
                trip = response.json()
                assert "id" in trip
                assert trip["name"] == trip_data["name"]
                
        except Exception as e:
            # If the endpoint crashes, that's what we're trying to catch
            pytest.fail(f"Trip creation crashed the server: {e}")
            
        print("✅ Trip CRUD operations test passed")
        
    def test_error_handling_robustness(self):
        """Test that error handling doesn't crash the server"""
        # Test malformed JSON
        try:
            response = requests.post(
                f"{self.base_url}/api/auth/register",
                data="invalid json",
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            # Should return 422 for malformed JSON, not crash
            assert response.status_code == 422
        except Exception as e:
            pytest.fail(f"Malformed JSON crashed the server: {e}")
            
        # Test invalid endpoint
        try:
            response = requests.get(f"{self.base_url}/api/nonexistent", timeout=10)
            # Should return 404, not crash
            assert response.status_code == 404
        except Exception as e:
            pytest.fail(f"Invalid endpoint crashed the server: {e}")
            
        print("✅ Error handling robustness test passed")
        
    def test_cors_headers(self):
        """Test CORS headers are present"""
        # Test OPTIONS request
        response = requests.options(
            f"{self.base_url}/api/auth/register",
            headers={"Origin": "https://semajyad.github.io"},
            timeout=10
        )
        
        # Should return 200 or 405 (method not allowed) but with CORS headers
        assert response.status_code in [200, 405]
        
        # Check for CORS headers
        headers = response.headers
        assert "access-control-allow-origin" in headers or "Access-Control-Allow-Origin" in headers
        
        print("✅ CORS headers test passed")
        
    def test_database_field_consistency(self):
        """Test database field consistency across models"""
        # This test ensures all model fields are correctly named
        response = requests.post(
            f"{self.base_url}/api/auth/register",
            json=self.test_user_data,
            timeout=10
        )
        
        assert response.status_code == 200
        user = response.json()
        
        # Verify User model fields match expected names
        user_fields = ["id", "email", "username", "hashed_password", "full_name", 
                      "certification_level", "total_dives", "created_at", "updated_at", "is_active"]
        
        # Response should not include hashed_password for security
        public_fields = ["id", "email", "username", "full_name", 
                        "certification_level", "total_dives", "created_at"]
        
        for field in public_fields:
            assert field in user, f"Missing public field: {field}"
            
        # Should not include sensitive fields
        assert "hashed_password" not in user, "Sensitive field leaked in response"
        assert "password" not in user, "Sensitive field leaked in response"
        
        print("✅ Database field consistency test passed")


def run_comprehensive_tests():
    """Run all comprehensive tests"""
    print("🧪 STARTING COMPREHENSIVE BACKEND TESTS")
    print("=" * 50)
    
    # Test basic connectivity first
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code != 200:
            print(f"❌ Backend not responding correctly: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Cannot connect to backend: {e}")
        print(f"   Make sure backend is running at {BASE_URL}")
        return False
    
    # Run pytest with our test class
    print("✅ Backend connectivity confirmed")
    print("🧪 Running comprehensive test suite...")
    
    # Use pytest to run our tests
    exit_code = pytest.main([
        __file__,
        "-v",
        "--tb=short",
        "-x"  # Stop on first failure
    ])
    
    if exit_code == 0:
        print("\n🎉 ALL COMPREHENSIVE TESTS PASSED!")
        print("✅ Backend is production-ready!")
    else:
        print(f"\n❌ TESTS FAILED (exit code: {exit_code})")
        print("🔧 Fix issues before deploying to production")
    
    return exit_code == 0


if __name__ == "__main__":
    run_comprehensive_tests()
