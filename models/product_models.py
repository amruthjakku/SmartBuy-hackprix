"""
Advanced Product Models for Intelligent Product Discovery Platform
"""
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import random

@dataclass
class ReviewSummary:
    """Intelligent review analysis"""
    overall_rating: float
    total_reviews: int
    category_ratings: Dict[str, float]  # performance: 4.2, battery: 3.8, etc.
    pros_summary: List[str]
    cons_summary: List[str]
    common_complaints: List[str]
    common_praise: List[str]
    reviewer_demographics: Dict[str, Any]  # age groups, use cases, etc.

@dataclass
class PriceHistory:
    """Price tracking and analysis"""
    current_price: float
    original_price: float
    price_history: List[Dict[str, Any]]  # date, price, platform
    lowest_price_ever: float
    highest_price_ever: float
    price_trend: str  # "increasing", "decreasing", "stable"
    discount_percentage: float
    is_good_deal: bool
    price_drop_alerts: List[str]
    seasonal_patterns: Dict[str, float]  # festival discounts, etc.

@dataclass
class ProductIntelligence:
    """Comprehensive product intelligence"""
    id: str
    name: str
    category: str
    brand: str
    model: str
    
    # Basic Info
    key_features: List[str]
    specifications: Dict[str, Any]
    images: List[str]
    
    # Pricing Intelligence
    price_info: PriceHistory
    platform_prices: Dict[str, Dict[str, Any]]  # platform: {price, availability, offers}
    
    # Review Intelligence
    review_analysis: ReviewSummary
    
    # Availability & Policy
    stock_status: Dict[str, str]  # platform: status
    warranty_info: Dict[str, str]
    return_policies: Dict[str, Dict[str, Any]]
    
    # Intelligence Scores
    value_score: float  # calculated based on price/features/reviews
    popularity_score: float
    deal_score: float  # how good the current deal is
    
    # Alternatives & Comparisons
    similar_products: List[str]  # product IDs
    better_alternatives: List[Dict[str, Any]]
    cheaper_alternatives: List[Dict[str, Any]]
    
    # Time Intelligence
    best_time_to_buy: str
    seasonal_advice: str
    urgency_score: int  # 1-10, how urgent it is to buy now

@dataclass
class ConversationContext:
    """Enhanced conversation memory and context"""
    session_id: str
    user_id: Optional[str]
    start_time: datetime
    
    # Requirements Evolution
    requirements_history: List[Dict[str, Any]]
    current_requirements: Dict[str, Any]
    clarification_history: List[Dict[str, Any]]
    
    # User Preferences Learning
    priority_rankings: Dict[str, int]  # feature: importance (1-10)
    deal_breakers: List[str]
    nice_to_haves: List[str]
    budget_flexibility: str  # "strict", "flexible", "very_flexible"
    
    # Conversation Intelligence
    user_expertise_level: str  # "beginner", "intermediate", "expert"
    education_needed: List[str]  # topics user needs to learn about
    contradictions_resolved: List[Dict[str, Any]]
    
    # Personalization
    past_searches: List[Dict[str, Any]]
    purchase_patterns: Dict[str, Any]
    preferred_brands: List[str]
    avoided_brands: List[str]

@dataclass
class SmartRecommendation:
    """Intelligent recommendation with reasoning"""
    product: ProductIntelligence
    match_score: float  # how well it matches user requirements
    reasoning: List[str]  # why this product is recommended
    trade_offs: Dict[str, str]  # feature: trade-off explanation
    confidence: float  # how confident the AI is about this recommendation
    
    # Deal Intelligence
    deal_highlights: List[str]
    savings_amount: float
    urgency_factors: List[str]  # "price dropped 15%", "limited stock", etc.
    
    # Alternative Context
    why_better_than_alternatives: List[str]
    what_you_might_miss: List[str]  # if they choose cheaper alternatives

class ProductDatabase:
    """Mock intelligent product database"""
    
    def __init__(self):
        self.products = self._generate_mock_products()
        self.price_histories = self._generate_price_histories()
        self.review_data = self._generate_review_intelligence()
    
    def _generate_mock_products(self) -> List[ProductIntelligence]:
        """Generate comprehensive mock product data"""
        products = []
        
        # Smartwatches
        smartwatches = [
            {
                "name": "Amazfit GTS 2 Mini",
                "brand": "Amazfit",
                "model": "GTS 2 Mini",
                "key_features": [
                    "1.55\" AMOLED Display",
                    "14-day Battery Life",
                    "70+ Sports Modes",
                    "Sleep & Stress Monitoring",
                    "GPS Built-in",
                    "5ATM Water Resistance"
                ],
                "specifications": {
                    "display": "1.55\" AMOLED",
                    "battery": "14 days",
                    "sensors": "Heart Rate, SpO2, Sleep",
                    "connectivity": "Bluetooth 5.0",
                    "water_resistance": "5ATM",
                    "weight": "19.5g",
                    "os": "Zepp OS"
                }
            },
            {
                "name": "Realme Watch S Pro",
                "brand": "Realme",
                "model": "Watch S Pro",
                "key_features": [
                    "1.39\" AMOLED Display",
                    "14-day Battery Life",
                    "15 Sports Modes",
                    "Heart Rate Monitoring",
                    "GPS + GLONASS",
                    "IP68 Water Resistance"
                ],
                "specifications": {
                    "display": "1.39\" AMOLED",
                    "battery": "14 days",
                    "sensors": "Heart Rate, SpO2",
                    "connectivity": "Bluetooth 5.0",
                    "water_resistance": "IP68",
                    "weight": "63g",
                    "os": "Realme UI"
                }
            },
            {
                "name": "Fire-Boltt Phoenix Pro",
                "brand": "Fire-Boltt",
                "model": "Phoenix Pro",
                "key_features": [
                    "1.39\" HD Display",
                    "7-day Battery Life",
                    "120+ Sports Modes",
                    "Bluetooth Calling",
                    "Health Monitoring",
                    "IP67 Water Resistance"
                ],
                "specifications": {
                    "display": "1.39\" HD",
                    "battery": "7 days",
                    "sensors": "Heart Rate, SpO2, Sleep",
                    "connectivity": "Bluetooth Calling",
                    "water_resistance": "IP67",
                    "weight": "52g",
                    "os": "Fire-Boltt OS"
                }
            }
        ]
        
        # Gaming Laptops
        gaming_laptops = [
            {
                "name": "ASUS TUF Gaming F15",
                "brand": "ASUS",
                "model": "FX506LH-HN258W",
                "key_features": [
                    "Intel Core i5-10300H Processor",
                    "NVIDIA GeForce GTX 1650 4GB",
                    "8GB DDR4 3200MHz RAM",
                    "512GB PCIe SSD",
                    "15.6\" FHD 144Hz Display",
                    "RGB Backlit Keyboard"
                ],
                "specifications": {
                    "processor": "Intel Core i5-10300H",
                    "graphics": "NVIDIA GTX 1650 4GB",
                    "ram": "8GB DDR4",
                    "storage": "512GB SSD",
                    "display": "15.6\" FHD 144Hz",
                    "weight": "2.3 kg",
                    "battery": "48WHrs",
                    "os": "Windows 11"
                }
            },
            {
                "name": "HP Pavilion Gaming 15",
                "brand": "HP",
                "model": "15-dk2018TX",
                "key_features": [
                    "Intel Core i5-11300H Processor",
                    "NVIDIA GeForce GTX 1650 4GB",
                    "8GB DDR4 RAM",
                    "1TB HDD + 256GB SSD",
                    "15.6\" FHD IPS Display",
                    "B&O Audio"
                ],
                "specifications": {
                    "processor": "Intel Core i5-11300H",
                    "graphics": "NVIDIA GTX 1650 4GB",
                    "ram": "8GB DDR4",
                    "storage": "1TB HDD + 256GB SSD",
                    "display": "15.6\" FHD IPS",
                    "weight": "2.25 kg",
                    "battery": "52.5WHrs",
                    "os": "Windows 11"
                }
            },
            {
                "name": "Lenovo IdeaPad Gaming 3",
                "brand": "Lenovo",
                "model": "15ACH6",
                "key_features": [
                    "AMD Ryzen 5 5600H Processor",
                    "NVIDIA GeForce RTX 3050 4GB",
                    "8GB DDR4 RAM",
                    "512GB SSD",
                    "15.6\" FHD 120Hz Display",
                    "Legion TrueStrike Keyboard"
                ],
                "specifications": {
                    "processor": "AMD Ryzen 5 5600H",
                    "graphics": "NVIDIA RTX 3050 4GB",
                    "ram": "8GB DDR4",
                    "storage": "512GB SSD",
                    "display": "15.6\" FHD 120Hz",
                    "weight": "2.25 kg",
                    "battery": "45WHrs",
                    "os": "Windows 11"
                }
            }
        ]
        
        # Process smartwatches
        for i, watch_data in enumerate(smartwatches):
            product = ProductIntelligence(
                id=f"smartwatch_{i+1}",
                name=watch_data["name"],
                category="smartwatches",
                brand=watch_data["brand"],
                model=watch_data["model"],
                key_features=watch_data["key_features"],
                specifications=watch_data["specifications"],
                images=[f"https://example.com/smartwatch_{i+1}.jpg"],
                
                # Will be populated by other methods
                price_info=None,
                platform_prices={},
                review_analysis=None,
                stock_status={},
                warranty_info={},
                return_policies={},
                value_score=0.0,
                popularity_score=0.0,
                deal_score=0.0,
                similar_products=[],
                better_alternatives=[],
                cheaper_alternatives=[],
                best_time_to_buy="",
                seasonal_advice="",
                urgency_score=0
            )
            products.append(product)
        
        # Process gaming laptops
        for i, laptop_data in enumerate(gaming_laptops):
            product = ProductIntelligence(
                id=f"laptop_{i+1}",
                name=laptop_data["name"],
                category="gaming laptops",
                brand=laptop_data["brand"],
                model=laptop_data["model"],
                key_features=laptop_data["key_features"],
                specifications=laptop_data["specifications"],
                images=[f"https://example.com/laptop_{i+1}.jpg"],
                
                # Will be populated by other methods
                price_info=None,
                platform_prices={},
                review_analysis=None,
                stock_status={},
                warranty_info={},
                return_policies={},
                value_score=0.0,
                popularity_score=0.0,
                deal_score=0.0,
                similar_products=[],
                better_alternatives=[],
                cheaper_alternatives=[],
                best_time_to_buy="",
                seasonal_advice="",
                urgency_score=0
            )
            products.append(product)
        
        return products
    
    def _generate_price_histories(self) -> Dict[str, PriceHistory]:
        """Generate mock price history data"""
        histories = {}
        
        # Base prices for smartwatches and laptops
        smartwatch_prices = [4999, 5999, 3999]  # Base prices for 3 smartwatches
        laptop_prices = [55999, 52999, 58999]  # Base prices for 3 laptops
        all_prices = smartwatch_prices + laptop_prices
        all_ids = [f"smartwatch_{i+1}" for i in range(3)] + [f"laptop_{i+1}" for i in range(3)]
        
        for i, base_price in enumerate(all_prices):
            product_id = all_ids[i]
            
            # Generate price history for last 6 months
            history = []
            current_date = datetime.now()
            
            for days_ago in range(180, 0, -7):  # Weekly data points
                date = current_date - timedelta(days=days_ago)
                # Add some realistic price variation
                price_variation = random.uniform(0.9, 1.15)
                price = int(base_price * price_variation)
                
                history.append({
                    "date": date.isoformat(),
                    "price": price,
                    "platform": random.choice(["Amazon", "Flipkart", "Croma"])
                })
            
            lowest = min(h["price"] for h in history)
            highest = max(h["price"] for h in history)
            current = base_price
            original = int(base_price * 1.1)
            
            histories[product_id] = PriceHistory(
                current_price=current,
                original_price=original,
                price_history=history,
                lowest_price_ever=lowest,
                highest_price_ever=highest,
                price_trend="decreasing" if current < sum(h["price"] for h in history[-4:]) / 4 else "stable",
                discount_percentage=((original - current) / original) * 100,
                is_good_deal=current <= lowest * 1.05,  # Within 5% of lowest price
                price_drop_alerts=[
                    f"Price dropped ₹{original - current:,} in last month!",
                    "Currently at 15% discount from original price"
                ] if current < original else [],
                seasonal_patterns={
                    "diwali": 0.85,  # 15% discount during Diwali
                    "new_year": 0.9,  # 10% discount during New Year
                    "summer": 0.95   # 5% discount during summer sales
                }
            )
        
        return histories
    
    def _generate_review_intelligence(self) -> Dict[str, ReviewSummary]:
        """Generate mock review intelligence"""
        reviews = {}
        
        # Smartwatch review data
        smartwatch_review_data = [
            {
                "overall": 4.2,
                "total": 890,
                "categories": {
                    "battery_life": 4.6,
                    "build_quality": 4.1,
                    "display": 4.3,
                    "fitness_tracking": 4.4,
                    "connectivity": 4.0,
                    "value_for_money": 4.5
                },
                "pros": [
                    "Excellent battery life - lasts 2 weeks",
                    "Beautiful AMOLED display",
                    "Accurate fitness tracking",
                    "Great value for money"
                ],
                "cons": [
                    "Limited app ecosystem",
                    "GPS can be slow to connect",
                    "No Google Pay support"
                ],
                "complaints": [
                    "App store is limited",
                    "Notifications can be delayed",
                    "GPS accuracy issues"
                ],
                "praise": [
                    "Amazing battery life",
                    "Great for fitness tracking",
                    "Excellent value",
                    "Comfortable to wear"
                ]
            },
            {
                "overall": 4.0,
                "total": 650,
                "categories": {
                    "battery_life": 4.2,
                    "build_quality": 3.9,
                    "display": 4.1,
                    "fitness_tracking": 4.3,
                    "connectivity": 3.8,
                    "value_for_money": 4.2
                },
                "pros": [
                    "Good battery life",
                    "Solid fitness features",
                    "Responsive touch screen",
                    "Decent build quality"
                ],
                "cons": [
                    "Software can be buggy",
                    "Limited customization",
                    "Average app support"
                ],
                "complaints": [
                    "Software updates are slow",
                    "Limited watch faces",
                    "Connectivity issues"
                ],
                "praise": [
                    "Good fitness tracking",
                    "Decent battery life",
                    "Nice display",
                    "Comfortable design"
                ]
            },
            {
                "overall": 3.8,
                "total": 420,
                "categories": {
                    "battery_life": 3.5,
                    "build_quality": 3.6,
                    "display": 4.0,
                    "fitness_tracking": 4.1,
                    "connectivity": 4.2,
                    "value_for_money": 4.3
                },
                "pros": [
                    "Bluetooth calling feature",
                    "Many sports modes",
                    "Good value for price",
                    "Decent display quality"
                ],
                "cons": [
                    "Battery life could be better",
                    "Build feels plasticky",
                    "Limited smartwatch features"
                ],
                "complaints": [
                    "Short battery life",
                    "Cheap build quality",
                    "Call quality is average"
                ],
                "praise": [
                    "Great value for money",
                    "Bluetooth calling works",
                    "Many fitness modes",
                    "Easy to use"
                ]
            }
        ]
        
        # Laptop review data
        laptop_review_data = [
            {
                "overall": 4.3,
                "total": 1250,
                "categories": {
                    "performance": 4.5,
                    "build_quality": 4.2,
                    "battery_life": 3.8,
                    "display": 4.4,
                    "keyboard": 4.1,
                    "value_for_money": 4.6
                },
                "pros": [
                    "Excellent gaming performance for the price",
                    "Solid build quality with military-grade certification",
                    "Good thermal management",
                    "Beautiful RGB keyboard"
                ],
                "cons": [
                    "Battery life could be better for non-gaming tasks",
                    "Can get loud under heavy load",
                    "Limited port selection"
                ],
                "complaints": [
                    "Fan noise during gaming",
                    "Average battery backup",
                    "Heating issues during extended gaming"
                ],
                "praise": [
                    "Great value for money",
                    "Smooth gaming experience",
                    "Sturdy build quality",
                    "Good customer service"
                ]
            },
            {
                "overall": 4.1,
                "total": 890,
                "categories": {
                    "performance": 4.3,
                    "build_quality": 4.0,
                    "battery_life": 4.2,
                    "display": 4.1,
                    "keyboard": 3.9,
                    "value_for_money": 4.4
                },
                "pros": [
                    "Good battery life for a gaming laptop",
                    "Decent performance for casual gaming",
                    "B&O audio sounds great",
                    "Dual storage setup is convenient"
                ],
                "cons": [
                    "Build quality feels plasticky",
                    "Keyboard could be better",
                    "Display colors are okay but not vibrant"
                ],
                "complaints": [
                    "Plastic build feels cheap",
                    "Keyboard backlight is uneven",
                    "Customer service issues"
                ],
                "praise": [
                    "Good battery life",
                    "Decent gaming performance",
                    "Audio quality is impressive",
                    "Storage combination works well"
                ]
            },
            {
                "overall": 4.2,
                "total": 756,
                "categories": {
                    "performance": 4.6,
                    "build_quality": 4.1,
                    "battery_life": 3.7,
                    "display": 4.3,
                    "keyboard": 4.4,
                    "value_for_money": 4.5
                },
                "pros": [
                    "RTX 3050 provides excellent 1080p gaming",
                    "AMD Ryzen processor is very efficient",
                    "120Hz display makes gaming smooth",
                    "Excellent keyboard for typing and gaming"
                ],
                "cons": [
                    "Battery drains quickly while gaming",
                    "Limited upgrade options",
                    "Can throttle under sustained load"
                ],
                "complaints": [
                    "Poor battery life during gaming",
                    "Thermal throttling issues",
                    "Limited RAM upgrade slots"
                ],
                "praise": [
                    "Outstanding gaming performance",
                    "Great display quality",
                    "Comfortable keyboard",
                    "Good value with RTX graphics"
                ]
            }
        ]
        
        # Process smartwatch reviews
        for i, data in enumerate(smartwatch_review_data):
            product_id = f"smartwatch_{i+1}"
            reviews[product_id] = ReviewSummary(
                overall_rating=data["overall"],
                total_reviews=data["total"],
                category_ratings=data["categories"],
                pros_summary=data["pros"],
                cons_summary=data["cons"],
                common_complaints=data["complaints"],
                common_praise=data["praise"],
                reviewer_demographics={
                    "age_groups": {"18-25": 20, "26-35": 40, "36-45": 25, "45+": 15},
                    "use_cases": {"fitness": 70, "smart_features": 20, "fashion": 10},
                    "experience_level": {"beginner": 40, "intermediate": 45, "expert": 15}
                }
            )
        
        # Process laptop reviews
        for i, data in enumerate(laptop_review_data):
            product_id = f"laptop_{i+1}"
            reviews[product_id] = ReviewSummary(
                overall_rating=data["overall"],
                total_reviews=data["total"],
                category_ratings=data["categories"],
                pros_summary=data["pros"],
                cons_summary=data["cons"],
                common_complaints=data["complaints"],
                common_praise=data["praise"],
                reviewer_demographics={
                    "age_groups": {"18-25": 35, "26-35": 45, "36-45": 15, "45+": 5},
                    "use_cases": {"gaming": 60, "work": 25, "study": 15},
                    "experience_level": {"beginner": 30, "intermediate": 50, "expert": 20}
                }
            )
        
        return reviews
    
    def get_products_with_intelligence(self, category: str = None, budget_max: float = None) -> List[ProductIntelligence]:
        """Get products with full intelligence data"""
        filtered_products = []
        
        for product in self.products:
            if category and product.category != category:
                continue
            
            # Populate intelligence data
            product.price_info = self.price_histories.get(product.id)
            product.review_analysis = self.review_data.get(product.id)
            
            # Generate platform prices
            base_price = product.price_info.current_price if product.price_info else 50000
            product.platform_prices = {
                "Amazon": {
                    "price": base_price,
                    "availability": "In Stock",
                    "offers": ["5% cashback with Amazon Pay", "No-cost EMI available"],
                    "delivery": "Free delivery by tomorrow"
                },
                "Flipkart": {
                    "price": int(base_price * random.uniform(0.98, 1.03)),
                    "availability": "In Stock" if random.random() > 0.2 else "Limited Stock",
                    "offers": ["10% instant discount with Axis Bank cards", "Exchange offer available"],
                    "delivery": "Free delivery in 2-3 days"
                },
                "Croma": {
                    "price": int(base_price * random.uniform(1.02, 1.08)),
                    "availability": "Available" if random.random() > 0.3 else "Check availability",
                    "offers": ["Store pickup available", "Extended warranty options"],
                    "delivery": "Delivery in 3-5 days"
                }
            }
            
            # Stock status
            product.stock_status = {
                platform: data["availability"] 
                for platform, data in product.platform_prices.items()
            }
            
            # Warranty and return policies
            product.warranty_info = {
                "manufacturer": "1 year international warranty",
                "extended": "Extended warranty available up to 3 years",
                "onsite": "On-site service for premium models"
            }
            
            product.return_policies = {
                "Amazon": {"window": "30 days", "condition": "Original packaging required"},
                "Flipkart": {"window": "7 days", "condition": "Physical damage covered"},
                "Croma": {"window": "15 days", "condition": "Store credit for returns"}
            }
            
            # Calculate intelligence scores
            if product.review_analysis:
                product.value_score = (
                    product.review_analysis.category_ratings.get("value_for_money", 4.0) * 2 +
                    product.review_analysis.category_ratings.get("performance", 4.0) +
                    (5.0 - (base_price / 15000))  # Price factor
                ) / 4
                
                product.popularity_score = min(5.0, product.review_analysis.total_reviews / 200)
            
            if product.price_info:
                product.deal_score = product.price_info.discount_percentage / 20  # Max 5.0 for 100% discount
            
            # Time intelligence
            product.best_time_to_buy = "Good time to buy - prices are stable and near historical low"
            product.seasonal_advice = "Diwali sales typically offer 10-15% additional discounts"
            product.urgency_score = 7 if product.price_info and product.price_info.is_good_deal else 4
            
            if budget_max and base_price <= budget_max:
                filtered_products.append(product)
            elif not budget_max:
                filtered_products.append(product)
        
        return filtered_products