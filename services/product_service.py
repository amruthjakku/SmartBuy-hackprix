import os
import requests
import json
from typing import Dict, List, Any

class ProductService:
    def __init__(self):
        self.rapidapi_key = os.getenv("RAPIDAPI_KEY")
        self.google_shopping_key = os.getenv("GOOGLE_SHOPPING_API_KEY")
        
    def search_products(self, requirements: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Search for products based on user requirements"""
        
        # For hackathon demo, return mock data first
        # You can replace this with real API calls later
        mock_products = self._get_mock_products(requirements)
        
        # Uncomment below to enable real API calls
        # real_products = self._search_real_products(requirements)
        # return real_products
        
        return mock_products
    
    def _get_mock_products(self, requirements: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate mock products for demo purposes"""
        
        category = requirements.get("category", "laptop")
        budget = requirements.get("budget", 50000)
        use_case = requirements.get("use_case", ["general"])
        
        if "laptop" in category.lower():
            return [
                {
                    "name": "ASUS TUF Gaming F15",
                    "price": 55999,
                    "original_price": 65999,
                    "platform": "Amazon",
                    "rating": 4.3,
                    "reviews": 1250,
                    "key_features": [
                        "Intel Core i5 11th Gen",
                        "GTX 1650 4GB Graphics",
                        "8GB RAM, 512GB SSD",
                        "15.6'' Full HD Display"
                    ],
                    "pros": ["Good gaming performance", "Solid build quality", "Good cooling"],
                    "cons": ["Average battery life", "Heavy weight"],
                    "image_url": "https://example.com/asus-tuf.jpg",
                    "product_url": "https://amazon.in/product1",
                    "availability": "In Stock"
                },
                {
                    "name": "HP Pavilion Gaming 15",
                    "price": 52999,
                    "original_price": 58999,
                    "platform": "Flipkart",
                    "rating": 4.1,
                    "reviews": 890,
                    "key_features": [
                        "AMD Ryzen 5 4600H",
                        "GTX 1650 4GB Graphics", 
                        "8GB RAM, 1TB HDD + 256GB SSD",
                        "15.6'' Full HD IPS Display"
                    ],
                    "pros": ["Good price-performance", "Decent display", "Upgradeable RAM"],
                    "cons": ["Plastic build", "Average keyboard"],
                    "image_url": "https://example.com/hp-pavilion.jpg", 
                    "product_url": "https://flipkart.com/product2",
                    "availability": "In Stock"
                },
                {
                    "name": "Lenovo IdeaPad Gaming 3",
                    "price": 58999,
                    "original_price": 62999,
                    "platform": "Amazon",
                    "rating": 4.2,
                    "reviews": 756,
                    "key_features": [
                        "AMD Ryzen 5 5600H",
                        "RTX 3050 4GB Graphics",
                        "8GB RAM, 512GB SSD",
                        "15.6'' Full HD 120Hz Display"
                    ],
                    "pros": ["120Hz display", "Latest RTX graphics", "Good performance"],
                    "cons": ["Average build quality", "Gets hot under load"],
                    "image_url": "https://example.com/lenovo-gaming3.jpg",
                    "product_url": "https://amazon.in/product3", 
                    "availability": "Limited Stock"
                }
            ]
        
        elif "phone" in category.lower() or "smartphone" in category.lower():
            return [
                {
                    "name": "Samsung Galaxy M34 5G",
                    "price": 18999,
                    "original_price": 24999,
                    "platform": "Amazon",
                    "rating": 4.2,
                    "reviews": 2340,
                    "key_features": [
                        "Exynos 1280 Processor",
                        "6GB RAM, 128GB Storage",
                        "50MP Triple Camera",
                        "6.6'' Super AMOLED Display",
                        "6000mAh Battery"
                    ],
                    "pros": ["Excellent battery life", "Good display", "Decent cameras"],
                    "cons": ["Average performance", "Slow charging"],
                    "image_url": "https://example.com/samsung-m34.jpg",
                    "product_url": "https://amazon.in/samsung-m34",
                    "availability": "In Stock"
                }
            ]
        
        # Default return for other categories
        return [
            {
                "name": f"Sample {category.title()}",
                "price": budget - 5000,
                "original_price": budget,
                "platform": "Amazon",
                "rating": 4.0,
                "reviews": 100,
                "key_features": ["Feature 1", "Feature 2", "Feature 3"],
                "pros": ["Pro 1", "Pro 2"],
                "cons": ["Con 1"],
                "image_url": "https://example.com/sample.jpg",
                "product_url": "https://example.com/product",
                "availability": "In Stock"
            }
        ]
    
    def _search_real_products(self, requirements: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Search real products using APIs (for later implementation)"""
        
        products = []
        
        # Add Amazon search
        amazon_products = self._search_amazon(requirements)
        products.extend(amazon_products)
        
        # Add Flipkart search  
        flipkart_products = self._search_flipkart(requirements)
        products.extend(flipkart_products)
        
        # Sort by relevance/price
        products = sorted(products, key=lambda x: x.get('price', 0))
        
        return products[:10]  # Return top 10 results
    
    def _search_amazon(self, requirements: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Search Amazon using RapidAPI"""
        
        try:
            url = "https://amazon-products1.p.rapidapi.com/search"
            
            # Build search query
            query = self._build_search_query(requirements)
            
            params = {
                "query": query,
                "country": "IN"  # India
            }
            
            headers = {
                "X-RapidAPI-Key": self.rapidapi_key,
                "X-RapidAPI-Host": "amazon-products1.p.rapidapi.com"
            }
            
            response = requests.get(url, headers=headers, params=params, timeout=10)
            data = response.json()
            
            # Parse Amazon response to standard format
            return self._parse_amazon_response(data)
            
        except Exception as e:
            print(f"Amazon search error: {e}")
            return []
    
    def _search_flipkart(self, requirements: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Search Flipkart using RapidAPI"""
        
        try:
            # Implementation for Flipkart API
            # Similar to Amazon search
            pass
            
        except Exception as e:
            print(f"Flipkart search error: {e}")
            return []
    
    def _build_search_query(self, requirements: Dict[str, Any]) -> str:
        """Build search query from requirements"""
        
        query_parts = []
        
        if "category" in requirements:
            query_parts.append(requirements["category"])
            
        if "use_case" in requirements:
            use_cases = requirements["use_case"]
            if isinstance(use_cases, list):
                query_parts.extend(use_cases)
            else:
                query_parts.append(use_cases)
        
        return " ".join(query_parts)
    
    def _parse_amazon_response(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Parse Amazon API response to standard format"""
        
        products = []
        
        # Implementation depends on the actual API response structure
        # This is a placeholder
        
        return products