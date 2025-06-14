"""
Advanced Conversational Intelligence for Product Discovery
"""
from typing import Dict, List, Optional, Any, Tuple
import json
import re
from datetime import datetime
from models.product_models import ConversationContext, ProductDatabase, SmartRecommendation

class IntelligentChatbot:
    """
    Advanced chatbot with deep requirement mining, contradiction resolution,
    and educational shopping capabilities
    """
    
    def __init__(self):
        self.product_db = ProductDatabase()
        self.conversations: Dict[str, ConversationContext] = {}
        
        # Priority ranking options for different categories
        self.priority_options = {
            "gaming laptops": [
                "Performance (GPU/CPU power)",
                "Display quality (refresh rate, color accuracy)",
                "Build quality and durability", 
                "Battery life",
                "Portability (weight, thickness)",
                "Price/Value for money",
                "Keyboard and trackpad quality",
                "Thermal management (cooling)",
                "Upgrade options (RAM, storage)",
                "Brand reputation and support"
            ],
            "smartphones": [
                "Camera quality",
                "Battery life", 
                "Performance (processor, RAM)",
                "Display quality",
                "Build quality and design",
                "Price/Value for money",
                "Software experience (OS, updates)",
                "Storage capacity",
                "Brand reputation",
                "Special features (wireless charging, etc.)"
            ]
        }
        
        # Educational content for different user levels
        self.educational_content = {
            "gaming laptops": {
                "beginner": {
                    "gpu_importance": "GPU (Graphics Card) is the most important component for gaming. Higher numbers like RTX 3060 > GTX 1650 mean better gaming performance.",
                    "refresh_rate": "Higher refresh rate (120Hz, 144Hz) makes games look smoother, especially in fast-paced games like shooters.",
                    "thermal_throttling": "Gaming laptops can slow down when they get too hot. Good cooling prevents this 'thermal throttling'."
                },
                "intermediate": {
                    "gpu_tiers": "Entry: GTX 1650 (1080p medium), Mid: RTX 3050/3060 (1080p high), High: RTX 3070+ (1080p ultra/1440p)",
                    "cpu_gpu_balance": "Don't pair a weak CPU with powerful GPU or vice versa. Balance is key for optimal performance.",
                    "ram_speed": "Gaming benefits from faster RAM. 3200MHz DDR4 is good, avoid slower speeds."
                }
            }
        }
    
    def start_conversation(self, session_id: str, initial_message: str) -> Dict[str, Any]:
        """Start a new intelligent conversation"""
        
        # Create conversation context
        context = ConversationContext(
            session_id=session_id,
            user_id=None,
            start_time=datetime.now(),
            requirements_history=[],
            current_requirements={},
            clarification_history=[],
            priority_rankings={},
            deal_breakers=[],
            nice_to_haves=[],
            budget_flexibility="unknown",
            user_expertise_level="unknown",
            education_needed=[],
            contradictions_resolved=[],
            past_searches=[],
            purchase_patterns={},
            preferred_brands=[],
            avoided_brands=[]
        )
        
        self.conversations[session_id] = context
        
        # Process initial message
        return self.process_message(session_id, initial_message)
    
    def process_message(self, session_id: str, message: str) -> Dict[str, Any]:
        """Process user message with advanced intelligence"""
        
        if session_id not in self.conversations:
            return self.start_conversation(session_id, message)
        
        context = self.conversations[session_id]
        
        # Extract requirements from message
        new_requirements = self._deep_requirement_extraction(message, context)
        
        # Update context
        context.requirements_history.append({
            "timestamp": datetime.now().isoformat(),
            "message": message,
            "extracted": new_requirements
        })
        
        # Merge requirements intelligently
        context.current_requirements.update(new_requirements)
        
        # Debug: Show what we extracted
        print(f"DEBUG: Message: '{message}'")
        print(f"DEBUG: Extracted: {new_requirements}")
        print(f"DEBUG: Current requirements: {context.current_requirements}")
        
        # Detect contradictions
        contradictions = self._detect_contradictions(context.current_requirements)
        
        if contradictions:
            return self._handle_contradictions(context, contradictions)
        
        # Determine next conversation step
        next_step = self._determine_conversation_strategy(context)
        print(f"DEBUG: Next step: {next_step}")
        
        if next_step["type"] == "ready_to_search":
            return self._create_intelligent_recommendations(context)
        elif next_step["type"] == "category_clarification":
            return {
                "response": "I'd be happy to help you find the perfect product! What type of product are you looking for? (e.g., laptop, smartphone, headphones, smartwatch, etc.)",
                "type": "clarification",
                "requires_user_input": True
            }
        elif next_step["type"] == "budget_clarification":
            category = context.current_requirements.get("category", "product")
            return {
                "response": f"Great! You're looking for {category}. What's your budget range for this purchase?",
                "type": "clarification", 
                "requires_user_input": True
            }
        else:
            return self._create_clarification_response(context)
    
    def _deep_requirement_extraction(self, message: str, context: ConversationContext) -> Dict[str, Any]:
        """Advanced requirement extraction with context awareness"""
        
        requirements = {}
        message_lower = message.lower()
        
        # Enhanced category detection
        category_patterns = {
            "gaming laptop": ("gaming laptops", "gaming"),
            "gaming laptops": ("gaming laptops", "gaming"),
            "business laptop": ("laptops", "business"),
            "work laptop": ("laptops", "work"),
            "ultrabook": ("laptops", "ultraportable"),
            "laptop": ("laptops", None),
            "gaming phone": ("smartphones", "gaming"),
            "camera phone": ("smartphones", "photography"),
            "smartphone": ("smartphones", None),
            "phone": ("smartphones", None),
            "smartwatch": ("smartwatches", "fitness"),
            "smartwatches": ("smartwatches", "fitness"),
            "fitness watch": ("smartwatches", "fitness"),
            "smart watch": ("smartwatches", "fitness"),
            "headphones": ("headphones", "music"),
            "earphones": ("headphones", "music"),
            "earbuds": ("headphones", "music"),
            "wireless headphones": ("headphones", "music"),
            "bluetooth headphones": ("headphones", "music")
        }
        
        for pattern, (category, use_case) in category_patterns.items():
            if pattern in message_lower:
                requirements["category"] = category
                if use_case:
                    requirements["use_case"] = use_case
                break
        
        # Advanced budget extraction
        budget_patterns = [
            r"under[^\d]*₹?\s*(\d+)(?:k|thousand|,000)?",
            r"below[^\d]*₹?\s*(\d+)(?:k|thousand|,000)?", 
            r"₹\s*(\d+)(?:k|thousand|,000)?",
            r"budget[^\d]*₹?\s*(\d+)(?:k|thousand|,000)?",
            r"around[^\d]*₹?\s*(\d+)(?:k|thousand|,000)?",
            r"(\d+)(?:k|thousand|,000)?\s*budget",
            r"^(\d+)$",  # Just a number like "6000"
            r"^(\d+)k$",  # Number with k like "60k"
        ]
        
        for pattern in budget_patterns:
            match = re.search(pattern, message_lower)
            if match:
                budget_num = int(match.group(1))
                if 'k' in message_lower or 'thousand' in message_lower:
                    budget_num *= 1000
                elif budget_num < 1000:
                    budget_num *= 1000
                requirements["budget"] = budget_num
                
                # Determine budget flexibility from language
                if "under" in message_lower or "below" in message_lower:
                    requirements["budget_flexibility"] = "strict"
                elif "around" in message_lower or "approximately" in message_lower:
                    requirements["budget_flexibility"] = "flexible"
                break
        
        # Feature importance extraction
        importance_indicators = {
            "must have": ["essential", "must have", "need", "required", "important"],
            "nice to have": ["would like", "prefer", "nice to have", "bonus", "if possible"],
            "don't care": ["don't care", "doesn't matter", "not important"]
        }
        
        for importance, keywords in importance_indicators.items():
            for keyword in keywords:
                if keyword in message_lower:
                    # Extract what comes after these keywords
                    pattern = rf"{keyword}[:\s]+([^.!?]*)"
                    match = re.search(pattern, message_lower)
                    if match:
                        feature = match.group(1).strip()
                        requirements[f"{importance}_features"] = requirements.get(f"{importance}_features", []) + [feature]
        
        # Brand preferences
        brand_keywords = {
            "prefer": ["prefer", "like", "want", "love"],
            "avoid": ["don't like", "avoid", "hate", "bad experience"]
        }
        
        brands = ["asus", "hp", "dell", "lenovo", "acer", "msi", "apple", "samsung", "xiaomi", "oneplus"]
        
        for preference, keywords in brand_keywords.items():
            for keyword in keywords:
                if keyword in message_lower:
                    for brand in brands:
                        if brand in message_lower:
                            key = f"{preference}_brands"
                            requirements[key] = requirements.get(key, []) + [brand]
        
        # Extract use case (only if not already set by category)
        if "use_case" not in requirements:
            use_case_mappings = {
                "gaming": "gaming",
                "games": "gaming", 
                "work": "work",
                "business": "business",
                "office": "business",
                "study": "study",
                "student": "study",
                "photography": "photography",
                "photos": "photography",
                "video editing": "video editing",
                "editing": "video editing",
                "music": "music",
                "audio": "music",
                "fitness": "fitness",
                "exercise": "fitness"
            }
            
            for keyword, use_case in use_case_mappings.items():
                if keyword in message_lower:
                    requirements["use_case"] = use_case
                    break
        
        # Experience level detection
        beginner_indicators = ["new to", "first time", "don't know much", "beginner", "confused"]
        expert_indicators = ["expert", "advanced", "professional", "experienced", "technical"]
        
        if any(indicator in message_lower for indicator in beginner_indicators):
            requirements["expertise_level"] = "beginner"
        elif any(indicator in message_lower for indicator in expert_indicators):
            requirements["expertise_level"] = "expert"
        
        return requirements
    
    def _detect_contradictions(self, requirements: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Detect impossible or contradictory requirements"""
        
        contradictions = []
        
        # Budget vs Performance contradictions
        if requirements.get("budget") and requirements.get("category"):
            budget = requirements["budget"]
            category = requirements["category"]
            
            if category == "gaming laptops":
                if budget < 40000:
                    contradictions.append({
                        "type": "budget_performance",
                        "message": f"Gaming laptops under ₹{budget:,} typically have very limited gaming performance. Entry-level gaming usually starts around ₹45,000.",
                        "suggestions": [
                            f"Increase budget to ₹45,000-50,000 for basic gaming",
                            "Consider older/refurbished gaming laptops",
                            "Look at regular laptops with integrated graphics for light gaming"
                        ]
                    })
                elif budget > 200000:
                    contradictions.append({
                        "type": "budget_overkill",
                        "message": f"₹{budget:,} budget can get you professional gaming/workstation laptops. This might be overkill for casual gaming.",
                        "suggestions": [
                            "Consider what games you actually play",
                            "₹60,000-80,000 handles most games excellently",
                            "Invest saved money in accessories (monitor, keyboard, mouse)"
                        ]
                    })
        
        # Feature contradictions
        must_haves = requirements.get("must_have_features", [])
        if "long battery life" in " ".join(must_haves).lower() and "gaming" in requirements.get("use_case", ""):
            contradictions.append({
                "type": "feature_conflict",
                "message": "Gaming laptops typically have poor battery life during gaming (2-3 hours). Long battery life and gaming performance are conflicting requirements.",
                "suggestions": [
                    "Prioritize either gaming performance OR battery life",
                    "Consider laptops with hybrid graphics for better battery",
                    "Plan to use laptop plugged in for gaming"
                ]
            })
        
        return contradictions
    
    def _handle_contradictions(self, context: ConversationContext, contradictions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Handle contradictions intelligently"""
        
        contradiction = contradictions[0]  # Handle one at a time
        
        context.contradictions_resolved.append({
            "timestamp": datetime.now().isoformat(),
            "contradiction": contradiction,
            "status": "presented"
        })
        
        response = f"🤔 I notice there might be a conflict in your requirements:\n\n"
        response += f"**Issue:** {contradiction['message']}\n\n"
        response += "**Possible solutions:**\n"
        for i, suggestion in enumerate(contradiction['suggestions'], 1):
            response += f"{i}. {suggestion}\n"
        
        response += "\nWhich approach would you prefer? Or would you like me to explain more about these trade-offs?"
        
        return {
            "response": response,
            "type": "contradiction_resolution",
            "options": contradiction['suggestions'],
            "requires_user_input": True
        }
    
    def _determine_conversation_strategy(self, context: ConversationContext) -> Dict[str, str]:
        """Intelligently determine next conversation step"""
        
        reqs = context.current_requirements
        
        # Check if we have basic requirements
        has_category = "category" in reqs
        has_budget = "budget" in reqs
        
        # If we have both category and budget, we can proceed to search
        if has_category and has_budget:
            return {"type": "ready_to_search"}
        
        if not has_category:
            return {"type": "category_clarification"}
        
        if not has_budget:
            return {"type": "budget_clarification"}
        
        # Default to clarification if nothing else matches
        return {"type": "clarification"}
    
    def _create_priority_ranking_response(self, context: ConversationContext) -> Dict[str, Any]:
        """Create priority ranking interaction"""
        
        category = context.current_requirements.get("category", "laptops")
        priorities = self.priority_options.get(category, self.priority_options["gaming laptops"])
        
        context.clarification_history.append({
            "timestamp": datetime.now().isoformat(),
            "type": "priority_ranking",
            "options_presented": priorities
        })
        
        response = "🎯 **Let's understand what matters most to you!**\n\n"
        response += f"Please rank these features by importance (1 = most important):\n\n"
        
        for i, priority in enumerate(priorities[:6], 1):  # Show top 6 priorities
            response += f"**{i}.** {priority}\n"
        
        response += "\nYou can respond like: '1. Performance, 2. Price, 3. Battery life' or just tell me your top 3 priorities."
        
        return {
            "response": response,
            "type": "priority_ranking",
            "options": priorities,
            "requires_user_input": True
        }
    
    def _create_use_case_scenario_response(self, context: ConversationContext) -> Dict[str, Any]:
        """Create use case scenario interaction"""
        
        context.clarification_history.append({
            "timestamp": datetime.now().isoformat(),
            "type": "use_case_scenario"
        })
        
        response = "📋 **Help me understand your typical usage:**\n\n"
        response += "Walk me through a typical day with your new laptop:\n"
        response += "• How many hours will you use it?\n"
        response += "• Will you carry it around or mostly use at home?\n"
        response += "• What games/software will you run?\n"
        response += "• Any specific performance requirements?\n\n"
        response += "This helps me recommend the perfect balance of features for your needs!"
        
        return {
            "response": response,
            "type": "use_case_scenario",
            "requires_user_input": True
        }
    
    def _create_deal_breaker_response(self, context: ConversationContext) -> Dict[str, Any]:
        """Create deal breaker detection interaction"""
        
        context.clarification_history.append({
            "timestamp": datetime.now().isoformat(),
            "type": "deal_breaker_detection"
        })
        
        response = "🚫 **What are your absolute deal-breakers?**\n\n"
        response += "These are features that would make you immediately reject a laptop:\n\n"
        response += "Common deal-breakers:\n"
        response += "• Too heavy (over X kg)\n"
        response += "• Poor battery life (under X hours)\n"
        response += "• Specific brands to avoid\n"
        response += "• Loud fan noise\n"
        response += "• Poor build quality\n"
        response += "• No specific ports you need\n\n"
        response += "What would be deal-breakers for you?"
        
        return {
            "response": response,
            "type": "deal_breaker_detection",
            "requires_user_input": True
        }
    
    def _create_budget_reality_response(self, context: ConversationContext) -> Dict[str, Any]:
        """Create budget reality check"""
        
        reqs = context.current_requirements
        budget = reqs.get("budget", 0)
        category = reqs.get("category", "")
        
        # Estimate realistic cost based on requirements
        estimated_cost = self._estimate_realistic_cost(context)
        
        context.clarification_history.append({
            "timestamp": datetime.now().isoformat(),
            "type": "budget_reality_check",
            "budget_provided": budget,
            "estimated_cost": estimated_cost
        })
        
        if estimated_cost > budget * 1.2:  # 20% over budget
            response = f"💰 **Budget Reality Check**\n\n"
            response += f"Based on your requirements, similar {category} typically cost around **₹{estimated_cost:,}**, "
            response += f"which is about ₹{estimated_cost - budget:,} over your ₹{budget:,} budget.\n\n"
            response += "**Your options:**\n"
            response += f"1. **Increase budget** to ₹{estimated_cost:,} for your ideal requirements\n"
            response += f"2. **Adjust requirements** - I can suggest compromises to fit ₹{budget:,}\n"
            response += f"3. **Wait for sales** - prices drop by 10-15% during festival seasons\n\n"
            response += "What would you prefer?"
        else:
            response = f"✅ **Good news!** Your ₹{budget:,} budget is realistic for your requirements. "
            response += f"Similar {category} typically cost ₹{estimated_cost:,}, so you're in a good range!"
        
        return {
            "response": response,
            "type": "budget_reality_check",
            "requires_user_input": True
        }
    
    def _create_educational_response(self, context: ConversationContext) -> Dict[str, Any]:
        """Create educational content for beginners"""
        
        category = context.current_requirements.get("category", "gaming laptops")
        level = context.current_requirements.get("expertise_level", "beginner")
        
        if category not in self.educational_content or level not in self.educational_content[category]:
            return self._create_clarification_response(context)
        
        education = self.educational_content[category][level]
        
        context.clarification_history.append({
            "timestamp": datetime.now().isoformat(),
            "type": "education",
            "content_provided": list(education.keys())
        })
        
        context.education_needed.extend(education.keys())
        
        response = "🎓 **Let me help you understand the key concepts:**\n\n"
        
        for concept, explanation in list(education.items())[:2]:  # Show 2 concepts at a time
            response += f"**{concept.replace('_', ' ').title()}:**\n{explanation}\n\n"
        
        response += "Does this help? Any questions about these concepts before we continue?"
        
        return {
            "response": response,
            "type": "education",
            "requires_user_input": True
        }
    
    def _create_intelligent_recommendations(self, context: ConversationContext) -> Dict[str, Any]:
        """Create intelligent product recommendations"""
        
        reqs = context.current_requirements
        category = reqs.get("category")
        budget = reqs.get("budget")
        
        # Get products with full intelligence
        products = self.product_db.get_products_with_intelligence(category, budget)
        
        if not products:
            return {
                "response": "I couldn't find products matching your exact requirements. Let me adjust the search criteria.",
                "type": "no_results",
                "requires_user_input": True
            }
        
        # Create smart recommendations with reasoning
        recommendations = []
        for product in products[:3]:  # Top 3 recommendations
            
            # Calculate match score based on priorities
            match_score = self._calculate_match_score(product, context)
            
            # Generate reasoning
            reasoning = self._generate_recommendation_reasoning(product, context)
            
            # Identify trade-offs
            trade_offs = self._identify_trade_offs(product, context)
            
            recommendation = SmartRecommendation(
                product=product,
                match_score=match_score,
                reasoning=reasoning,
                trade_offs=trade_offs,
                confidence=min(0.95, match_score / 5.0 + 0.5),
                deal_highlights=self._get_deal_highlights(product),
                savings_amount=product.price_info.original_price - product.price_info.current_price if product.price_info else 0,
                urgency_factors=self._get_urgency_factors(product),
                why_better_than_alternatives=self._get_better_than_alternatives(product, products),
                what_you_might_miss=self._get_what_you_might_miss(product, context)
            )
            
            recommendations.append(recommendation)
        
        # Sort by match score
        recommendations.sort(key=lambda x: x.match_score, reverse=True)
        
        if recommendations:
            return {
                "response": f"Perfect! I found {len(recommendations)} excellent options that match your needs. Here are my top recommendations:",
                "type": "intelligent_recommendations",
                "recommendations": recommendations,
                "conversation_summary": self._create_conversation_summary(context)
            }
        else:
            return {
                "response": f"I'm having trouble finding products that match your requirements for {category} under ₹{budget:,}. Let me adjust the search criteria or would you like to modify your requirements?",
                "type": "no_results",
                "requires_user_input": True
            }
    
    def _calculate_match_score(self, product, context: ConversationContext) -> float:
        """Calculate how well product matches user requirements"""
        score = 0.0
        max_score = 0.0
        
        # Budget match (30% weight)
        budget = context.current_requirements.get("budget", 0)
        if budget > 0 and product.price_info:
            price = product.price_info.current_price
            if price <= budget:
                score += 1.5 * (1 - (price / budget) * 0.5)  # Reward being under budget
            else:
                score += max(0, 1.5 * (1 - (price - budget) / budget))  # Penalize over budget
        max_score += 1.5
        
        # Review score match (25% weight)
        if product.review_analysis:
            score += 1.25 * (product.review_analysis.overall_rating / 5.0)
        max_score += 1.25
        
        # Priority rankings match (30% weight)
        priority_score = 0.0
        if context.priority_rankings:
            for feature, importance in context.priority_rankings.items():
                if product.review_analysis and feature.lower() in product.review_analysis.category_ratings:
                    rating = product.review_analysis.category_ratings[feature.lower()]
                    priority_score += (importance / 10.0) * (rating / 5.0) * 0.3
        score += priority_score
        max_score += 1.5
        
        # Deal quality (15% weight)
        if product.price_info:
            score += 0.75 * (product.price_info.discount_percentage / 100.0)
        max_score += 0.75
        
        return min(5.0, (score / max_score) * 5.0) if max_score > 0 else 3.0
    
    def _generate_recommendation_reasoning(self, product, context: ConversationContext) -> List[str]:
        """Generate reasoning for why this product is recommended"""
        reasoning = []
        
        # Budget reasoning
        budget = context.current_requirements.get("budget", 0)
        if budget > 0 and product.price_info:
            price = product.price_info.current_price
            if price <= budget * 0.9:
                reasoning.append(f"Excellent value - ₹{budget - price:,} under your budget")
            elif price <= budget:
                reasoning.append(f"Fits your ₹{budget:,} budget perfectly")
        
        # Performance reasoning
        if product.review_analysis and product.review_analysis.category_ratings.get("performance", 0) >= 4.0:
            reasoning.append(f"Strong performance rating ({product.review_analysis.category_ratings['performance']}/5.0) from users")
        
        # Deal reasoning
        if product.price_info and product.price_info.discount_percentage > 10:
            reasoning.append(f"Great deal - {product.price_info.discount_percentage:.0f}% discount from original price")
        
        # User priority reasoning
        if context.priority_rankings:
            for feature, importance in context.priority_rankings.items():
                if (importance >= 8 and product.review_analysis and 
                    product.review_analysis.category_ratings.get(feature.lower().replace(" ", "_"), 0) >= 4.0):
                    reasoning.append(f"Excels in your top priority: {feature}")
        
        return reasoning[:4]  # Max 4 reasons
    
    def _identify_trade_offs(self, product, context: ConversationContext) -> Dict[str, str]:
        """Identify potential trade-offs for this product"""
        trade_offs = {}
        
        if product.review_analysis:
            ratings = product.review_analysis.category_ratings
            
            # Check for lower-rated categories
            for category, rating in ratings.items():
                if rating < 3.5:
                    trade_offs[category] = f"Below average {category.replace('_', ' ')} ({rating}/5.0)"
                elif rating < 4.0:
                    trade_offs[category] = f"Average {category.replace('_', ' ')} ({rating}/5.0)"
        
        return trade_offs
    
    def _get_deal_highlights(self, product) -> List[str]:
        """Get deal highlights for the product"""
        highlights = []
        
        if product.price_info:
            if product.price_info.discount_percentage > 15:
                highlights.append(f"Major discount: {product.price_info.discount_percentage:.0f}% off")
            
            if product.price_info.is_good_deal:
                highlights.append("Near historical low price")
            
            if product.price_info.price_drop_alerts:
                highlights.extend(product.price_info.price_drop_alerts[:2])
        
        return highlights
    
    def _get_urgency_factors(self, product) -> List[str]:
        """Get urgency factors for buying this product"""
        factors = []
        
        if product.stock_status:
            limited_stock = any("Limited" in status for status in product.stock_status.values())
            if limited_stock:
                factors.append("Limited stock across platforms")
        
        if product.price_info and product.price_info.price_trend == "increasing":
            factors.append("Price trend is increasing")
        
        if product.urgency_score >= 7:
            factors.append("Good time to buy based on market analysis")
        
        return factors
    
    def _needs_budget_reality_check(self, context: ConversationContext) -> bool:
        """Determine if budget reality check is needed"""
        estimated = self._estimate_realistic_cost(context)
        budget = context.current_requirements.get("budget", 0)
        return estimated > budget * 1.15  # 15% over budget
    
    def _estimate_realistic_cost(self, context: ConversationContext) -> int:
        """Estimate realistic cost based on requirements"""
        base_cost = 50000  # Base gaming laptop cost
        
        # Adjust based on requirements
        if "high performance" in str(context.current_requirements).lower():
            base_cost += 15000
        
        if "premium" in str(context.current_requirements).lower():
            base_cost += 20000
            
        return base_cost
    
    def _create_conversation_summary(self, context: ConversationContext) -> Dict[str, Any]:
        """Create a summary of the conversation"""
        return {
            "requirements": context.current_requirements,
            "priorities": context.priority_rankings,
            "deal_breakers": context.deal_breakers,
            "expertise_level": context.user_expertise_level,
            "conversation_turns": len(context.requirements_history)
        }
    
    def _get_better_than_alternatives(self, product, all_products) -> List[str]:
        """Why this product is better than alternatives"""
        reasons = []
        
        for other in all_products:
            if other.id == product.id:
                continue
                
            # Compare prices
            if (product.price_info and other.price_info and 
                product.price_info.current_price < other.price_info.current_price):
                price_diff = other.price_info.current_price - product.price_info.current_price
                reasons.append(f"₹{price_diff:,} cheaper than {other.name}")
            
            # Compare reviews
            if (product.review_analysis and other.review_analysis and
                product.review_analysis.overall_rating > other.review_analysis.overall_rating):
                reasons.append(f"Higher rated than {other.name} ({product.review_analysis.overall_rating} vs {other.review_analysis.overall_rating})")
        
        return reasons[:3]
    
    def _get_what_you_might_miss(self, product, context: ConversationContext) -> List[str]:
        """What user might miss if they choose cheaper alternatives"""
        misses = []
        
        if product.review_analysis:
            strong_points = [
                category for category, rating in product.review_analysis.category_ratings.items()
                if rating >= 4.3
            ]
            
            for point in strong_points[:3]:
                misses.append(f"Excellent {point.replace('_', ' ')}")
        
        return misses
    
    def _create_clarification_response(self, context: ConversationContext) -> Dict[str, Any]:
        """Create contextual clarification response"""
        
        reqs = context.current_requirements
        
        # Generate contextual response based on what's missing
        if not reqs.get("category"):
            response = "I'd be happy to help you find the perfect product! What type of product are you looking for? (e.g., laptop, smartphone, headphones, etc.)"
        elif not reqs.get("budget"):
            category = reqs.get("category", "product")
            response = f"Great! You're looking for {category}. What's your budget range for this purchase?"
        else:
            # We have basic info, ask for more details
            response = "Perfect! I have your basic requirements. Is there anything specific you'd like me to know about your needs or preferences?"
        
        return {
            "response": response,
            "type": "clarification",
            "requires_user_input": True
        }