import os
import json
import google.generativeai as genai
from typing import Dict, Any

class ChatbotService:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            print("Warning: Gemini API key not found in environment variables. Using fallback mode.")
            self.model = None
        else:
            try:
                genai.configure(api_key=api_key)
                
                # Try different model names in order of preference
                model_names = [
                    'gemini-1.5-flash',
                    'gemini-1.5-pro', 
                    'gemini-pro',
                    'models/gemini-1.5-flash',
                    'models/gemini-pro'
                ]
                
                self.model = None
                for model_name in model_names:
                    try:
                        self.model = genai.GenerativeModel(model_name)
                        # Test with a simple generation
                        test_response = self.model.generate_content("Hello")
                        print(f"✅ Gemini API initialized successfully with model: {model_name}")
                        break
                    except Exception as model_error:
                        print(f"Failed to initialize model {model_name}: {model_error}")
                        continue
                
                if not self.model:
                    print("❌ Failed to initialize any Gemini model")
                    
            except Exception as e:
                print(f"Error configuring Gemini API: {e}")
                self.model = None
        
        self.conversation_history = []
        self.asked_questions = set()  # Track what we've already asked about
        
    def process_message(self, user_message: str, current_requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Process user message and return response with updated requirements"""
        
        # Add user message to conversation history
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })
        
        # Create system prompt for requirement gathering
        system_prompt = self._create_system_prompt(current_requirements)
        
        try:
            # Check if model is available
            if not self.model:
                return {
                    "message": "I'm having trouble connecting to the chat service. Let me use a fallback response to help you.",
                    "requirements": self._extract_requirements_fallback(user_message, current_requirements),
                    "search_ready": self._is_search_ready_fallback(current_requirements)
                }
            
            # Create conversation context for Gemini
            conversation_context = ""
            if self.conversation_history:
                for msg in self.conversation_history[-4:]:  # Keep last 4 messages for context
                    role = "User" if msg["role"] == "user" else "Assistant"
                    conversation_context += f"{role}: {msg['content']}\n"
            
            # Create the prompt for Gemini
            full_prompt = f"{system_prompt}\n\nConversation history:\n{conversation_context}\nUser: {user_message}\nAssistant:"
            
            # Get response from Gemini
            response = self.model.generate_content(full_prompt)
            assistant_message = response.text
            
            # Add assistant response to conversation history
            self.conversation_history.append({
                "role": "assistant", 
                "content": assistant_message
            })
            
            # Parse response to extract requirements and determine if search is ready
            parsed_response = self._parse_response(assistant_message, user_message, current_requirements)
            
            return {
                "message": assistant_message,
                "requirements": parsed_response.get("requirements", {}),
                "search_ready": parsed_response.get("search_ready", False)
            }
            
        except Exception as e:
            return {
                "message": f"I'm having trouble connecting right now. Can you try again? Error: {str(e)}",
                "requirements": {},
                "search_ready": False
            }
    
    def _create_system_prompt(self, current_requirements: Dict[str, Any]) -> str:
        """Create system prompt for the chatbot"""
        
        # Determine what information we still need (only category and budget are essential)
        missing_info = []
        if not current_requirements.get("category"):
            missing_info.append("product category")
        if not current_requirements.get("budget"):
            missing_info.append("budget range")
        # Use case is optional - don't add to missing info if we have category and budget
        
        # Create a requirements summary
        req_summary = "No requirements gathered yet."
        if current_requirements:
            req_summary = "Current requirements:\n"
            for key, value in current_requirements.items():
                if isinstance(value, list):
                    req_summary += f"- {key.replace('_', ' ').title()}: {', '.join(value)}\n"
                else:
                    req_summary += f"- {key.replace('_', ' ').title()}: {value}\n"
        
        return f"""You are SmartShop Assistant, a helpful product discovery chatbot. Your goal is to understand what product the user wants to buy by asking SMART, NON-REPETITIVE questions.

{req_summary}

CRITICAL INSTRUCTIONS:
1. NEVER ask about information you already have - review the current requirements carefully
2. If you have category and budget - you have enough info to search (use case is optional)
3. Ask only ONE question at a time
4. Be conversational and natural
5. Don't repeat questions or information gathering
6. If user says "Gaming Laptops under ₹60,000" - you already have category (gaming laptops), budget (₹60,000), and use case (gaming)

Current conversation stage:
{f"Missing: {', '.join(missing_info)}" if missing_info else "Ready to search - you have enough information!"}

Response strategy:
- If you have NO info: Ask about product category first
- If you have category but no budget: Ask about budget range  
- If you have category and budget: Say you're ready to search and start the search
- If you have all three: Say you're ready to search and start the search

NEVER ask:
- Questions about information already provided
- Multiple questions in one response  
- Generic "Any other preferences?" questions
- Budget questions when budget is already mentioned

When ready to search, say: "Perfect! I have everything I need. Let me find the best [category] options for you within your budget of ₹[budget]."

EXAMPLES:
- User: "Gaming Laptops under ₹60,000" → You already have: category (gaming laptops), budget (₹60,000), use_case (gaming) → Response: "Perfect! I have everything I need. Let me find the best gaming laptops for you within your budget of ₹60,000."
- User: "I need a smartphone" → You have: category (smartphones) → Response: "Great! What's your budget range for the smartphone?"
- User: "Business laptop for work" → You have: category (laptops), use_case (work) → Response: "Great choice! What's your budget range for the business laptop?"

CRITICAL: If user says "Gaming [product]" - they clearly want it for GAMING. Don't ask what they'll use it for!
"""
    
    def _parse_response(self, assistant_message: str, user_message: str, current_requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Parse the assistant's response to extract requirements and determine search readiness"""
        
        # Enhanced keyword-based requirement extraction
        requirements = {}
        user_lower = user_message.lower()
        
        # Extract budget information with better patterns
        import re
        budget_patterns = [
            r"under[^\d]*₹?\s*(\d+)[k\s]*(?:thousand|k|,000)?",
            r"below[^\d]*₹?\s*(\d+)[k\s]*(?:thousand|k|,000)?",
            r"₹\s*(\d+)[k\s]*(?:thousand|k|,000)?",
            r"budget[^\d]*₹?\s*(\d+)[k\s]*(?:thousand|k|,000)?",
            r"₹?\s*(\d+)[k\s]*(?:thousand|k|,000)?\s*budget",
            r"(\d+)[k\s]*(?:thousand|k|,000)?\s*rupees?",
            r"rs\.?\s*(\d+)[k\s]*(?:thousand|k|,000)?",
            r"(\d+)k(?:\s|$)"
        ]
        
        for pattern in budget_patterns:
            match = re.search(pattern, user_lower)
            if match:
                budget_num = int(match.group(1))
                # Handle k notation and reasonable assumptions
                if 'k' in user_lower or 'thousand' in user_lower or budget_num < 1000:
                    if budget_num < 1000:
                        budget_num *= 1000
                requirements["budget"] = budget_num
                break
        
        # Enhanced category extraction with gaming laptops (order matters - check specific terms first)
        category_mappings = {
            "gaming laptop": ("gaming laptops", "gaming"),
            "gaming laptops": ("gaming laptops", "gaming"),
            "business laptop": ("laptops", "business"),
            "work laptop": ("laptops", "work"),
            "laptop": ("laptops", None),
            "gaming phone": ("smartphones", "gaming"),
            "phone": ("smartphones", None),
            "smartphone": ("smartphones", None),
            "mobile": ("smartphones", None),
            "tablet": ("tablets", None),
            "gaming headphones": ("headphones", "gaming"),
            "headphones": ("headphones", None),
            "earphones": ("headphones", None),
            "headset": ("headphones", None),
            "camera": ("cameras", "photography"),
            "watch": ("smartwatches", None),
            "smartwatch": ("smartwatches", None)
        }
        
        # Check in order of specificity (gaming laptop before laptop)
        for keyword, (category, use_case) in category_mappings.items():
            if keyword in user_lower:
                requirements["category"] = category
                if use_case:
                    requirements["use_case"] = use_case
                break
        
        # Extract use case
        use_case_mappings = {
            "gaming": "gaming",
            "work": "work",
            "office": "office work",
            "college": "studies",
            "study": "studies",
            "photography": "photography",
            "video editing": "video editing",
            "music": "music",
            "business": "business",
            "programming": "programming"
        }
        
        for keyword, use_case in use_case_mappings.items():
            if keyword in user_lower:
                requirements["use_case"] = use_case
                break
        
        # Determine if search is ready
        search_indicators = [
            "let me search", "search for", "find the best", "show me options", 
            "ready to search", "have all the information", "perfect! i have everything"
        ]
        search_ready = any(indicator in assistant_message.lower() for indicator in search_indicators)
        
        # Check if we have minimum required info (category + budget)
        merged_requirements = {**current_requirements, **requirements}
        has_category = "category" in merged_requirements
        has_budget = "budget" in merged_requirements
        
        # If we have both category and budget, we're ready to search
        if has_category and has_budget:
            search_ready = True
        
        # Debug: print extracted requirements (for development)
        print(f"DEBUG - User message: {user_message}")
        print(f"DEBUG - Extracted requirements: {requirements}")
        print(f"DEBUG - Merged requirements: {merged_requirements}")
        print(f"DEBUG - Search ready: {search_ready}")
        
        return {
            "requirements": requirements,
            "search_ready": search_ready
        }
    
    def _extract_requirements_fallback(self, user_message: str, current_requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback method to extract requirements without OpenAI"""
        requirements = {}
        
        # Simple keyword-based extraction
        message_lower = user_message.lower()
        
        # Extract budget
        if "budget" in message_lower or "price" in message_lower or "₹" in user_message:
            import re
            numbers = re.findall(r'₹?(\d+)k?', user_message)
            if numbers:
                budget = int(numbers[0])
                if 'k' in user_message.lower():
                    budget *= 1000
                requirements["budget"] = budget
        
        # Extract category
        categories = ["laptop", "phone", "smartphone", "mobile", "tablet", "headphones", "earphones"]
        for category in categories:
            if category in message_lower:
                requirements["category"] = category
                break
        
        return requirements
    
    def _is_search_ready_fallback(self, current_requirements: Dict[str, Any]) -> bool:
        """Fallback method to determine if search is ready"""
        has_category = "category" in current_requirements
        has_budget = "budget" in current_requirements
        return has_category and has_budget