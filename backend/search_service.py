"""
🔍 DUCKDUCKGO SEARCH SERVICE
Realistic pricing search for dive trips using DuckDuckGo

This service searches for real dive trip pricing data to provide
realistic cost estimates for trip planning.
"""

import requests
import re
import json
from typing import List, Dict, Any, Optional
from datetime import datetime
import time

class DuckDuckGoSearchService:
    """Service for searching dive trip pricing using DuckDuckGo"""
    
    def __init__(self):
        self.base_url = "https://duckduckgo.com/html/"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def search_dive_trip_pricing(self, location: str, duration_days: int = 7) -> Dict[str, Any]:
        """
        Search for realistic dive trip pricing for a specific location
        
        Args:
            location: Dive location (e.g., "Belize", "Red Sea", "Great Barrier Reef")
            duration_days: Trip duration in days
            
        Returns:
            Dictionary with pricing information and search results
        """
        try:
            # Construct search query
            query = f"dive trip cost price {location} {duration_days} days liveaboard resort"
            
            # Search DuckDuckGo
            params = {
                'q': query,
                'kl': 'us-en'  # US English results
            }
            
            response = self.session.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            
            # Parse results
            pricing_data = self._parse_pricing_results(response.text, location, duration_days)
            
            # Add search metadata
            pricing_data['search_metadata'] = {
                'query': query,
                'search_time': datetime.now().isoformat(),
                'location': location,
                'duration_days': duration_days
            }
            
            return pricing_data
            
        except Exception as e:
            print(f"Error searching for pricing: {e}")
            return self._get_fallback_pricing(location, duration_days)
    
    def _parse_pricing_results(self, html_content: str, location: str, duration_days: int) -> Dict[str, Any]:
        """Parse DuckDuckGo HTML results to extract pricing information"""
        
        # Extract price patterns from HTML
        price_patterns = [
            r'\$(\d+(?:,\d{3})*(?:\.\d{2})?)',  # $1,234.56
            r'(\d+(?:,\d{3})*(?:\.\d{2})?)\s*USD',  # 1,234.56 USD
            r'price[:\s]*(\$?\d+(?:,\d{3})*(?:\.\d{2})?)',  # price: $1234
            r'cost[:\s]*(\$?\d+(?:,\d{3})*(?:\.\d{2})?)',  # cost: $1234
            r'from\s*\$(\d+(?:,\d{3})*(?:\.\d{2})?)',  # from $1234
        ]
        
        prices = []
        for pattern in price_patterns:
            matches = re.findall(pattern, html_content, re.IGNORECASE)
            for match in matches:
                try:
                    # Clean and convert price
                    price_str = match.replace('$', '').replace(',', '')
                    price = float(price_str)
                    
                    # Filter reasonable price ranges
                    if 100 <= price <= 10000:
                        prices.append(price)
                except ValueError:
                    continue
        
        # Extract location-specific information
        location_info = self._extract_location_info(html_content, location)
        
        # Calculate statistics
        if prices:
            avg_price = sum(prices) / len(prices)
            min_price = min(prices)
            max_price = max(prices)
            
            # Create price ranges
            budget_price = min_price * 1.1  # 10% above minimum
            luxury_price = max_price * 0.9  # 10% below maximum
        else:
            # Fallback pricing
            avg_price, min_price, max_price = self._get_location_defaults(location, duration_days)
            budget_price = avg_price * 0.8
            luxury_price = avg_price * 1.3
        
        return {
            'location': location,
            'duration_days': duration_days,
            'pricing': {
                'average_price': round(avg_price, 2),
                'min_price': round(min_price, 2),
                'max_price': round(max_price, 2),
                'budget_price': round(budget_price, 2),
                'luxury_price': round(luxury_price, 2),
                'price_per_day': round(avg_price / duration_days, 2),
                'sample_prices': sorted(prices[:10]) if prices else []
            },
            'location_info': location_info,
            'data_source': 'duckduckgo_search',
            'confidence': 'high' if len(prices) >= 3 else 'medium' if len(prices) >= 1 else 'low'
        }
    
    def _extract_location_info(self, html_content: str, location: str) -> Dict[str, Any]:
        """Extract location-specific information from search results"""
        
        # Look for common dive trip information
        info_patterns = {
            'best_season': r'(?:best|peak)\s*(?:time|season)\s*(?:to\s*)?(?:dive|visit)\s*([^.,\n]+)',
            'difficulty': r'(?:difficulty|level|certification)[^:]*:\s*([^.,\n]+)',
            'visibility': r'(?:visibility|vis)[^:]*:\s*(\d+(?:\.\d+)?)\s*(?:m|meters|ft)',
            'water_temp': r'(?:water\s*temperature|temp)[^:]*:\s*(\d+(?:\.\d+)?)\s*(?:°|degrees?)',
            'marine_life': r'(?:marine\s*life|fish|coral|creatures)[^:]*:\s*([^.,\n]+)',
        }
        
        extracted_info = {}
        for key, pattern in info_patterns:
            matches = re.findall(pattern, html_content, re.IGNORECASE)
            if matches:
                extracted_info[key] = matches[0].strip()
        
        return extracted_info
    
    def _get_location_defaults(self, location: str, duration_days: int) -> tuple:
        """Get default pricing for location based on known averages"""
        
        # Known average pricing per day for popular dive destinations
        location_defaults = {
            'belize': (250, 180, 450),      # avg, min, max per day
            'red sea': (200, 150, 350),
            'great barrier reef': (300, 200, 500),
            'maldives': (350, 250, 600),
            'caribbean': (220, 160, 400),
            'thailand': (180, 120, 300),
            'indonesia': (200, 140, 350),
            'philippines': (170, 120, 280),
            'hawaii': (280, 200, 450),
            'florida': (190, 140, 320),
        }
        
        location_lower = location.lower()
        
        # Find matching location
        for key, (avg, min_price, max_price) in location_defaults.items():
            if key in location_lower:
                total_avg = avg * duration_days
                total_min = min_price * duration_days
                total_max = max_price * duration_days
                return total_avg, total_min, total_max
        
        # Default pricing if location not found
        default_avg = 220 * duration_days
        default_min = 150 * duration_days
        default_max = 380 * duration_days
        
        return default_avg, default_min, default_max
    
    def _get_fallback_pricing(self, location: str, duration_days: int) -> Dict[str, Any]:
        """Get fallback pricing when search fails"""
        
        avg_price, min_price, max_price = self._get_location_defaults(location, duration_days)
        
        return {
            'location': location,
            'duration_days': duration_days,
            'pricing': {
                'average_price': round(avg_price, 2),
                'min_price': round(min_price, 2),
                'max_price': round(max_price, 2),
                'budget_price': round(min_price * 1.1, 2),
                'luxury_price': round(max_price * 0.9, 2),
                'price_per_day': round(avg_price / duration_days, 2),
                'sample_prices': []
            },
            'location_info': {
                'note': 'Using default pricing estimates'
            },
            'data_source': 'fallback_estimates',
            'confidence': 'low'
        }
    
    def search_multiple_locations(self, locations: List[str], duration_days: int = 7) -> List[Dict[str, Any]]:
        """Search pricing for multiple locations"""
        
        results = []
        for location in locations:
            try:
                result = self.search_dive_trip_pricing(location, duration_days)
                results.append(result)
                time.sleep(1)  # Rate limiting
            except Exception as e:
                print(f"Error searching for {location}: {e}")
                continue
        
        return results
    
    def get_trip_components_pricing(self, location: str, duration_days: int) -> Dict[str, Any]:
        """Get detailed pricing breakdown for trip components"""
        
        base_pricing = self.search_dive_trip_pricing(location, duration_days)
        
        # Component breakdown estimates
        components = {
            'accommodation': {
                'percentage': 35,
                'estimated_cost': round(base_pricing['pricing']['average_price'] * 0.35, 2)
            },
            'diving': {
                'percentage': 25,
                'estimated_cost': round(base_pricing['pricing']['average_price'] * 0.25, 2)
            },
            'meals': {
                'percentage': 20,
                'estimated_cost': round(base_pricing['pricing']['average_price'] * 0.20, 2)
            },
            'transportation': {
                'percentage': 15,
                'estimated_cost': round(base_pricing['pricing']['average_price'] * 0.15, 2)
            },
            'equipment': {
                'percentage': 5,
                'estimated_cost': round(base_pricing['pricing']['average_price'] * 0.05, 2)
            }
        }
        
        base_pricing['pricing']['components'] = components
        
        return base_pricing


# Global search service instance
search_service = DuckDuckGoSearchService()

def search_dive_pricing(location: str, duration_days: int = 7) -> Dict[str, Any]:
    """Convenience function to search dive trip pricing"""
    return search_service.search_dive_trip_pricing(location, duration_days)

def get_trip_cost_breakdown(location: str, duration_days: int = 7) -> Dict[str, Any]:
    """Convenience function to get detailed trip cost breakdown"""
    return search_service.get_trip_components_pricing(location, duration_days)
