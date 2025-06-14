import streamlit as st
import os
from dotenv import load_dotenv
from services.chatbot_service import ChatbotService
from services.product_service import ProductService
from services.intelligent_chatbot import IntelligentChatbot
from components.intelligent_ui import IntelligentProductDisplay, ConversationInterface
from models.product_models import ConversationContext
from utils.ui_helpers import display_product_comparison, display_chat_message
import uuid

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="SmartShop - Product Discovery Platform",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize services
@st.cache_resource
def init_services():
    chatbot = ChatbotService()
    product_service = ProductService()
    intelligent_chatbot = IntelligentChatbot()
    return chatbot, product_service, intelligent_chatbot

def load_custom_css():
    """Load custom CSS for better UI"""
    try:
        with open("/Users/jakkuamruth/Downloads/hackprix/style.css") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        pass  # CSS file not found, use default styling

def main():
    # Load custom CSS
    load_custom_css()
    
    # Header section
    st.markdown("""
    <div class="main-header">
        <h1>🛍️ SmartShop</h1>
        <p>Your AI-Powered Product Discovery Assistant</p>
        <p style="font-size: 1rem; margin-top: 1rem;">
            Tell us what you need, and we'll find the best options across multiple platforms
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize services
    chatbot, product_service, intelligent_chatbot = init_services()
    
    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = []
        st.session_state.user_requirements = {}
        st.session_state.search_complete = False
        st.session_state.products = []
        st.session_state.intelligent_mode = True  # Enable intelligent mode by default
        st.session_state.session_id = str(uuid.uuid4())
        st.session_state.conversation_context = None
        st.session_state.smart_recommendations = []
    
    # Enhanced Sidebar
    with st.sidebar:
        st.markdown("### 🧠 Intelligent Mode")
        intelligent_mode = st.toggle(
            "Enable Advanced AI", 
            value=st.session_state.intelligent_mode,
            help="Advanced AI with deep requirement analysis, contradiction resolution, and educational guidance"
        )
        
        if intelligent_mode != st.session_state.intelligent_mode:
            st.session_state.intelligent_mode = intelligent_mode
            st.rerun()
        
        st.markdown("### 🔄 Chat Controls")
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.messages = []
            st.session_state.user_requirements = {}
            st.session_state.search_complete = False
            st.session_state.products = []
            st.session_state.smart_recommendations = []
            st.session_state.conversation_context = None
            st.session_state.session_id = str(uuid.uuid4())
            st.rerun()
        
        # Display current requirements in a clean format
        if st.session_state.user_requirements:
            st.markdown("### 📋 Your Requirements")
            
            with st.container():
                for key, value in st.session_state.user_requirements.items():
                    formatted_key = key.replace('_', ' ').title()
                    if isinstance(value, list):
                        formatted_value = ", ".join(str(v) for v in value)
                    elif key == "budget":
                        formatted_value = f"₹{value:,}"
                    else:
                        formatted_value = str(value)
                    
                    st.write(f"**{formatted_key}:** {formatted_value}")
        
        # Add some helpful tips
        st.markdown("### 💡 Tips")
        st.markdown("""
        - Be specific about your needs
        - Mention your budget range
        - Tell us how you'll use the product
        - We'll find the best deals for you!
        """)
        
        # Display progress based on mode
        if st.session_state.intelligent_mode and st.session_state.conversation_context:
            # Intelligent mode progress
            IntelligentProductDisplay.display_conversation_progress(
                st.session_state.conversation_context, 
                "recommendations" if st.session_state.smart_recommendations else "in_progress"
            )
        elif st.session_state.user_requirements:
            # Basic mode progress
            progress = 0
            total_required = 2  # category and budget
            
            if st.session_state.user_requirements.get("category"):
                progress += 1
            if st.session_state.user_requirements.get("budget"):
                progress += 1
        
            st.markdown("### 📊 Progress")
            st.progress(progress / total_required)
            
            if progress >= total_required:
                st.success("✅ Ready to search!")
            else:
                missing = []
                if not st.session_state.user_requirements.get("category"):
                    missing.append("category")
                if not st.session_state.user_requirements.get("budget"):
                    missing.append("budget")
                st.write(f"Need: {', '.join(missing)}")
    
    # Main chat interface
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Show current conversation status
        if st.session_state.intelligent_mode:
            if st.session_state.smart_recommendations:
                st.success("🧠 Advanced AI Analysis Complete - Smart Recommendations Ready!")
            elif st.session_state.conversation_context:
                st.info("🤖 Advanced AI is analyzing your needs...")
            else:
                st.info("🧠 Advanced AI Mode - Deep requirement analysis enabled")
        else:
            # Basic mode status
            if st.session_state.user_requirements:
                progress = 0
                if st.session_state.user_requirements.get("category"):
                    progress += 1
                if st.session_state.user_requirements.get("budget"):
                    progress += 1
                
                if progress < 2:
                    missing = []
                    if not st.session_state.user_requirements.get("category"):
                        missing.append("category")
                    if not st.session_state.user_requirements.get("budget"):
                        missing.append("budget")
                    st.info(f"💬 Conversation in progress... (Need: {', '.join(missing)})")
                else:
                    st.success("✅ Ready to find products! All requirements collected.")
        
        # Create a styled chat container
        chat_container = st.container()
        
        # Display chat messages in a scrollable area
        with chat_container:
            if st.session_state.messages:
                for message in st.session_state.messages:
                    display_chat_message(message["role"], message["content"])
            else:
                # Welcome message when no conversation started
                st.markdown("""
                <div style="text-align: center; padding: 2rem; color: #6c757d;">
                    <h4>👋 Welcome to SmartShop!</h4>
                    <p>I'm here to help you find the perfect product. Just tell me what you're looking for!</p>
                    <p><strong>Try saying:</strong></p>
                    <ul style="text-align: left; display: inline-block;">
                        <li>"I need a laptop for gaming"</li>
                        <li>"Looking for a smartphone under 30k"</li>
                        <li>"Want to buy headphones for music"</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
        
        # Add quick suggestion buttons if no conversation started
        if not st.session_state.messages:
            st.markdown("**Quick Start:**")
            col_q1, col_q2, col_q3 = st.columns(3)
            
            with col_q1:
                if st.button("💻 Gaming Laptop", use_container_width=True, key="quick_laptop"):
                    user_message = "I need a gaming laptop under 60000"
                    st.session_state.messages.append({"role": "user", "content": user_message})
                    st.rerun()
            
            with col_q2:
                if st.button("📱 Smartphone", use_container_width=True, key="quick_phone"):
                    user_message = "I need a smartphone under 30000"
                    st.session_state.messages.append({"role": "user", "content": user_message})
                    st.rerun()
            
            with col_q3:
                if st.button("🎧 Headphones", use_container_width=True, key="quick_audio"):
                    user_message = "I need wireless headphones for music under 5000"
                    st.session_state.messages.append({"role": "user", "content": user_message})
                    st.rerun()
    
    # Dynamic chat input based on conversation state
    if st.session_state.intelligent_mode:
        if not st.session_state.messages:
            placeholder = "What product are you looking for? (e.g., 'Gaming laptops under ₹60,000')"
        elif st.session_state.conversation_context and not st.session_state.conversation_context.current_requirements.get("budget"):
            placeholder = "What's your budget for this purchase?"
        else:
            placeholder = "Tell me more about your preferences..."
    else:
        # Basic mode placeholders
        if not st.session_state.messages:
            placeholder = "What product are you looking for? (e.g., 'gaming laptop under 60k')"
        elif not st.session_state.user_requirements.get("category"):
            placeholder = "Tell me what type of product you need..."
        elif not st.session_state.user_requirements.get("budget"):
            placeholder = "What's your budget range?"
        else:
            placeholder = "Any other preferences or questions?"
    
    # Chat input (outside columns to avoid container restriction)
    if prompt := st.chat_input(placeholder):
        # Add user message to chat
        st.session_state.messages.append({"role": "user", "content": prompt})
        if st.session_state.intelligent_mode:
            # Use intelligent chatbot
            if not st.session_state.conversation_context:
                # Start new intelligent conversation
                response = intelligent_chatbot.start_conversation(st.session_state.session_id, prompt)
                st.session_state.conversation_context = intelligent_chatbot.conversations[st.session_state.session_id]
            else:
                # Continue existing conversation
                response = intelligent_chatbot.process_message(st.session_state.session_id, prompt)
                st.session_state.conversation_context = intelligent_chatbot.conversations[st.session_state.session_id]
            
            # Handle different response types
            if response["type"] == "intelligent_recommendations":
                st.session_state.smart_recommendations = response["recommendations"]
                st.session_state.search_complete = True
                st.session_state.messages.append({"role": "assistant", "content": response["response"]})
            elif response["type"] in ["priority_ranking", "use_case_scenario", "deal_breaker_detection"]:
                # Handle interactive responses
                st.session_state.messages.append({"role": "assistant", "content": response["response"]})
                # Add interactive components below
                if response["type"] == "priority_ranking":
                    priorities = ConversationInterface.display_priority_ranking_interface(response.get("options", []))
                    if priorities:
                        st.session_state.conversation_context.priority_rankings = priorities
            else:
                # Regular conversation response
                st.session_state.messages.append({"role": "assistant", "content": response["response"]})
            
            # Update session requirements from context
            if st.session_state.conversation_context:
                st.session_state.user_requirements.update(
                    st.session_state.conversation_context.current_requirements
                )
        else:
            # Use basic chatbot
            response = chatbot.process_message(prompt, st.session_state.user_requirements)
            
            # Add assistant response to chat
            st.session_state.messages.append({"role": "assistant", "content": response["message"]})
            
            # Update requirements if provided
            if response.get("requirements"):
                st.session_state.user_requirements.update(response["requirements"])
            
            # Check if search should be triggered
            if response.get("search_ready", False):
                st.session_state.search_complete = True
                # Get products based on requirements
                products = product_service.search_products(st.session_state.user_requirements)
                st.session_state.products = products
        
        st.rerun()
    
    with col2:
        if st.session_state.search_complete:
            if st.session_state.intelligent_mode and st.session_state.smart_recommendations:
                # Display intelligent recommendations
                st.markdown("### 🧠 Smart Recommendations")
                
                # Quick stats
                num_recs = len(st.session_state.smart_recommendations)
                avg_match = sum(r.match_score for r in st.session_state.smart_recommendations) / num_recs
                
                col_stat1, col_stat2 = st.columns(2)
                with col_stat1:
                    st.metric("AI Recommendations", num_recs)
                with col_stat2:
                    st.metric("Avg Match Score", f"{avg_match:.1f}/5.0")
            
            elif st.session_state.products:
                # Display basic recommendations
                st.markdown("### 🏆 Product Recommendations")
                
                # Display search stats
        
                num_products = len(st.session_state.products)
                platforms = list(set(p.get('platform', 'Unknown') for p in st.session_state.products))
                avg_price = sum(p.get('price', 0) for p in st.session_state.products) / len(st.session_state.products)
                
                col_stat1, col_stat2 = st.columns(2)
                with col_stat1:
                    st.metric("Products Found", num_products)
                with col_stat2:
                    st.metric("Avg Price", f"₹{avg_price:,.0f}")
                
                st.write(f"**Platforms:** {', '.join(platforms)}")
                
                display_product_comparison(st.session_state.products)
        else:
            st.markdown("### 🎯 How SmartShop Works")
            
            # Use a container with clean styling
            with st.container():
                st.markdown("#### 🤖 AI-Powered Search")
                
                st.markdown("""
                1. **Tell us what you need**  
                   *Describe the product you're looking for*
                
                2. **Smart questions**  
                   *We'll ask clarifying questions to understand your needs*
                
                3. **Multi-platform search**  
                   *Search across Amazon, Flipkart, and more*
                
                4. **Compare and choose**  
                   *See the best options with detailed comparisons*
                """)
            
            # Add some example searches
            st.markdown("### 📱 Popular Searches")
            
            example_searches = [
                "🎮 Gaming Laptops under ₹60,000",
                "📱 Smartphones with good cameras",
                "🎧 Wireless earphones for music",
                "⌚ Smartwatches for fitness",
                "📷 DSLR cameras for beginners"
            ]
            
            for search in example_searches:
                if st.button(search, key=f"example_{search}", use_container_width=True):
                    # Auto-fill the chat with example search and get bot response
                    user_message = search.split(" ", 1)[1]  # Remove emoji
                    st.session_state.messages.append({"role": "user", "content": user_message})
                    
                    # Get immediate chatbot response
                    response = chatbot.process_message(user_message, st.session_state.user_requirements)
                    st.session_state.messages.append({"role": "assistant", "content": response["message"]})
                    
                    # Update requirements if provided
                    if response.get("requirements"):
                        st.session_state.user_requirements.update(response["requirements"])
                    
                    # Check if ready to search for products
                    if response.get("search_ready"):
                        with st.spinner("Searching for products..."):
                            products = product_service.search_products(st.session_state.user_requirements)
                            st.session_state.products = products
                            st.session_state.search_complete = True
                    
                    st.rerun()
    
    # Display intelligent recommendations in full width if available
    if st.session_state.intelligent_mode and st.session_state.smart_recommendations:
        st.markdown("---")
        
        # Get conversation summary
        conversation_summary = {}
        if st.session_state.conversation_context:
            conversation_summary = {
                "requirements": st.session_state.conversation_context.current_requirements,
                "priorities": st.session_state.conversation_context.priority_rankings,
                "deal_breakers": st.session_state.conversation_context.deal_breakers,
                "expertise_level": st.session_state.conversation_context.user_expertise_level,
                "conversation_turns": len(st.session_state.conversation_context.requirements_history)
            }
        
        # Display intelligent recommendations
        IntelligentProductDisplay.display_smart_recommendations(
            st.session_state.smart_recommendations,
            conversation_summary
        )

if __name__ == "__main__":
    main()