from locust import HttpUser, task, between
import json
from datetime import datetime, timedelta
import random


class DecoRouteUser(HttpUser):
    wait_time = between(1, 3)
    
    def on_start(self):
        """Setup: login and get token"""
        # Register a new user
        username = f"perfuser_{random.randint(10000, 99999)}"
        email = f"{username}@test.com"
        
        register_response = self.client.post("/api/auth/register", json={
            "email": email,
            "username": username,
            "password": "testpass123",
            "full_name": "Performance Test User",
            "certification_level": "Open Water"
        })
        
        if register_response.status_code == 200:
            # Login to get token
            login_response = self.client.post("/api/auth/token", data={
                "username": username,
                "password": "testpass123"
            })
            
            if login_response.status_code == 200:
                self.token = login_response.json()["access_token"]
                self.headers = {"Authorization": f"Bearer {self.token}"}
            else:
                self.token = None
                self.headers = {}
        else:
            # User might already exist, try login
            login_response = self.client.post("/api/auth/token", data={
                "username": username,
                "password": "testpass123"
            })
            
            if login_response.status_code == 200:
                self.token = login_response.json()["access_token"]
                self.headers = {"Authorization": f"Bearer {self.token}"}
            else:
                self.token = None
                self.headers = {}
    
    @task(3)
    def check_transit_safety(self):
        """Test the Safe Transit Engine endpoint"""
        if not self.token:
            return
        
        # Generate realistic dive data
        base_time = datetime.now() - timedelta(hours=random.randint(12, 48))
        dives = []
        
        # Add 1-3 dives
        num_dives = random.randint(1, 3)
        for i in range(num_dives):
            dives.append({
                "dive_site_id": random.choice([1, 2]),
                "dive_datetime": (base_time + timedelta(hours=i * 4)).isoformat(),
                "max_depth": random.uniform(15.0, 40.0),
                "bottom_time": random.randint(25, 60)
            })
        
        # Flight time after last dive
        flight_time = datetime.now() + timedelta(hours=random.randint(2, 72))
        
        response = self.client.post(
            "/api/transit/check-safety",
            json={
                "dives": dives,
                "flight_datetime": flight_time.isoformat()
            },
            headers=self.headers
        )
        
        # Verify response time is under 500ms
        if response.status_code == 200:
            assert response.elapsed.total_seconds() < 0.5, "Transit safety check took too long"
    
    @task(2)
    def get_dive_sites(self):
        """Test dive sites endpoint"""
        if not self.token:
            return
        
        self.client.get("/api/dive-sites/", headers=self.headers)
    
    @task(2)
    def get_user_trips(self):
        """Test user trips endpoint"""
        if not self.token:
            return
        
        self.client.get("/api/trips/", headers=self.headers)
    
    @task(1)
    def create_trip(self):
        """Test trip creation endpoint"""
        if not self.token:
            return
        
        trip_data = {
            "name": f"Performance Test Trip {random.randint(1000, 9999)}",
            "description": "Load testing trip creation",
            "start_date": (datetime.now() + timedelta(days=random.randint(1, 30))).isoformat(),
            "end_date": (datetime.now() + timedelta(days=random.randint(31, 60))).isoformat(),
            "is_public": False
        }
        
        self.client.post("/api/trips/", json=trip_data, headers=self.headers)
    
    @task(1)
    def get_user_profile(self):
        """Test user profile endpoint"""
        if not self.token:
            return
        
        self.client.get("/api/auth/me", headers=self.headers)
    
    @task(1)
    def health_check(self):
        """Test health check endpoint"""
        self.client.get("/health")


class AdminUser(HttpUser):
    wait_time = between(2, 5)
    weight = 1  # Less frequent admin user
    
    def on_start(self):
        """Admin user with higher privileges"""
        # Use a fixed admin user for testing
        self.token = None
        self.headers = {}
    
    @task
    def admin_health_check(self):
        """Admin health monitoring"""
        self.client.get("/health")
        self.client.get("/")


class StressTestUser(HttpUser):
    """High-frequency user for stress testing"""
    wait_time = between(0.1, 0.5)  # Very fast requests
    weight = 0.5  # Lower weight to avoid overwhelming
    
    def on_start(self):
        """Quick login without registration"""
        username = f"stressuser_{random.randint(10000, 99999)}"
        
        # Try direct login (user might exist from previous runs)
        login_response = self.client.post("/api/auth/token", data={
            "username": username,
            "password": "testpass123"
        })
        
        if login_response.status_code == 200:
            self.token = login_response.json()["access_token"]
            self.headers = {"Authorization": f"Bearer {self.token}"}
        else:
            self.token = None
            self.headers = {}
    
    @task
    def rapid_transit_check(self):
        """Rapid transit safety checks"""
        if not self.token:
            return
        
        # Simple transit check
        response = self.client.post(
            "/api/transit/check-safety",
            json={
                "dives": [{
                    "dive_site_id": 1,
                    "dive_datetime": (datetime.now() - timedelta(hours=20)).isoformat(),
                    "max_depth": 20.0,
                    "bottom_time": 45
                }],
                "flight_datetime": (datetime.now() + timedelta(hours=4)).isoformat()
            },
            headers=self.headers
        )
        
        # Strict performance requirement
        if response.status_code == 200:
            assert response.elapsed.total_seconds() < 0.3, "Stress test transit check too slow"
