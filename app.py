import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import hashlib
import json
import base64
from PIL import Image
import io
import plotly.graph_objects as go
import plotly.express as px

# Configure Streamlit
st.set_page_config(
    page_title="RealEstateIreland.ie - Sell Your Home for a Flat Fee",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user = None
    st.session_state.user_type = None

if 'properties' not in st.session_state:
    # Sample properties for demonstration
    st.session_state.properties = [
        {
            'id': 1,
            'title': 'Modern 3-Bed Semi-Detached House',
            'address': '123 Main Street, Dublin 4',
            'price': 450000,
            'bedrooms': 3,
            'bathrooms': 2,
            'size': 120,
            'seller_id': 'seller1',
            'description': 'Beautiful modern home in prime location',
            'images': ['house1.jpg'],
            'listed_date': datetime.now() - timedelta(days=5),
            'status': 'active',
            'bids': [
                {'bidder': 'buyer1', 'amount': 440000, 'date': datetime.now() - timedelta(days=2)},
                {'bidder': 'buyer2', 'amount': 445000, 'date': datetime.now() - timedelta(days=1)}
            ],
            'views': 234,
            'ai_valuation': 455000
        },
        {
            'id': 2,
            'title': 'Spacious 4-Bed Detached House',
            'address': '456 Park Avenue, Dublin 6',
            'price': 650000,
            'bedrooms': 4,
            'bathrooms': 3,
            'size': 180,
            'seller_id': 'seller2',
            'description': 'Stunning family home with large garden',
            'images': ['house2.jpg'],
            'listed_date': datetime.now() - timedelta(days=10),
            'status': 'active',
            'bids': [
                {'bidder': 'buyer3', 'amount': 640000, 'date': datetime.now() - timedelta(days=3)}
            ],
            'views': 189,
            'ai_valuation': 660000
        }
    ]

if 'users' not in st.session_state:
    # Sample users for demonstration
    st.session_state.users = {
        'seller1': {'password': hashlib.md5('pass123'.encode()).hexdigest(), 'type': 'seller', 
                    'name': 'John Doe', 'email': 'john@email.com', 'verified': True},
        'seller2': {'password': hashlib.md5('pass123'.encode()).hexdigest(), 'type': 'seller',
                    'name': 'Jane Smith', 'email': 'jane@email.com', 'verified': True},
        'buyer1': {'password': hashlib.md5('pass123'.encode()).hexdigest(), 'type': 'buyer',
                   'name': 'Mike Johnson', 'email': 'mike@email.com', 'verified': True,
                   'finance_verified': True}
    }

if 'transactions' not in st.session_state:
    st.session_state.transactions = []

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #2c5282;
        text-align: center;
        margin-bottom: 2rem;
    }
    .value-prop {
        background-color: #e6fffa;
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
    }
    .stat-card {
        background-color: #f7fafc;
        padding: 1.5rem;
        border-radius: 8px;
        text-align: center;
        border: 1px solid #e2e8f0;
    }
    .property-card {
        background-color: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
        transition: transform 0.2s;
    }
    .property-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    }
    .bid-badge {
        background-color: #48bb78;
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.875rem;
        font-weight: bold;
    }
    .logo-container {
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 2rem;
    }
    .logo-text {
        font-size: 2.5rem;
        font-weight: bold;
        color: #2c5282;
        margin-left: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Helper Functions
def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()

def authenticate_user(username, password):
    if username in st.session_state.users:
        user = st.session_state.users[username]
        if user['password'] == hash_password(password):
            return True, user
    return False, None

def calculate_ai_valuation(bedrooms, bathrooms, size, location, description=""):
    """Simulate AI property valuation"""
    base_price = 200000
    price_per_bedroom = 50000
    price_per_bathroom = 25000
    price_per_sqm = 2500
    
    # Location multiplier (simplified)
    location_multipliers = {
        'Dublin 4': 1.3, 'Dublin 6': 1.25, 'Dublin 2': 1.35,
        'Dublin 1': 1.1, 'Dublin 8': 1.15
    }
    
    location_mult = 1.0
    for area, mult in location_multipliers.items():
        if area.lower() in location.lower():
            location_mult = mult
            break
    
    valuation = (base_price + 
                 (bedrooms * price_per_bedroom) + 
                 (bathrooms * price_per_bathroom) + 
                 (size * price_per_sqm)) * location_mult
    
    # Add some randomness to simulate market conditions
    valuation *= np.random.uniform(0.95, 1.05)
    
    return int(valuation)

def format_currency(amount):
    return f"€{amount:,.0f}"

# Sidebar Navigation
with st.sidebar:
    st.markdown("""
    <div style='text-align: center; margin-bottom: 2rem;'>
        <div style='font-size: 3rem;'>🏠</div>
        <div style='font-size: 1.5rem; font-weight: bold; color: #2c5282;'>
            RealEstate<br>Ireland.ie
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.logged_in:
        st.write(f"Welcome, **{st.session_state.user['name']}**")
        st.write(f"Account Type: **{st.session_state.user_type.title()}**")
        
        if st.button("Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.user = None
            st.session_state.user_type = None
            st.rerun()
    
    st.markdown("---")
    
    # Navigation menu
    if st.session_state.logged_in:
        if st.session_state.user_type == 'seller':
            page = st.radio("Navigation", 
                           ["Dashboard", "List Property", "My Listings", "Analytics", "Legal Documents"])
        else:
            page = st.radio("Navigation", 
                           ["Browse Properties", "My Bids", "Saved Properties", "Profile"])
    else:
        page = st.radio("Navigation", 
                       ["Home", "How It Works", "Browse Properties", "Login/Register", "Contact"])

# Main Content Area
if not st.session_state.logged_in:
    if page == "Home":
        # Hero Section
        st.markdown("<h1 class='main-header'>Sell Your Home for a Flat Fee of €1,500</h1>", 
                   unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("""
            <div class='stat-card'>
                <h2 style='color: #48bb78;'>€10,000+</h2>
                <p>Average Savings vs Traditional Agents</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class='stat-card'>
                <h2 style='color: #4299e1;'>100%</h2>
                <p>Transparent & Secure Process</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class='stat-card'>
                <h2 style='color: #ed8936;'>24/7</h2>
                <p>Platform Access & Support</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Value Proposition
        st.markdown("""
        <div class='value-prop'>
            <h2>Why Choose RealEstateIreland.ie?</h2>
            <p style='font-size: 1.2rem;'>The Irish property market is highly competitive. 
            Properties in Dublin sold for 8.6% above asking price in Q4 2024. 
            Traditional agents charge 1-2% commission plus VAT. On a €600,000 property, 
            that's €12,000+ in fees!</p>
            <p style='font-size: 1.2rem; font-weight: bold;'>
            We charge just €1,500 flat fee - saving you thousands!</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Features Grid
        st.markdown("### Our Revolutionary Features")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🏠 For Sellers")
            st.markdown("""
            - **AI-Powered Valuation**: Get accurate property valuations instantly
            - **Direct Listing**: Upload photos and details yourself
            - **Full Control**: Manage viewings and negotiations directly
            - **Legal Support**: Partnership with top law firms
            - **Real-time Analytics**: Track views, bids, and interest
            """)
        
        with col2:
            st.markdown("#### 🔍 For Buyers")
            st.markdown("""
            - **Legally Binding Offers**: 10% deposit secures your bid
            - **Transparent Bidding**: See all offers in real-time
            - **Verified Sellers**: All properties and owners verified
            - **Digital Timeline**: Track purchase progress online
            - **Secure Escrow**: Protected payments through escrow
            """)
        
        # Call to Action
        st.markdown("---")
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            if st.button("Start Selling Today - Save Thousands!", 
                        use_container_width=True, type="primary"):
                st.session_state.selected_page = "Login/Register"
                st.rerun()
    
    elif page == "How It Works":
        st.markdown("<h1 class='main-header'>How It Works</h1>", unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["For Sellers", "For Buyers"])
        
        with tab1:
            st.markdown("### Simple 4-Step Process for Sellers")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown("""
                <div class='stat-card'>
                    <h1>1️⃣</h1>
                    <h4>Register & Verify</h4>
                    <p>Create account and verify your identity</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown("""
                <div class='stat-card'>
                    <h1>2️⃣</h1>
                    <h4>List Property</h4>
                    <p>Upload photos & details, get AI valuation</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown("""
                <div class='stat-card'>
                    <h1>3️⃣</h1>
                    <h4>Receive Bids</h4>
                    <p>Review offers with full transparency</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                st.markdown("""
                <div class='stat-card'>
                    <h1>4️⃣</h1>
                    <h4>Complete Sale</h4>
                    <p>Legal team handles paperwork</p>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("---")
            st.markdown("### Cost Comparison")
            
            # Create comparison chart
            traditional_fee = 600000 * 0.015 * 1.23  # 1.5% + VAT
            our_fee = 1500
            
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=['Traditional Agent', 'RealEstateIreland.ie'],
                y=[traditional_fee, our_fee],
                text=[f'€{traditional_fee:,.0f}', f'€{our_fee:,.0f}'],
                textposition='auto',
                marker_color=['#e53e3e', '#48bb78']
            ))
            fig.update_layout(
                title="Fees on €600,000 Property Sale",
                yaxis_title="Total Fees (€)",
                showlegend=False,
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            st.markdown("### Secure Buying Process")
            
            st.markdown("""
            1. **Browse Properties**: Search verified listings with transparent pricing
            2. **Make an Offer**: Submit legally binding offer with 10% deposit
            3. **Track Progress**: Monitor every step through digital timeline
            4. **Complete Purchase**: Our legal partners ensure smooth transfer
            
            #### Buyer Protection Features:
            - ✅ Escrow-protected deposits
            - ✅ Verified seller identities
            - ✅ Legal binding agreements
            - ✅ Full bidding transparency
            - ✅ Professional legal support
            """)
    
    elif page == "Browse Properties":
        st.markdown("<h1 class='main-header'>Browse Properties</h1>", unsafe_allow_html=True)
        
        # Filters
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            min_price = st.number_input("Min Price (€)", min_value=0, max_value=2000000, 
                                       value=0, step=50000)
        with col2:
            max_price = st.number_input("Max Price (€)", min_value=0, max_value=2000000, 
                                       value=1000000, step=50000)
        with col3:
            bedrooms = st.selectbox("Bedrooms", ["Any", "1", "2", "3", "4", "5+"])
        with col4:
            sort_by = st.selectbox("Sort By", ["Newest", "Price (Low-High)", "Price (High-Low)"])
        
        # Display properties
        filtered_properties = st.session_state.properties.copy()
        
        # Apply filters
        filtered_properties = [p for p in filtered_properties 
                             if p['price'] >= min_price and p['price'] <= max_price]
        
        if bedrooms != "Any":
            if bedrooms == "5+":
                filtered_properties = [p for p in filtered_properties if p['bedrooms'] >= 5]
            else:
                filtered_properties = [p for p in filtered_properties 
                                     if p['bedrooms'] == int(bedrooms)]
        
        # Sort
        if sort_by == "Price (Low-High)":
            filtered_properties.sort(key=lambda x: x['price'])
        elif sort_by == "Price (High-Low)":
            filtered_properties.sort(key=lambda x: x['price'], reverse=True)
        else:
            filtered_properties.sort(key=lambda x: x['listed_date'], reverse=True)
        
        st.markdown(f"### Found {len(filtered_properties)} Properties")
        
        # Display properties in grid
        for i in range(0, len(filtered_properties), 2):
            col1, col2 = st.columns(2)
            
            for j, col in enumerate([col1, col2]):
                if i + j < len(filtered_properties):
                    prop = filtered_properties[i + j]
                    with col:
                        st.markdown(f"""
                        <div class='property-card'>
                            <h4>{prop['title']}</h4>
                            <p>📍 {prop['address']}</p>
                            <h3 style='color: #2c5282;'>{format_currency(prop['price'])}</h3>
                            <p>🛏️ {prop['bedrooms']} beds | 🚿 {prop['bathrooms']} baths | 
                               📐 {prop['size']}m²</p>
                            <p>👁️ {prop['views']} views | 
                               <span class='bid-badge'>{len(prop['bids'])} bids</span></p>
                            <p><strong>AI Valuation:</strong> {format_currency(prop['ai_valuation'])}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        if st.button(f"View Details", key=f"view_{prop['id']}"):
                            st.info("Please login to view full details and make offers")
    
    elif page == "Login/Register":
        st.markdown("<h1 class='main-header'>Login or Register</h1>", unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["Login", "Register"])
        
        with tab1:
            st.markdown("### Login to Your Account")
            
            col1, col2, col3 = st.columns([1,2,1])
            with col2:
                username = st.text_input("Username", key="login_username")
                password = st.text_input("Password", type="password", key="login_password")
                
                if st.button("Login", use_container_width=True, type="primary"):
                    success, user = authenticate_user(username, password)
                    if success:
                        st.session_state.logged_in = True
                        st.session_state.user = user
                        st.session_state.user_type = user['type']
                        st.success("Login successful!")
                        st.rerun()
                    else:
                        st.error("Invalid username or password")
                
                st.info("Demo accounts: seller1/pass123, buyer1/pass123")
        
        with tab2:
            st.markdown("### Create New Account")
            
            col1, col2, col3 = st.columns([1,2,1])
            with col2:
                account_type = st.radio("I want to:", ["Sell a Property", "Buy a Property"])
                new_username = st.text_input("Choose Username", key="reg_username")
                new_email = st.text_input("Email Address", key="reg_email")
                new_name = st.text_input("Full Name", key="reg_name")
                new_password = st.text_input("Password", type="password", key="reg_password")
                confirm_password = st.text_input("Confirm Password", type="password", 
                                               key="reg_confirm")
                
                terms = st.checkbox("I agree to the Terms of Service and Privacy Policy")
                
                if st.button("Register", use_container_width=True, type="primary"):
                    if new_username in st.session_state.users:
                        st.error("Username already exists")
                    elif new_password != confirm_password:
                        st.error("Passwords do not match")
                    elif not terms:
                        st.error("Please accept the terms and conditions")
                    elif not all([new_username, new_email, new_name, new_password]):
                        st.error("Please fill in all fields")
                    else:
                        # Create new user
                        user_type = 'seller' if account_type == "Sell a Property" else 'buyer'
                        st.session_state.users[new_username] = {
                            'password': hash_password(new_password),
                            'type': user_type,
                            'name': new_name,
                            'email': new_email,
                            'verified': False
                        }
                        st.success("Registration successful! Please login.")
                        st.balloons()
    
    elif page == "Contact":
        st.markdown("<h1 class='main-header'>Contact Us</h1>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            ### Get in Touch
            
            **RealEstateIreland.ie**  
            123 Nassau Street  
            Dublin 2, D02 XY45  
            Ireland
            
            📧 info@realestateireland.ie  
            📞 +353 1 234 5678  
            💬 Live Chat: Available 24/7
            
            **Office Hours:**  
            Monday - Friday: 9:00 AM - 6:00 PM  
            Saturday: 10:00 AM - 4:00 PM  
            Sunday: Closed
            """)
        
        with col2:
            st.markdown("### Send us a Message")
            
            contact_name = st.text_input("Your Name")
            contact_email = st.text_input("Your Email")
            contact_subject = st.selectbox("Subject", 
                                         ["General Inquiry", "Selling Property", 
                                          "Buying Property", "Technical Support", "Other"])
            contact_message = st.text_area("Message", height=150)
            
            if st.button("Send Message", use_container_width=True, type="primary"):
                if all([contact_name, contact_email, contact_message]):
                    st.success("Thank you for your message! We'll respond within 24 hours.")
                else:
                    st.error("Please fill in all fields")

else:  # User is logged in
    if st.session_state.user_type == 'seller':
        if page == "Dashboard":
            st.markdown(f"<h1 class='main-header'>Welcome back, {st.session_state.user['name']}!</h1>", 
                       unsafe_allow_html=True)
            
            # Get seller's properties
            seller_properties = [p for p in st.session_state.properties 
                               if p['seller_id'] == st.session_state.logged_in]
            
            # Dashboard metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                total_value = sum(p['price'] for p in seller_properties)
                st.metric("Total Portfolio Value", format_currency(total_value))
            
            with col2:
                total_views = sum(p['views'] for p in seller_properties)
                st.metric("Total Views", f"{total_views:,}")
            
            with col3:
                total_bids = sum(len(p['bids']) for p in seller_properties)
                st.metric("Total Bids Received", total_bids)
            
            with col4:
                active_listings = len([p for p in seller_properties if p['status'] == 'active'])
                st.metric("Active Listings", active_listings)
            
            st.markdown("---")
            
            # Recent Activity
            st.markdown("### Recent Activity")
            
            if seller_properties:
                # Get all recent bids
                recent_bids = []
                for prop in seller_properties:
                    for bid in prop['bids']:
                        recent_bids.append({
                            'property': prop['title'],
                            'bidder': bid['bidder'],
                            'amount': bid['amount'],
                            'date': bid['date']
                        })
                
                recent_bids.sort(key=lambda x: x['date'], reverse=True)
                
                if recent_bids:
                    for bid in recent_bids[:5]:
                        st.info(f"**New bid** on {bid['property']}: "
                               f"{format_currency(bid['amount'])} from {bid['bidder']} "
                               f"({bid['date'].strftime('%d %b %Y')})")
                else:
                    st.info("No recent activity")
            else:
                st.info("You don't have any properties listed yet. Start by listing your first property!")
        
        elif page == "List Property":
            st.markdown("<h1 class='main-header'>List Your Property</h1>", unsafe_allow_html=True)
            
            with st.form("property_listing"):
                st.markdown("### Property Details")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    title = st.text_input("Property Title", 
                                        placeholder="e.g., Modern 3-Bed Semi-Detached House")
                    address = st.text_input("Full Address", 
                                          placeholder="e.g., 123 Main Street, Dublin 4")
                    bedrooms = st.number_input("Number of Bedrooms", min_value=1, max_value=10, value=3)
                    bathrooms = st.number_input("Number of Bathrooms", min_value=1, max_value=5, value=2)
                
                with col2:
                    size = st.number_input("Property Size (m²)", min_value=20, max_value=1000, value=100)
                    price = st.number_input("Asking Price (€)", min_value=50000, max_value=5000000, 
                                          value=450000, step=10000)
                    property_type = st.selectbox("Property Type", 
                                               ["Detached", "Semi-Detached", "Terraced", "Apartment"])
                    ber_rating = st.selectbox("BER Rating", 
                                            ["A1", "A2", "A3", "B1", "B2", "B3", "C1", "C2", "C3", 
                                             "D1", "D2", "E1", "E2", "F", "G"])
                
                description = st.text_area("Property Description", 
                                         placeholder="Describe your property's key features...", 
                                         height=150)
                
                st.markdown("### Upload Photos")
                photos = st.file_uploader("Upload property photos", 
                                        type=['jpg', 'jpeg', 'png'], 
                                        accept_multiple_files=True)
                
                st.markdown("### AI Valuation")
                if st.checkbox("Get AI-Powered Valuation"):
                    ai_val = calculate_ai_valuation(bedrooms, bathrooms, size, address, description)
                    st.success(f"AI Estimated Value: {format_currency(ai_val)}")
                    st.info("This valuation is based on property characteristics and local market data")
                
                st.markdown("### Legal Documents")
                st.info("Our partner law firm will handle all legal documentation. "
                       "Fee: €850 (included in total cost)")
                
                terms = st.checkbox("I confirm I am the legal owner of this property")
                
                submitted = st.form_submit_button("List Property (€1,500 Total Fee)", 
                                                type="primary", use_container_width=True)
                
                if submitted:
                    if not all([title, address, description, terms]):
                        st.error("Please fill in all required fields and confirm ownership")
                    else:
                        # Add new property
                        new_property = {
                            'id': len(st.session_state.properties) + 1,
                            'title': title,
                            'address': address,
                            'price': price,
                            'bedrooms': bedrooms,
                            'bathrooms': bathrooms,
                            'size': size,
                            'seller_id': st.session_state.logged_in,
                            'description': description,
                            'images': ['property.jpg'],
                            'listed_date': datetime.now(),
                            'status': 'active',
                            'bids': [],
                            'views': 0,
                            'ai_valuation': ai_val if 'ai_val' in locals() else price * 1.05
                        }
                        st.session_state.properties.append(new_property)
                        st.success("Property listed successfully! You'll receive an invoice for €1,500.")
                        st.balloons()
        
        elif page == "My Listings":
            st.markdown("<h1 class='main-header'>My Property Listings</h1>", unsafe_allow_html=True)
            
            # Get seller's properties
            seller_properties = [p for p in st.session_state.properties 
                               if p.get('seller_id') == st.session_state.logged_in]
            
            if not seller_properties:
                st.info("You haven't listed any properties yet.")
            else:
                for prop in seller_properties:
                    with st.expander(f"{prop['title']} - {format_currency(prop['price'])}", 
                                   expanded=True):
                        col1, col2, col3 = st.columns([2,1,1])
                        
                        with col1:
                            st.markdown(f"**Address:** {prop['address']}")
                            st.markdown(f"**Details:** {prop['bedrooms']} beds, "
                                      f"{prop['bathrooms']} baths, {prop['size']}m²")
                            st.markdown(f"**Listed:** {prop['listed_date'].strftime('%d %b %Y')}")
                            st.markdown(f"**Status:** {prop['status'].title()}")
                        
                        with col2:
                            st.metric("Views", prop['views'])
                            st.metric("Bids", len(prop['bids']))
                        
                        with col3:
                            st.metric("Highest Bid", 
                                    format_currency(max([b['amount'] for b in prop['bids']]) 
                                                   if prop['bids'] else 0))
                            st.metric("AI Valuation", format_currency(prop['ai_valuation']))
                        
                        if prop['bids']:
                            st.markdown("#### Recent Bids")
                            bid_df = pd.DataFrame(prop['bids'])
                            bid_df['amount'] = bid_df['amount'].apply(format_currency)
                            bid_df['date'] = bid_df['date'].dt.strftime('%d %b %Y')
                            st.dataframe(bid_df[['bidder', 'amount', 'date']], 
                                       use_container_width=True)
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            if st.button(f"Edit Listing", key=f"edit_{prop['id']}"):
                                st.info("Edit functionality coming soon")
                        with col2:
                            if st.button(f"Accept Offer", key=f"accept_{prop['id']}", 
                                       disabled=len(prop['bids']) == 0):
                                st.success("Legal documents will be prepared by our partner firm")
                        with col3:
                            if st.button(f"Remove Listing", key=f"remove_{prop['id']}"):
                                prop['status'] = 'removed'
                                st.success("Listing removed")
                                st.rerun()
        
        elif page == "Analytics":
            st.markdown("<h1 class='main-header'>Property Analytics</h1>", unsafe_allow_html=True)
            
            # Get seller's properties
            seller_properties = [p for p in st.session_state.properties 
                               if p.get('seller_id') == st.session_state.logged_in]
            
            if not seller_properties:
                st.info("No properties to analyze. List a property to see analytics.")
            else:
                # Overview metrics
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    avg_views = np.mean([p['views'] for p in seller_properties])
                    st.metric("Avg Views per Property", f"{avg_views:.0f}")
                
                with col2:
                    avg_bids = np.mean([len(p['bids']) for p in seller_properties])
                    st.metric("Avg Bids per Property", f"{avg_bids:.1f}")
                
                with col3:
                    conversion_rate = (len([p for p in seller_properties if p['bids']]) / 
                                     len(seller_properties) * 100)
                    st.metric("Bid Conversion Rate", f"{conversion_rate:.0f}%")
                
                with col4:
                    if any(p['bids'] for p in seller_properties):
                        all_bids = []
                        for p in seller_properties:
                            all_bids.extend([b['amount'] for b in p['bids']])
                        avg_bid = np.mean(all_bids) if all_bids else 0
                    else:
                        avg_bid = 0
                    st.metric("Avg Bid Amount", format_currency(avg_bid))
                
                st.markdown("---")
                
                # Views over time (simulated)
                st.markdown("### Views Over Time")
                dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
                views_data = np.random.poisson(10, size=30).cumsum()
                
                fig = px.line(x=dates, y=views_data, labels={'x': 'Date', 'y': 'Total Views'})
                fig.update_layout(showlegend=False)
                st.plotly_chart(fig, use_container_width=True)
                
                # Property comparison
                if len(seller_properties) > 1:
                    st.markdown("### Property Performance Comparison")
                    
                    prop_names = [p['title'][:30] + '...' if len(p['title']) > 30 
                                 else p['title'] for p in seller_properties]
                    prop_views = [p['views'] for p in seller_properties]
                    prop_bids = [len(p['bids']) for p in seller_properties]
                    
                    fig = go.Figure()
                    fig.add_trace(go.Bar(name='Views', x=prop_names, y=prop_views))
                    fig.add_trace(go.Bar(name='Bids', x=prop_names, y=prop_bids))
                    fig.update_layout(barmode='group')
                    st.plotly_chart(fig, use_container_width=True)
                
                # Market insights
                st.markdown("### Market Insights")
                col1, col2 = st.columns(2)
                
                with col1:
                    st.info("🔥 Properties in Dublin 4 are receiving 23% more views than average")
                    st.info("📈 3-bedroom properties are in highest demand this month")
                
                with col2:
                    st.info("💰 Properties priced 5-10% below AI valuation sell 40% faster")
                    st.info("📸 Listings with 10+ photos receive 2x more inquiries")
        
        elif page == "Legal Documents":
            st.markdown("<h1 class='main-header'>Legal Documents & Process</h1>", unsafe_allow_html=True)
            
            st.markdown("""
            ### Our Legal Partnership
            
            We've partnered with **McCarthy & Associates Solicitors** to handle all legal aspects 
            of your property sale. This ensures a smooth, secure transaction for all parties.
            
            #### What's Included (€850 flat fee):
            - ✅ Title deed verification
            - ✅ Contract preparation
            - ✅ Buyer deposit handling via escrow
            - ✅ All legal searches and checks
            - ✅ Completion of sale documentation
            - ✅ Registration with Property Registration Authority
            
            #### Digital Timeline Tracker
            Track your sale progress in real-time:
            """)
            
            # Progress tracker
            stages = [
                ("Listing Active", 100),
                ("Offer Accepted", 75),
                ("Contracts Drafted", 50),
                ("Surveys Complete", 25),
                ("Sale Completed", 0)
            ]
            
            for stage, progress in stages:
                col1, col2 = st.columns([3,1])
                with col1:
                    st.progress(progress/100)
                with col2:
                    st.write(stage)
            
            st.markdown("---")
            
            st.markdown("""
            ### Required Documents
            
            Please have the following ready:
            - Property title deeds
            - Planning permissions (if applicable)
            - BER certificate
            - Property tax clearance
            - Proof of identity
            - Bank account details for proceeds
            
            ### Download Templates
            """)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.button("📄 Sale Agreement Template", use_container_width=True)
            with col2:
                st.button("📋 Property Disclosure Form", use_container_width=True)
            with col3:
                st.button("📑 Legal Checklist", use_container_width=True)
    
    else:  # Buyer pages
        if page == "Browse Properties":
            st.markdown("<h1 class='main-header'>Browse Properties</h1>", unsafe_allow_html=True)
            
            # Enhanced filters for logged-in buyers
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                min_price = st.number_input("Min Price (€)", min_value=0, max_value=2000000, 
                                           value=0, step=50000)
            with col2:
                max_price = st.number_input("Max Price (€)", min_value=0, max_value=2000000, 
                                           value=1000000, step=50000)
            with col3:
                bedrooms = st.selectbox("Bedrooms", ["Any", "1", "2", "3", "4", "5+"])
            with col4:
                property_type = st.selectbox("Type", ["Any", "Detached", "Semi-Detached", 
                                                     "Terraced", "Apartment"])
            
            # Display properties with bidding functionality
            active_properties = [p for p in st.session_state.properties if p['status'] == 'active']
            
            for prop in active_properties:
                with st.expander(f"{prop['title']} - {format_currency(prop['price'])}", 
                               expanded=False):
                    col1, col2 = st.columns([2,1])
                    
                    with col1:
                        st.markdown(f"**Address:** {prop['address']}")
                        st.markdown(f"**Details:** {prop['bedrooms']} beds, "
                                  f"{prop['bathrooms']} baths, {prop['size']}m²")
                        st.markdown(f"**Description:** {prop['description']}")
                        st.markdown(f"**AI Valuation:** {format_currency(prop['ai_valuation'])}")
                        
                        # Bidding history
                        if prop['bids']:
                            st.markdown("**Recent Bids:**")
                            for bid in prop['bids'][-3:]:
                                st.write(f"- {format_currency(bid['amount'])} "
                                       f"({bid['date'].strftime('%d %b')})")
                    
                    with col2:
                        # Increment view count
                        prop['views'] += 1
                        
                        st.metric("Current Price", format_currency(prop['price']))
                        st.metric("Highest Bid", 
                                format_currency(max([b['amount'] for b in prop['bids']]) 
                                               if prop['bids'] else 0))
                        
                        # Bidding form
                        bid_amount = st.number_input(f"Your Bid (€)", 
                                                   min_value=int(prop['price'] * 0.9),
                                                   max_value=int(prop['price'] * 1.5),
                                                   value=prop['price'],
                                                   step=5000,
                                                   key=f"bid_{prop['id']}")
                        
                        if st.button(f"Place Bid", key=f"submit_bid_{prop['id']}", 
                                   type="primary"):
                            # Add bid
                            prop['bids'].append({
                                'bidder': st.session_state.user['name'],
                                'amount': bid_amount,
                                'date': datetime.now()
                            })
                            st.success(f"Bid of {format_currency(bid_amount)} placed! "
                                     "10% deposit (€{:,.0f}) will be required to secure.".format(bid_amount * 0.1))
                            st.rerun()
                        
                        if st.button(f"💾 Save Property", key=f"save_{prop['id']}"):
                            st.success("Property saved to your list")
        
        elif page == "My Bids":
            st.markdown("<h1 class='main-header'>My Bids</h1>", unsafe_allow_html=True)
            
            # Find all bids by current user
            my_bids = []
            for prop in st.session_state.properties:
                for bid in prop['bids']:
                    if bid['bidder'] == st.session_state.user['name']:
                        my_bids.append({
                            'property': prop['title'],
                            'address': prop['address'],
                            'asking_price': prop['price'],
                            'bid_amount': bid['amount'],
                            'bid_date': bid['date'],
                            'highest_bid': max([b['amount'] for b in prop['bids']]),
                            'status': 'Winning' if bid['amount'] == max([b['amount'] for b in prop['bids']]) else 'Outbid'
                        })
            
            if my_bids:
                for bid in my_bids:
                    status_color = "🟢" if bid['status'] == 'Winning' else "🔴"
                    
                    with st.expander(f"{status_color} {bid['property']} - {bid['status']}"):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.markdown(f"**Address:** {bid['address']}")
                            st.markdown(f"**Asking Price:** {format_currency(bid['asking_price'])}")
                            st.markdown(f"**Your Bid:** {format_currency(bid['bid_amount'])}")
                            st.markdown(f"**Highest Bid:** {format_currency(bid['highest_bid'])}")
                        
                        with col2:
                            st.markdown(f"**Bid Date:** {bid['bid_date'].strftime('%d %b %Y')}")
                            st.markdown(f"**Status:** {bid['status']}")
                            
                            if bid['status'] == 'Winning':
                                if st.button(f"Proceed to Deposit", key=f"deposit_{bid['property']}"):
                                    st.success("Deposit of €{:,.0f} required. "
                                             "Legal documents will be sent within 24 hours.".format(bid['bid_amount'] * 0.1))
                            else:
                                if st.button(f"Increase Bid", key=f"increase_{bid['property']}"):
                                    st.info("Go to Browse Properties to place a higher bid")
            else:
                st.info("You haven't placed any bids yet.")
        
        elif page == "Saved Properties":
            st.markdown("<h1 class='main-header'>Saved Properties</h1>", unsafe_allow_html=True)
            st.info("Your saved properties will appear here. This feature is coming soon!")
        
        elif page == "Profile":
            st.markdown("<h1 class='main-header'>My Profile</h1>", unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### Account Information")
                st.write(f"**Name:** {st.session_state.user['name']}")
                st.write(f"**Email:** {st.session_state.user['email']}")
                st.write(f"**Account Type:** {st.session_state.user_type.title()}")
                st.write(f"**Verified:** {'✅ Yes' if st.session_state.user.get('verified') else '❌ No'}")
                
                if st.session_state.user_type == 'buyer':
                    st.write(f"**Finance Verified:** {'✅ Yes' if st.session_state.user.get('finance_verified') else '❌ No'}")
                
                st.markdown("---")
                
                st.markdown("### Verification Status")
                if not st.session_state.user.get('verified'):
                    if st.button("Verify Identity", type="primary"):
                        st.session_state.user['verified'] = True
                        st.success("Identity verified! You can now place binding offers.")
                        st.rerun()
                
                if st.session_state.user_type == 'buyer' and not st.session_state.user.get('finance_verified'):
                    if st.button("Verify Finances", type="primary"):
                        st.session_state.user['finance_verified'] = True
                        st.success("Finances verified! Your bids will be prioritized.")
                        st.rerun()
            
            with col2:
                st.markdown("### Account Settings")
                
                with st.form("update_profile"):
                    new_email = st.text_input("Update Email", value=st.session_state.user['email'])
                    new_phone = st.text_input("Phone Number", value="+353 1 234 5678")
                    
                    notifications = st.checkbox("Email Notifications", value=True)
                    sms_alerts = st.checkbox("SMS Alerts for Bids", value=False)
                    
                    if st.form_submit_button("Update Profile"):
                        st.session_state.user['email'] = new_email
                        st.success("Profile updated successfully!")
                
                st.markdown("---")
                
                if st.button("Change Password"):
                    st.info("Password change functionality coming soon")
                
                if st.button("Delete Account", type="secondary"):
                    st.warning("Account deletion is permanent. Please contact support.")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #718096; padding: 2rem;'>
    <p>© 2025 RealEstateIreland.ie - Revolutionizing Property Sales in Ireland</p>
    <p>Save thousands on estate agent fees. Sell your home for just €1,500 flat fee.</p>
    <p>🔒 Secure | 📱 24/7 Access | 🤝 Legal Support | 🏆 Trusted by 1000+ Sellers</p>
</div>
""", unsafe_allow_html=True)
