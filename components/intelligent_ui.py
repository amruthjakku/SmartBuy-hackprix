"""
Advanced UI Components for Intelligent Product Discovery
"""
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from typing import List, Dict, Any
from models.product_models import ProductIntelligence, SmartRecommendation, PriceHistory
import pandas as pd
from datetime import datetime, timedelta

class IntelligentProductDisplay:
    """Advanced product display with comprehensive intelligence"""
    
    @staticmethod
    def display_smart_recommendations(recommendations: List[SmartRecommendation], conversation_summary: Dict[str, Any]):
        """Display intelligent recommendations with reasoning"""
        
        st.markdown("## 🧠 Smart Recommendations")
        st.markdown("*Based on our conversation and advanced product intelligence*")
        
        # Conversation summary
        with st.expander("📋 What we learned about your needs", expanded=False):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Your Requirements:**")
                for key, value in conversation_summary.get("requirements", {}).items():
                    if key != "expertise_level":
                        st.write(f"• **{key.replace('_', ' ').title()}:** {value}")
            
            with col2:
                if conversation_summary.get("priorities"):
                    st.markdown("**Your Priorities:**")
                    for feature, importance in conversation_summary["priorities"].items():
                        st.write(f"• {feature}: {importance}/10")
        
        # Display recommendations
        for i, rec in enumerate(recommendations, 1):
            IntelligentProductDisplay.display_single_recommendation(rec, i)
    
    @staticmethod
    def display_single_recommendation(recommendation: SmartRecommendation, rank: int):
        """Display a single smart recommendation"""
        
        product = recommendation.product
        
        # Main product card
        with st.container():
            st.markdown(f"### {rank}. {product.name}")
            
            # Match score and confidence
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                # Match score visualization
                match_percentage = (recommendation.match_score / 5.0) * 100
                st.metric(
                    "Match Score", 
                    f"{match_percentage:.0f}%",
                    help="How well this product matches your requirements"
                )
            
            with col2:
                st.metric(
                    "AI Confidence",
                    f"{recommendation.confidence*100:.0f}%",
                    help="How confident our AI is about this recommendation"
                )
            
            with col3:
                if recommendation.savings_amount > 0:
                    st.metric(
                        "You Save",
                        f"₹{recommendation.savings_amount:,}",
                        help="Savings from original price"
                    )
            
            # Reasoning section
            st.markdown("#### 🎯 Why we recommend this:")
            for reason in recommendation.reasoning:
                st.write(f"✅ {reason}")
            
            # Deal highlights
            if recommendation.deal_highlights:
                st.markdown("#### 🔥 Deal Highlights:")
                for highlight in recommendation.deal_highlights:
                    st.write(f"🎉 {highlight}")
            
            # Price and availability
            IntelligentProductDisplay.display_price_intelligence(product)
            
            # Product intelligence tabs
            tab1, tab2, tab3, tab4 = st.tabs(["📊 Reviews", "📈 Price History", "⚖️ Trade-offs", "🔄 Alternatives"])
            
            with tab1:
                IntelligentProductDisplay.display_review_intelligence(product.review_analysis)
            
            with tab2:
                IntelligentProductDisplay.display_price_history(product.price_info)
            
            with tab3:
                IntelligentProductDisplay.display_trade_offs(recommendation.trade_offs)
            
            with tab4:
                IntelligentProductDisplay.display_alternatives(recommendation)
            
            # Action buttons
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button(f"View Details - {product.name}", key=f"details_{product.id}"):
                    st.session_state[f"show_details_{product.id}"] = True
            
            with col2:
                if st.button(f"Compare Prices", key=f"compare_{product.id}"):
                    IntelligentProductDisplay.display_price_comparison(product)
            
            with col3:
                if st.button(f"Set Price Alert", key=f"alert_{product.id}"):
                    st.success(f"Price alert set for {product.name}!")
            
            st.markdown("---")
    
    @staticmethod
    def display_price_intelligence(product: ProductIntelligence):
        """Display comprehensive price intelligence"""
        
        st.markdown("#### 💰 Price Intelligence")
        
        if not product.platform_prices:
            st.warning("Price information not available")
            return
        
        # Create price comparison
        platforms = []
        prices = []
        availability = []
        offers = []
        
        for platform, data in product.platform_prices.items():
            platforms.append(platform)
            prices.append(data["price"])
            availability.append(data["availability"])
            offers.append(", ".join(data.get("offers", [])))
        
        # Price comparison table
        price_df = pd.DataFrame({
            "Platform": platforms,
            "Price": [f"₹{p:,}" for p in prices],
            "Availability": availability,
            "Special Offers": offers
        })
        
        st.dataframe(price_df, use_container_width=True)
        
        # Best price highlight
        min_price_idx = prices.index(min(prices))
        st.success(f"🏆 **Best Price:** {platforms[min_price_idx]} - ₹{min(prices):,}")
        
        # Price trend and advice
        if product.price_info:
            col1, col2 = st.columns(2)
            
            with col1:
                trend_color = "🔺" if product.price_info.price_trend == "increasing" else "🔻" if product.price_info.price_trend == "decreasing" else "➡️"
                st.write(f"**Price Trend:** {trend_color} {product.price_info.price_trend.title()}")
                
                if product.price_info.is_good_deal:
                    st.success("✅ Good time to buy!")
                else:
                    st.info("💡 Consider waiting for better deals")
            
            with col2:
                st.write(f"**Best Time to Buy:** {product.best_time_to_buy}")
                st.write(f"**Seasonal Advice:** {product.seasonal_advice}")
    
    @staticmethod
    def display_review_intelligence(review_analysis):
        """Display intelligent review analysis"""
        
        if not review_analysis:
            st.warning("Review analysis not available")
            return
        
        # Overall rating with breakdown
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.metric(
                "Overall Rating",
                f"{review_analysis.overall_rating}/5.0",
                f"Based on {review_analysis.total_reviews:,} reviews"
            )
        
        with col2:
            # Category ratings chart
            categories = list(review_analysis.category_ratings.keys())
            ratings = list(review_analysis.category_ratings.values())
            
            fig = go.Figure(data=go.Scatterpolar(
                r=ratings,
                theta=[cat.replace('_', ' ').title() for cat in categories],
                fill='toself',
                name='Ratings'
            ))
            
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 5]
                    )),
                showlegend=False,
                height=300
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Pros and Cons
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**✅ What Users Love:**")
            for pro in review_analysis.pros_summary:
                st.write(f"• {pro}")
        
        with col2:
            st.markdown("**❌ Common Concerns:**")
            for con in review_analysis.cons_summary:
                st.write(f"• {con}")
        
        # Detailed feedback
        with st.expander("📈 Detailed User Feedback"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Most Praised Features:**")
                for praise in review_analysis.common_praise:
                    st.write(f"👍 {praise}")
            
            with col2:
                st.markdown("**Common Complaints:**")
                for complaint in review_analysis.common_complaints:
                    st.write(f"👎 {complaint}")
    
    @staticmethod
    def display_price_history(price_info: PriceHistory):
        """Display price history and trends"""
        
        if not price_info or not price_info.price_history:
            st.warning("Price history not available")
            return
        
        # Create price history chart
        df = pd.DataFrame(price_info.price_history)
        df['date'] = pd.to_datetime(df['date'])
        
        fig = px.line(
            df, 
            x='date', 
            y='price',
            title='Price History (Last 6 Months)',
            labels={'price': 'Price (₹)', 'date': 'Date'}
        )
        
        # Add current price line
        fig.add_hline(
            y=price_info.current_price,
            line_dash="dash",
            line_color="green",
            annotation_text=f"Current: ₹{price_info.current_price:,}"
        )
        
        # Add lowest price line
        fig.add_hline(
            y=price_info.lowest_price_ever,
            line_dash="dot",
            line_color="red",
            annotation_text=f"Lowest: ₹{price_info.lowest_price_ever:,}"
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Price statistics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "Current Price",
                f"₹{price_info.current_price:,}",
                f"-₹{price_info.original_price - price_info.current_price:,}"
            )
        
        with col2:
            st.metric(
                "Lowest Ever",
                f"₹{price_info.lowest_price_ever:,}",
                help="Historical lowest price"
            )
        
        with col3:
            st.metric(
                "Highest Ever",
                f"₹{price_info.highest_price_ever:,}",
                help="Historical highest price"
            )
        
        # Price alerts
        if price_info.price_drop_alerts:
            st.info("📢 " + " | ".join(price_info.price_drop_alerts))
    
    @staticmethod
    def display_trade_offs(trade_offs: Dict[str, str]):
        """Display trade-offs analysis"""
        
        if not trade_offs:
            st.success("✅ No significant trade-offs identified!")
            return
        
        st.markdown("**⚖️ Potential Trade-offs:**")
        
        for feature, trade_off in trade_offs.items():
            st.warning(f"**{feature.replace('_', ' ').title()}:** {trade_off}")
        
        st.info("💡 Consider if these trade-offs are acceptable for your use case.")
    
    @staticmethod
    def display_alternatives(recommendation: SmartRecommendation):
        """Display alternative products and comparisons"""
        
        col1, col2 = st.columns(2)
        
        with col1:
            if recommendation.why_better_than_alternatives:
                st.markdown("**✅ Why this is better:**")
                for reason in recommendation.why_better_than_alternatives:
                    st.write(f"• {reason}")
        
        with col2:
            if recommendation.what_you_might_miss:
                st.markdown("**❓ What you might miss with cheaper options:**")
                for miss in recommendation.what_you_might_miss:
                    st.write(f"• {miss}")
        
        # Urgency factors
        if recommendation.urgency_factors:
            st.markdown("**⚡ Urgency Factors:**")
            for factor in recommendation.urgency_factors:
                st.write(f"🔥 {factor}")
    
    @staticmethod
    def display_conversation_progress(context, current_step: str):
        """Display conversation progress and insights"""
        
        st.sidebar.markdown("### 🎯 Conversation Progress")
        
        # Progress steps
        steps = [
            ("Requirements", "category" in context.current_requirements and "budget" in context.current_requirements),
            ("Priorities", bool(context.priority_rankings)),
            ("Use Case", any("use_case" in h.get("type", "") for h in context.clarification_history)),
            ("Deal Breakers", bool(context.deal_breakers)),
            ("Recommendations", current_step == "recommendations")
        ]
        
        for step_name, completed in steps:
            icon = "✅" if completed else "⏳"
            st.sidebar.write(f"{icon} {step_name}")
        
        # Current requirements
        if context.current_requirements:
            st.sidebar.markdown("### 📋 Your Requirements")
            for key, value in context.current_requirements.items():
                if key == "budget":
                    st.sidebar.write(f"**Budget:** ₹{value:,}")
                else:
                    st.sidebar.write(f"**{key.replace('_', ' ').title()}:** {value}")
        
        # Priorities
        if context.priority_rankings:
            st.sidebar.markdown("### 🎯 Your Priorities")
            sorted_priorities = sorted(context.priority_rankings.items(), key=lambda x: x[1], reverse=True)
            for feature, importance in sorted_priorities[:3]:
                st.sidebar.write(f"• {feature}: {importance}/10")
    
    @staticmethod
    def display_price_comparison(product: ProductIntelligence):
        """Display detailed price comparison across platforms"""
        
        st.markdown("### 💰 Price Comparison")
        
        if not product.platform_prices:
            st.warning("Price comparison not available")
            return
        
        # Create comparison chart
        platforms = list(product.platform_prices.keys())
        prices = [data["price"] for data in product.platform_prices.values()]
        
        fig = px.bar(
            x=platforms,
            y=prices,
            title=f"Price Comparison - {product.name}",
            labels={'x': 'Platform', 'y': 'Price (₹)'},
            color=prices,
            color_continuous_scale='RdYlGn_r'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Detailed comparison table
        comparison_data = []
        for platform, data in product.platform_prices.items():
            comparison_data.append({
                "Platform": platform,
                "Price": f"₹{data['price']:,}",
                "Availability": data["availability"],
                "Delivery": data.get("delivery", "N/A"),
                "Offers": ", ".join(data.get("offers", [])[:2])  # Show first 2 offers
            })
        
        df = pd.DataFrame(comparison_data)
        st.dataframe(df, use_container_width=True)
        
        # Best deal highlight
        min_price_platform = min(product.platform_prices.items(), key=lambda x: x[1]["price"])
        st.success(f"🏆 **Best Deal:** {min_price_platform[0]} at ₹{min_price_platform[1]['price']:,}")

class ConversationInterface:
    """Enhanced conversation interface with branching and visual feedback"""
    
    @staticmethod
    def display_priority_ranking_interface(options: List[str]):
        """Interactive priority ranking interface"""
        
        st.markdown("### 🎯 Priority Ranking")
        st.markdown("Drag to reorder or use the sliders to rank by importance:")
        
        priorities = {}
        
        for i, option in enumerate(options):
            importance = st.slider(
                option,
                min_value=1,
                max_value=10,
                value=5,
                key=f"priority_{i}",
                help=f"How important is {option} to you? (1=Not important, 10=Extremely important)"
            )
            priorities[option] = importance
        
        if st.button("Submit Priorities"):
            return priorities
        
        return None
    
    @staticmethod
    def display_use_case_scenario_interface():
        """Interactive use case scenario builder"""
        
        st.markdown("### 📋 Build Your Use Case Scenario")
        
        col1, col2 = st.columns(2)
        
        with col1:
            daily_hours = st.slider("Daily usage hours", 1, 16, 6)
            portability = st.selectbox(
                "Portability needs",
                ["Mostly at home", "Occasional travel", "Daily commute", "Frequent travel"]
            )
            performance_need = st.selectbox(
                "Performance requirements",
                ["Basic tasks", "Moderate gaming", "High-end gaming", "Professional work"]
            )
        
        with col2:
            games = st.multiselect(
                "Games you play",
                ["AAA titles (Cyberpunk, GTA)", "Esports (CS:GO, Valorant)", 
                 "Casual games", "Indie games", "Mobile games"]
            )
            other_uses = st.multiselect(
                "Other uses",
                ["Video editing", "Programming", "3D modeling", "Streaming", "Office work"]
            )
        
        scenario = {
            "daily_hours": daily_hours,
            "portability": portability,
            "performance_need": performance_need,
            "games": games,
            "other_uses": other_uses
        }
        
        if st.button("Build My Scenario"):
            return scenario
        
        return None
    
    @staticmethod
    def display_deal_breaker_interface():
        """Interactive deal breaker selection"""
        
        st.markdown("### 🚫 Deal Breakers")
        st.markdown("Select anything that would make you immediately reject a laptop:")
        
        deal_breakers = []
        
        # Weight limits
        weight_limit = st.checkbox("Weight over 2.5 kg")
        if weight_limit:
            deal_breakers.append("Heavy weight (>2.5kg)")
        
        # Battery life
        battery_limit = st.checkbox("Battery life under 4 hours")
        if battery_limit:
            deal_breakers.append("Poor battery life (<4 hours)")
        
        # Noise levels
        noise_limit = st.checkbox("Loud fan noise")
        if noise_limit:
            deal_breakers.append("Loud fan noise")
        
        # Brand preferences
        avoid_brands = st.multiselect(
            "Brands to avoid",
            ["ASUS", "HP", "Dell", "Lenovo", "Acer", "MSI", "Apple"]
        )
        deal_breakers.extend([f"Avoid {brand}" for brand in avoid_brands])
        
        # Build quality
        build_quality = st.checkbox("Plastic build (prefer metal)")
        if build_quality:
            deal_breakers.append("Plastic build quality")
        
        # Price flexibility
        price_flexibility = st.checkbox("Cannot exceed budget by any amount")
        if price_flexibility:
            deal_breakers.append("Strict budget limit")
        
        if st.button("Set Deal Breakers"):
            return deal_breakers
        
        return None