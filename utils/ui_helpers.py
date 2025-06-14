import streamlit as st
import pandas as pd
from typing import List, Dict, Any

def display_chat_message(role: str, content: str):
    """Display a chat message with appropriate styling"""
    
    if role == "user":
        with st.chat_message("user"):
            st.write(content)
    else:
        with st.chat_message("assistant"):
            st.write(content)

def display_product_comparison(products: List[Dict[str, Any]]):
    """Display product comparison in an enhanced format"""
    
    if not products:
        st.markdown("""
        <div style="text-align: center; padding: 2rem; background: #f8f9fa; border-radius: 10px;">
            <h4>🔍 No products found</h4>
            <p>Try adjusting your requirements or being more specific.</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Display products in cards
    for i, product in enumerate(products):
        # Use Streamlit components instead of HTML for better compatibility
        with st.container():
            # Create product card using Streamlit components
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"### {product['name']}")
                
                # Platform badge
                platform_color = "#ff9500" if product['platform'] == "Amazon" else "#047bd6" if product['platform'] == "Flipkart" else "#28a745"
                st.markdown(f"""
                <span style="background-color: {platform_color}; color: white; padding: 0.25rem 0.8rem; border-radius: 20px; font-size: 0.85rem;">
                    {product['platform']}
                </span>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"### ₹{product['price']:,}")
                
                # Discount info
                if product.get('original_price') and product['original_price'] > product['price']:
                    discount_pct = ((product['original_price'] - product['price']) / product['original_price']) * 100
                    st.markdown(f"""
                    <div style="text-align: right;">
                        <span style="color: #7f8c8d; text-decoration: line-through;">₹{product['original_price']:,}</span>
                        <span style="background-color: #28a745; color: white; padding: 0.25rem 0.5rem; border-radius: 15px; font-size: 0.8rem; margin-left: 0.5rem;">
                            {discount_pct:.0f}% OFF
                        </span>
                    </div>
                    """, unsafe_allow_html=True)
            
            # Rating and availability
            col_rating, col_avail = st.columns(2)
            
            with col_rating:
                rating = product.get('rating', 0)
                stars = "⭐" * int(rating) + "☆" * (5 - int(rating))
                st.write(f"**Rating:** {stars} {rating} ({product.get('reviews', 0)} reviews)")
            
            with col_avail:
                availability_color = "#28a745" if product.get('availability') == 'In Stock' else "#ffc107"
                st.markdown(f"""
                **Availability:** <span style="color: {availability_color};">{product.get('availability', 'Unknown')}</span>
                """, unsafe_allow_html=True)
            
            # Key features
            if product.get('key_features'):
                st.markdown("**Key Features:**")
                for feature in product['key_features'][:4]:  # Show only first 4 features
                    st.write(f"• {feature}")
            
            st.markdown("---")  # Separator between products
        
        # Pros and Cons in an expander
        with st.expander(f"📊 Details & Reviews - {product['name']}", expanded=False):
            col1, col2 = st.columns(2)
            
            with col1:
                if product.get('pros'):
                    st.markdown("**✅ Pros:**")
                    for pro in product['pros']:
                        st.write(f"• {pro}")
            
            with col2:
                if product.get('cons'):
                    st.markdown("**❌ Cons:**")
                    for con in product['cons']:
                        st.write(f"• {con}")
            
            # Action buttons
            col_btn1, col_btn2 = st.columns(2)
            
            with col_btn1:
                if st.button(f"🛒 View on {product['platform']}", key=f"view_{i}", use_container_width=True):
                    st.success(f"Opening {product['platform']} link...")
                    # In real implementation, you'd open the product URL
            
            with col_btn2:
                if st.button("⭐ Add to Wishlist", key=f"wishlist_{i}", use_container_width=True):
                    st.success("Added to wishlist!")
    
    # Quick comparison table at the bottom
    if len(products) > 1:
        st.markdown("### 📊 Quick Comparison")
        
        comparison_data = []
        for product in products:
            comparison_data.append({
                "Product": product['name'][:30] + "..." if len(product['name']) > 30 else product['name'],
                "Price (₹)": f"{product['price']:,}",
                "Platform": product['platform'],
                "Rating": f"{product.get('rating', 'N/A')} ⭐",
                "Status": product.get('availability', 'Unknown')
            })
        
        df = pd.DataFrame(comparison_data)
        st.dataframe(df, use_container_width=True, hide_index=True)

def format_price(price: float) -> str:
    """Format price in Indian currency format"""
    return f"₹{price:,.0f}"

def get_price_color(current_price: float, original_price: float = None) -> str:
    """Get color for price display based on discount"""
    if original_price and original_price > current_price:
        return "green"  # Discounted price
    return "black"  # Regular price

def display_requirements_summary(requirements: Dict[str, Any]):
    """Display a summary of user requirements"""
    
    if not requirements:
        return
    
    st.sidebar.subheader("Your Requirements")
    
    for key, value in requirements.items():
        formatted_key = key.replace('_', ' ').title()
        
        if isinstance(value, list):
            formatted_value = ", ".join(value)
        elif key == "budget":
            formatted_value = format_price(value)
        else:
            formatted_value = str(value)
        
        st.sidebar.write(f"**{formatted_key}:** {formatted_value}")

def display_loading_spinner(message: str = "Searching for products..."):
    """Display a loading spinner with message"""
    with st.spinner(message):
        st.empty()

def display_search_stats(products: List[Dict[str, Any]]):
    """Display search statistics"""
    
    if not products:
        return
    
    platforms = list(set(p.get('platform', 'Unknown') for p in products))
    avg_price = sum(p.get('price', 0) for p in products) / len(products)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Products Found", len(products))
    
    with col2:
        st.metric("Platforms", len(platforms))
    
    with col3:
        st.metric("Avg Price", format_price(avg_price))