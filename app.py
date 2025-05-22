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
import requests
from io import BytesIO

# Configure Streamlit
st.set_page_config(
    page_title="RealEstateIreland.ie - Premium Property Sales Platform",
    page_icon="RE",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user = None
    st.session_state.user_type = None

# Property images (using placeholder images)
property_images = [
    "https://images.unsplash.com/photo-1568605114967-8130f3a36994?w=800&q=80",
    "https://images.unsplash.com/photo-1583608205776-bfd35f0d9f83?w=800&q=80",
    "https://images.unsplash.com/photo-1572120360610-d971b9d7767c?w=800&q=80",
    "https://images.unsplash.com/photo-1570129477492-45c003edd2be?w=800&q=80",
    "https://images.unsplash.com/photo-1554995207-c18c203602cb?w=800&q=80",
    "https://images.unsplash.com/photo-1560184897-ae75f418493e?w=800&q=80",
    "https://images.unsplash.com/photo-1558036117-15d82a90b9b1?w=800&q=80",
    "https://images.unsplash.com/photo-1564013799919-ab600027ffc6?w=800&q=80"
]

if 'properties' not in st.session_state:
    # Sample properties for demonstration
    st.session_state.properties = [
        {
            'id': 1,
            'title': 'Contemporary Georgian Residence',
            'address': '42 Fitzwilliam Square, Dublin 2',
            'price': 1250000,
            'bedrooms': 5,
            'bathrooms': 3,
            'size': 280,
            'seller_id': 'seller1',
            'description': 'Exquisite Georgian property meticulously restored with contemporary luxury finishes. Period features throughout including original fireplaces and cornicing.',
            'images': [property_images[0], property_images[1]],
            'listed_date': datetime.now() - timedelta(days=5),
            'status': 'active',
            'bids': [
                {'bidder': 'buyer1', 'amount': 1200000, 'date': datetime.now() - timedelta(days=2)},
                {'bidder': 'buyer2', 'amount': 1225000, 'date': datetime.now() - timedelta(days=1)}
            ],
            'views': 234,
            'ai_valuation': 1275000,
            'property_type': 'Detached',
            'ber_rating': 'B2'
        },
        {
            'id': 2,
            'title': 'Modern Architectural Masterpiece',
            'address': '15 Shrewsbury Road, Dublin 4',
            'price': 2850000,
            'bedrooms': 6,
            'bathrooms': 5,
            'size': 450,
            'seller_id': 'seller2',
            'description': 'Award-winning contemporary design featuring floor-to-ceiling windows, infinity pool, and smart home technology throughout.',
            'images': [property_images[2], property_images[3]],
            'listed_date': datetime.now() - timedelta(days=10),
            'status': 'active',
            'bids': [
                {'bidder': 'buyer3', 'amount': 2750000, 'date': datetime.now() - timedelta(days=3)}
            ],
            'views': 189,
            'ai_valuation': 2900000,
            'property_type': 'Detached',
            'ber_rating': 'A2'
        },
        {
            'id': 3,
            'title': 'Penthouse at Grand Canal Dock',
            'address': 'Capital Dock, Dublin 2',
            'price': 1850000,
            'bedrooms': 3,
            'bathrooms': 3,
            'size': 200,
            'seller_id': 'seller1',
            'description': 'Stunning penthouse with panoramic city views, private terrace, and concierge service. Premium finishes throughout.',
            'images': [property_images[4], property_images[5]],
            'listed_date': datetime.now() - timedelta(days=7),
            'status': 'active',
            'bids': [],
            'views': 156,
            'ai_valuation': 1900000,
            'property_type': 'Apartment',
            'ber_rating': 'A1'
        }
    ]

if 'users' not in st.session_state:
    # Sample users for demonstration
    st.session_state.users = {
        'seller1': {'password': hashlib.md5('pass123'.encode()).hexdigest(), 'type': 'seller', 
                    'name': 'Jonathan Fitzgerald', 'email': 'j.fitzgerald@email.com', 'verified': True},
        'seller2': {'password': hashlib.md5('pass123'.encode()).hexdigest(), 'type': 'seller',
                    'name': 'Catherine O\'Sullivan', 'email': 'c.osullivan@email.com', 'verified': True},
        'buyer1': {'password': hashlib.md5('pass123'.encode()).hexdigest(), 'type': 'buyer',
                   'name': 'Michael Chen', 'email': 'm.chen@email.com', 'verified': True,
                   'finance_verified': True}
    }

if 'transactions' not in st.session_state:
    st.session_state.transactions = []

# Premium CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Inter:wght@300;400;500;600&display=swap');
    
    .main {
        font-family: 'Inter', sans-serif;
    }
    
    .main-header {
        font-family: 'Playfair Display', serif;
        font-size: 3.5rem;
        font-weight: 700;
        color: #1a2332;
        text-align: center;
        margin-bottom: 3rem;
        letter-spacing: -0.02em;
    }
    
    .section-header {
        font-family: 'Playfair Display', serif;
        font-size: 2.5rem;
        font-weight: 700;
        color: #1a2332;
        margin: 2rem 0 1.5rem 0;
    }
    
    .value-prop {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 3rem;
        border-radius: 20px;
        margin-bottom: 3rem;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }
    
    .stat-card {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        border: 1px solid #e5e7eb;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        transition: all 0.3s ease;
        height: 100%;
    }
    
    .stat-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 30px rgba(0,0,0,0.12);
    }
    
    .stat-value {
        font-size: 2.5rem;
        font-weight: 600;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    
    .property-card {
        background: white;
        border-radius: 20px;
        overflow: hidden;
        box-shadow: 0 8px 30px rgba(0,0,0,0.08);
        margin-bottom: 2rem;
        transition: all 0.3s ease;
    }
    
    .property-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(0,0,0,0.15);
    }
    
    .property-image {
        width: 100%;
        height: 250px;
        object-fit: cover;
    }
    
    .property-details {
        padding: 2rem;
    }
    
    .price-tag {
        font-size: 2rem;
        font-weight: 600;
        color: #1a2332;
        margin: 1rem 0;
    }
    
    .premium-button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.75rem 2rem;
        border-radius: 50px;
        border: none;
        font-weight: 500;
        letter-spacing: 0.5px;
        transition: all 0.3s ease;
        cursor: pointer;
        display: inline-block;
        text-decoration: none;
    }
    
    .premium-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4);
    }
    
    .bid-status {
        background: #10b981;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 25px;
        font-size: 0.875rem;
        font-weight: 500;
        display: inline-block;
    }
    
    .metric-container {
        background: #f9fafb;
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 1rem;
    }
    
    .sidebar-header {
        font-family: 'Playfair Display', serif;
        font-size: 1.8rem;
        font-weight: 700;
        color: #1a2332;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 2rem;
        margin: 2rem 0;
    }
    
    .feature-card {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        border: 1px solid #e5e7eb;
        transition: all 0.3s ease;
    }
    
    .feature-card:hover {
        border-color: #667eea;
        box-shadow: 0 4px 20px rgba(102, 126, 234, 0.1);
    }
    
    .logo-text {
        font-family: 'Playfair Display', serif;
        font-size: 2rem;
        font-weight: 700;
        color: #1a2332;
        text-align: center;
    }
    
    .sub-logo-text {
        font-size: 0.9rem;
        color: #64748b;
        text-align: center;
        margin-top: -0.5rem;
    }
    
    .property-meta {
        display: flex;
        gap: 1.5rem;
        margin: 1rem 0;
        color: #64748b;
        font-size: 0.95rem;
    }
    
    .divider {
        height: 1px;
        background: linear-gradient(to right, transparent, #e5e7eb, transparent);
        margin: 3rem 0;
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

def calculate_ai_valuation(bedrooms, bathrooms, size, location, property_type="", description=""):
    """Simulate AI property valuation with advanced algorithm"""
    base_price = 250000
    price_per_bedroom = 75000
    price_per_bathroom = 35000
    price_per_sqm = 3500
    
    # Location multiplier
    location_multipliers = {
        'Dublin 2': 1.5, 'Dublin 4': 1.4, 'Dublin 6': 1.35,
        'Dublin 1': 1.2, 'Dublin 8': 1.25, 'Dublin 3': 1.15
    }
    
    # Property type multiplier
    type_multipliers = {
        'Detached': 1.2, 'Semi-Detached': 1.0, 'Terraced': 0.95, 'Apartment': 0.9
    }
    
    location_mult = 1.0
    for area, mult in location_multipliers.items():
        if area.lower() in location.lower():
            location_mult = mult
            break
    
    type_mult = type_multipliers.get(property_type, 1.0)
    
    valuation = (base_price + 
                 (bedrooms * price_per_bedroom) + 
                 (bathrooms * price_per_bathroom) + 
                 (size * price_per_sqm)) * location_mult * type_mult
    
    # Market conditions adjustment
    valuation *= np.random.uniform(0.95, 1.05)
    
    return int(valuation)

def format_currency(amount):
    return f"€{amount:,.0f}"

def load_image(url):
    """Load image from URL"""
    try:
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        return img
    except:
        return None

# Sidebar Navigation
with st.sidebar:
    st.markdown("""
    <div class='sidebar-header'>
        RealEstate<br>Ireland.ie
    </div>
    <div class='sub-logo-text'>Premium Property Sales Platform</div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    
    if st.session_state.logged_in:
        st.markdown(f"**Welcome**  \n{st.session_state.user['name']}")
        st.markdown(f"*{st.session_state.user_type.title()} Account*")
        
        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
        
        if st.button("Sign Out", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.user = None
            st.session_state.user_type = None
            st.rerun()
    
    # Navigation menu
    if st.session_state.logged_in:
        if st.session_state.user_type == 'seller':
            page = st.radio("Navigation", 
                           ["Dashboard", "List Property", "My Portfolio", "Analytics", "Legal Centre"])
        else:
            page = st.radio("Navigation", 
                           ["Property Search", "My Offers", "Saved Properties", "Account"])
    else:
        page = st.radio("Navigation", 
                       ["Home", "How It Works", "Properties", "Sign In", "Contact"])

# Main Content Area
if not st.session_state.logged_in:
    if page == "Home":
        # Hero Section
        st.markdown("<h1 class='main-header'>The Future of Property Sales in Ireland</h1>", 
                   unsafe_allow_html=True)
        
        st.markdown("""
        <p style='text-align: center; font-size: 1.3rem; color: #64748b; margin-bottom: 3rem;'>
        Experience premium service at a fraction of traditional costs
        </p>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("""
            <div class='stat-card'>
                <div class='stat-value'>€12,000+</div>
                <p style='margin: 0; color: #64748b;'>Average Savings per Sale</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class='stat-card'>
                <div class='stat-value'>100%</div>
                <p style='margin: 0; color: #64748b;'>Transparent Process</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class='stat-card'>
                <div class='stat-value'>€1,500</div>
                <p style='margin: 0; color: #64748b;'>Fixed Fee</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
        
        # Value Proposition
        st.markdown("""
        <div class='value-prop'>
            <h2 style='font-family: "Playfair Display", serif; font-size: 2.5rem; margin-bottom: 1rem;'>
            Revolutionary Flat-Fee Model
            </h2>
            <p style='font-size: 1.2rem; line-height: 1.8; max-width: 800px; margin: 0 auto;'>
            Traditional estate agents charge 1-2% commission plus VAT. On a €800,000 property, 
            that's over €16,000 in fees. We charge just €1,500 — all inclusive.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Features
        st.markdown("<h2 class='section-header'>Premium Features</h2>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class='feature-card'>
                <h3 style='color: #1a2332; margin-bottom: 1rem;'>For Sellers</h3>
                <ul style='list-style: none; padding: 0;'>
                    <li style='margin-bottom: 0.8rem;'>
                        <strong>AI Valuation Engine</strong><br>
                        <span style='color: #64748b;'>Instant property valuation using advanced algorithms</span>
                    </li>
                    <li style='margin-bottom: 0.8rem;'>
                        <strong>Professional Photography</strong><br>
                        <span style='color: #64748b;'>Showcase your property in its best light</span>
                    </li>
                    <li style='margin-bottom: 0.8rem;'>
                        <strong>Legal Partnership</strong><br>
                        <span style='color: #64748b;'>McCarthy & Associates handle all documentation</span>
                    </li>
                    <li style='margin-bottom: 0.8rem;'>
                        <strong>Real-time Analytics</strong><br>
                        <span style='color: #64748b;'>Track views, offers, and market trends</span>
                    </li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class='feature-card'>
                <h3 style='color: #1a2332; margin-bottom: 1rem;'>For Buyers</h3>
                <ul style='list-style: none; padding: 0;'>
                    <li style='margin-bottom: 0.8rem;'>
                        <strong>Binding Agreements</strong><br>
                        <span style='color: #64748b;'>Secure your dream home with legal protection</span>
                    </li>
                    <li style='margin-bottom: 0.8rem;'>
                        <strong>Transparent Bidding</strong><br>
                        <span style='color: #64748b;'>See all offers in real-time</span>
                    </li>
                    <li style='margin-bottom: 0.8rem;'>
                        <strong>Escrow Protection</strong><br>
                        <span style='color: #64748b;'>Deposits held securely until completion</span>
                    </li>
                    <li style='margin-bottom: 0.8rem;'>
                        <strong>Digital Timeline</strong><br>
                        <span style='color: #64748b;'>Track every step of your purchase</span>
                    </li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        # Call to Action
        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            st.markdown("""
            <div style='text-align: center;'>
                <a href='#' class='premium-button' style='font-size: 1.1rem; padding: 1rem 3rem;'>
                    Start Your Journey Today
                </a>
            </div>
            """, unsafe_allow_html=True)
    
    elif page == "How It Works":
        st.markdown("<h1 class='main-header'>How It Works</h1>", unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["Sellers", "Buyers"])
        
        with tab1:
            st.markdown("<h2 class='section-header'>Four Simple Steps</h2>", unsafe_allow_html=True)
            
            steps = [
                ("1", "Register & Verify", "Complete identity verification and property ownership confirmation"),
                ("2", "List Your Property", "Upload professional photos and receive instant AI valuation"),
                ("3", "Review Offers", "Transparent bidding process with real-time notifications"),
                ("4", "Complete Sale", "Our legal partners handle all documentation and transfer")
            ]
            
            for step_num, title, desc in steps:
                st.markdown(f"""
                <div class='stat-card' style='margin-bottom: 1.5rem;'>
                    <div style='display: flex; align-items: center; gap: 2rem;'>
                        <div style='font-size: 3rem; font-weight: 700; color: #667eea; width: 80px;'>
                            {step_num}
                        </div>
                        <div style='flex: 1; text-align: left;'>
                            <h3 style='margin: 0 0 0.5rem 0; color: #1a2332;'>{title}</h3>
                            <p style='margin: 0; color: #64748b;'>{desc}</p>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
            
            # Cost Comparison
            st.markdown("<h2 class='section-header'>Cost Comparison</h2>", unsafe_allow_html=True)
            
            property_values = [400000, 600000, 800000, 1000000, 1500000]
            traditional_fees = [val * 0.015 * 1.23 for val in property_values]
            our_fees = [1500] * len(property_values)
            
            fig = go.Figure()
            fig.add_trace(go.Bar(
                name='Traditional Agent Fees',
                x=[f'€{val:,.0f}' for val in property_values],
                y=traditional_fees,
                marker_color='#ef4444',
                text=[f'€{fee:,.0f}' for fee in traditional_fees],
                textposition='outside'
            ))
            fig.add_trace(go.Bar(
                name='RealEstateIreland.ie',
                x=[f'€{val:,.0f}' for val in property_values],
                y=our_fees,
                marker_color='#10b981',
                text=['€1,500'] * len(property_values),
                textposition='outside'
            ))
            fig.update_layout(
                title={
                    'text': 'Fee Comparison by Property Value',
                    'font': {'family': 'Playfair Display', 'size': 24}
                },
                xaxis_title='Property Value',
                yaxis_title='Total Fees (€)',
                barmode='group',
                height=500,
                font={'family': 'Inter'},
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            st.markdown("<h2 class='section-header'>Secure Buying Process</h2>", unsafe_allow_html=True)
            
            buyer_steps = [
                ("Search & Discover", "Browse verified properties with transparent pricing and AI valuations"),
                ("Make an Offer", "Submit legally binding offers with 10% deposit through secure escrow"),
                ("Track Progress", "Monitor every step through our digital timeline system"),
                ("Complete Purchase", "Our legal partners ensure smooth transfer and registration")
            ]
            
            for i, (title, desc) in enumerate(buyer_steps, 1):
                st.markdown(f"""
                <div class='feature-card' style='margin-bottom: 1.5rem;'>
                    <h3 style='color: #1a2332;'>{i}. {title}</h3>
                    <p style='color: #64748b; margin: 0;'>{desc}</p>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
            
            st.markdown("""
            <div class='stat-card'>
                <h3 style='color: #1a2332; margin-bottom: 1rem;'>Buyer Protection Guarantee</h3>
                <ul style='list-style: none; padding: 0;'>
                    <li style='margin-bottom: 0.5rem; color: #64748b;'>
                        • All deposits held in secure escrow accounts
                    </li>
                    <li style='margin-bottom: 0.5rem; color: #64748b;'>
                        • Verified seller identities and property ownership
                    </li>
                    <li style='margin-bottom: 0.5rem; color: #64748b;'>
                        • Legally binding purchase agreements
                    </li>
                    <li style='margin-bottom: 0.5rem; color: #64748b;'>
                        • Full transparency on all competing offers
                    </li>
                    <li style='margin-bottom: 0.5rem; color: #64748b;'>
                        • Professional legal support throughout
                    </li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
    
    elif page == "Properties":
        st.markdown("<h1 class='main-header'>Premium Properties</h1>", unsafe_allow_html=True)
        
        # Filters
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            min_price = st.number_input("Minimum Price (€)", min_value=0, max_value=5000000, 
                                       value=0, step=100000, format="%d")
        with col2:
            max_price = st.number_input("Maximum Price (€)", min_value=0, max_value=5000000, 
                                       value=3000000, step=100000, format="%d")
        with col3:
            bedrooms = st.selectbox("Bedrooms", ["Any", "2+", "3+", "4+", "5+"])
        with col4:
            sort_by = st.selectbox("Sort By", ["Newest First", "Price: Low to High", "Price: High to Low"])
        
        # Display properties
        filtered_properties = st.session_state.properties.copy()
        
        # Apply filters
        filtered_properties = [p for p in filtered_properties 
                             if p['price'] >= min_price and p['price'] <= max_price]
        
        if bedrooms != "Any":
            min_beds = int(bedrooms[0])
            filtered_properties = [p for p in filtered_properties if p['bedrooms'] >= min_beds]
        
        # Sort
        if sort_by == "Price: Low to High":
            filtered_properties.sort(key=lambda x: x['price'])
        elif sort_by == "Price: High to Low":
            filtered_properties.sort(key=lambda x: x['price'], reverse=True)
        else:
            filtered_properties.sort(key=lambda x: x['listed_date'], reverse=True)
        
        st.markdown(f"<p style='color: #64748b; margin-bottom: 2rem;'>Showing {len(filtered_properties)} properties</p>", 
                   unsafe_allow_html=True)
        
        # Display properties
        for prop in filtered_properties:
            with st.container():
                col1, col2 = st.columns([1.5, 2])
                
                with col1:
                    if prop['images']:
                        st.image(prop['images'][0], use_column_width=True)
                
                with col2:
                    st.markdown(f"<h3 style='margin: 0;'>{prop['title']}</h3>", unsafe_allow_html=True)
                    st.markdown(f"<p style='color: #64748b; margin: 0.5rem 0;'>{prop['address']}</p>", 
                               unsafe_allow_html=True)
                    
                    st.markdown(f"<div class='price-tag'>{format_currency(prop['price'])}</div>", 
                               unsafe_allow_html=True)
                    
                    st.markdown(f"""
                    <div class='property-meta'>
                        <span>{prop['bedrooms']} Bedrooms</span>
                        <span>•</span>
                        <span>{prop['bathrooms']} Bathrooms</span>
                        <span>•</span>
                        <span>{prop['size']}m²</span>
                        <span>•</span>
                        <span>{prop['property_type']}</span>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.markdown(f"<small style='color: #64748b;'>Views: {prop['views']}</small>", 
                                   unsafe_allow_html=True)
                        if prop['bids']:
                            st.markdown(f"<div class='bid-status'>{len(prop['bids'])} Active Bids</div>", 
                                       unsafe_allow_html=True)
                    with col_b:
                        st.markdown(f"<small style='color: #64748b;'>AI Valuation: {format_currency(prop['ai_valuation'])}</small>", 
                                   unsafe_allow_html=True)
                    
                    if st.button("View Details", key=f"view_{prop['id']}", use_container_width=True):
                        st.info("Please sign in to view full details and make offers")
                
                st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    
    elif page == "Sign In":
        st.markdown("<h1 class='main-header'>Sign In</h1>", unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["Sign In", "Create Account"])
        
        with tab1:
            col1, col2, col3 = st.columns([1,2,1])
            with col2:
                with st.form("login_form"):
                    st.markdown("<h3 style='text-align: center; margin-bottom: 2rem;'>Welcome Back</h3>", 
                               unsafe_allow_html=True)
                    
                    username = st.text_input("Username")
                    password = st.text_input("Password", type="password")
                    
                    submitted = st.form_submit_button("Sign In", use_container_width=True)
                    
                    if submitted:
                        success, user = authenticate_user(username, password)
                        if success:
                            st.session_state.logged_in = True
                            st.session_state.user = user
                            st.session_state.user_type = user['type']
                            st.success("Welcome back!")
                            st.rerun()
                        else:
                            st.error("Invalid credentials")
                
                st.info("Demo accounts: seller1/pass123, buyer1/pass123")
        
        with tab2:
            col1, col2, col3 = st.columns([1,2,1])
            with col2:
                with st.form("register_form"):
                    st.markdown("<h3 style='text-align: center; margin-bottom: 2rem;'>Join RealEstateIreland.ie</h3>", 
                               unsafe_allow_html=True)
                    
                    account_type = st.radio("I am a", ["Property Seller", "Property Buyer"])
                    st.markdown("<div style='margin-bottom: 1rem;'></div>", unsafe_allow_html=True)
                    
                    new_username = st.text_input("Choose Username")
                    new_email = st.text_input("Email Address")
                    new_name = st.text_input("Full Name")
                    new_password = st.text_input("Create Password", type="password")
                    confirm_password = st.text_input("Confirm Password", type="password")
                    
                    terms = st.checkbox("I agree to the Terms of Service and Privacy Policy")
                    
                    submitted = st.form_submit_button("Create Account", use_container_width=True)
                    
                    if submitted:
                        if new_username in st.session_state.users:
                            st.error("Username already exists")
                        elif new_password != confirm_password:
                            st.error("Passwords do not match")
                        elif not terms:
                            st.error("Please accept the terms and conditions")
                        elif not all([new_username, new_email, new_name, new_password]):
                            st.error("Please complete all fields")
                        else:
                            user_type = 'seller' if account_type == "Property Seller" else 'buyer'
                            st.session_state.users[new_username] = {
                                'password': hash_password(new_password),
                                'type': user_type,
                                'name': new_name,
                                'email': new_email,
                                'verified': False
                            }
                            st.success("Account created successfully! Please sign in.")
                            st.balloons()
    
    elif page == "Contact":
        st.markdown("<h1 class='main-header'>Contact Us</h1>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class='feature-card'>
                <h3 style='color: #1a2332;'>Head Office</h3>
                <p style='color: #64748b; line-height: 1.8;'>
                    RealEstateIreland.ie<br>
                    42 Fitzwilliam Square<br>
                    Dublin 2, D02 R283<br>
                    Ireland
                </p>
                
                <p style='color: #64748b; margin-top: 1.5rem;'>
                    <strong>General Inquiries</strong><br>
                    +353 1 234 5678<br>
                    info@realestateireland.ie
                </p>
                
                <p style='color: #64748b; margin-top: 1.5rem;'>
                    <strong>Office Hours</strong><br>
                    Monday - Friday: 9:00 - 18:00<br>
                    Saturday: 10:00 - 16:00<br>
                    Sunday: Closed
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("<h3>Send us a Message</h3>", unsafe_allow_html=True)
            
            with st.form("contact_form"):
                contact_name = st.text_input("Your Name")
                contact_email = st.text_input("Your Email")
                contact_phone = st.text_input("Phone Number (Optional)")
                contact_subject = st.selectbox("Subject", 
                                             ["General Inquiry", "Selling Property", 
                                              "Buying Property", "Partnership Opportunities", 
                                              "Technical Support"])
                contact_message = st.text_area("Message", height=150)
                
                submitted = st.form_submit_button("Send Message", use_container_width=True)
                
                if submitted:
                    if all([contact_name, contact_email, contact_message]):
                        st.success("Thank you for your message. We'll respond within 24 hours.")
                    else:
                        st.error("Please complete all required fields")

else:  # User is logged in
    if st.session_state.user_type == 'seller':
        if page == "Dashboard":
            st.markdown(f"<h1 class='main-header'>Welcome back, {st.session_state.user['name']}</h1>", 
                       unsafe_allow_html=True)
            
            # Get seller's properties
            seller_properties = [p for p in st.session_state.properties 
                               if p.get('seller_id') == st.session_state.logged_in]
            
            # Dashboard metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                total_value = sum(p['price'] for p in seller_properties)
                st.markdown(f"""
                <div class='stat-card'>
                    <div class='stat-value'>{format_currency(total_value)}</div>
                    <p style='margin: 0; color: #64748b;'>Portfolio Value</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                total_views = sum(p['views'] for p in seller_properties)
                st.markdown(f"""
                <div class='stat-card'>
                    <div class='stat-value'>{total_views:,}</div>
                    <p style='margin: 0; color: #64748b;'>Total Views</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                total_bids = sum(len(p['bids']) for p in seller_properties)
                st.markdown(f"""
                <div class='stat-card'>
                    <div class='stat-value'>{total_bids}</div>
                    <p style='margin: 0; color: #64748b;'>Active Bids</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                active_listings = len([p for p in seller_properties if p['status'] == 'active'])
                st.markdown(f"""
                <div class='stat-card'>
                    <div class='stat-value'>{active_listings}</div>
                    <p style='margin: 0; color: #64748b;'>Active Listings</p>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
            
            # Recent Activity
            st.markdown("<h2 class='section-header'>Recent Activity</h2>", unsafe_allow_html=True)
            
            if seller_properties:
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
                        st.markdown(f"""
                        <div class='metric-container'>
                            <strong>New offer on {bid['property']}</strong><br>
                            <span style='color: #64748b;'>
                            {format_currency(bid['amount'])} from {bid['bidder']} • 
                            {bid['date'].strftime('%d %B %Y')}
                            </span>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.info("No recent activity")
            else:
                st.info("List your first property to start receiving offers")
        
        elif page == "List Property":
            st.markdown("<h1 class='main-header'>List Your Property</h1>", unsafe_allow_html=True)
            
            with st.form("property_listing"):
                st.markdown("<h3>Property Information</h3>", unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    title = st.text_input("Property Title", 
                                        placeholder="e.g., Elegant Victorian Townhouse")
                    address = st.text_input("Full Address", 
                                          placeholder="e.g., 15 Merrion Square, Dublin 2")
                    property_type = st.selectbox("Property Type", 
                                               ["Detached", "Semi-Detached", "Terraced", 
                                                "Apartment", "Penthouse", "Duplex"])
                    bedrooms = st.number_input("Bedrooms", min_value=1, max_value=10, value=3)
                
                with col2:
                    price = st.number_input("Asking Price (€)", min_value=100000, max_value=10000000, 
                                          value=750000, step=25000, format="%d")
                    size = st.number_input("Size (m²)", min_value=20, max_value=1000, value=150)
                    bathrooms = st.number_input("Bathrooms", min_value=1, max_value=8, value=2)
                    ber_rating = st.selectbox("BER Rating", 
                                            ["A1", "A2", "A3", "B1", "B2", "B3", 
                                             "C1", "C2", "C3", "D1", "D2", "E1", "E2", "F", "G"])
                
                description = st.text_area("Property Description", 
                                         placeholder="Describe the unique features and selling points of your property...", 
                                         height=150)
                
                st.markdown("<h3>Media</h3>", unsafe_allow_html=True)
                photos = st.file_uploader("Upload Property Photos", 
                                        type=['jpg', 'jpeg', 'png'], 
                                        accept_multiple_files=True,
                                        help="Professional photography service available")
                
                st.markdown("<h3>Valuation & Pricing</h3>", unsafe_allow_html=True)
                
                col1, col2 = st.columns([2,1])
                with col1:
                    if st.checkbox("Request AI Valuation"):
                        ai_val = calculate_ai_valuation(bedrooms, bathrooms, size, address, 
                                                       property_type, description)
                        st.success(f"AI Estimated Value: {format_currency(ai_val)}")
                        
                        # Valuation breakdown
                        st.markdown("""
                        <div class='metric-container'>
                            <p style='margin: 0; font-weight: 500;'>Valuation Analysis</p>
                            <small style='color: #64748b;'>
                            Based on location premium, property specifications, 
                            and current market conditions
                            </small>
                        </div>
                        """, unsafe_allow_html=True)
                
                st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
                
                st.markdown("""
                <div class='metric-container'>
                    <h4 style='margin-bottom: 0.5rem;'>Legal Documentation</h4>
                    <p style='color: #64748b; margin: 0;'>
                    McCarthy & Associates will handle all legal aspects<br>
                    Additional fee: €850 (payable at completion)
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
                terms = st.checkbox("I confirm I am the legal owner and have the right to sell this property")
                marketing = st.checkbox("I agree to the marketing terms and flat fee of €1,500")
                
                submitted = st.form_submit_button("List Property", type="primary", use_container_width=True)
                
                if submitted:
                    if not all([title, address, description, terms, marketing]):
                        st.error("Please complete all required fields and confirmations")
                    else:
                        new_property = {
                            'id': len(st.session_state.properties) + 1,
                            'title': title,
                            'address': address,
                            'price': price,
                            'bedrooms': bedrooms,
                            'bathrooms': bathrooms,
                            'size': size,
                            'property_type': property_type,
                            'ber_rating': ber_rating,
                            'seller_id': st.session_state.logged_in,
                            'description': description,
                            'images': [property_images[len(st.session_state.properties) % len(property_images)]],
                            'listed_date': datetime.now(),
                            'status': 'active',
                            'bids': [],
                            'views': 0,
                            'ai_valuation': ai_val if 'ai_val' in locals() else int(price * 1.02)
                        }
                        st.session_state.properties.append(new_property)
                        st.success("Property listed successfully! Invoice for €1,500 will be sent to your email.")
                        st.balloons()
        
        elif page == "My Portfolio":
            st.markdown("<h1 class='main-header'>Property Portfolio</h1>", unsafe_allow_html=True)
            
            seller_properties = [p for p in st.session_state.properties 
                               if p.get('seller_id') == st.session_state.logged_in]
            
            if not seller_properties:
                st.info("Your portfolio is empty. List your first property to get started.")
            else:
                for prop in seller_properties:
                    with st.expander(f"{prop['title']} | {format_currency(prop['price'])}", 
                                   expanded=True):
                        col1, col2 = st.columns([1.5, 2])
                        
                        with col1:
                            if prop['images']:
                                st.image(prop['images'][0], use_column_width=True)
                        
                        with col2:
                            st.markdown(f"**Address:** {prop['address']}")
                            st.markdown(f"**Type:** {prop['property_type']} | **BER:** {prop['ber_rating']}")
                            st.markdown(f"**Specifications:** {prop['bedrooms']} bed, "
                                      f"{prop['bathrooms']} bath, {prop['size']}m²")
                            st.markdown(f"**Listed:** {prop['listed_date'].strftime('%d %B %Y')}")
                            st.markdown(f"**Status:** {prop['status'].title()}")
                            
                            col_a, col_b, col_c = st.columns(3)
                            with col_a:
                                st.metric("Views", prop['views'])
                            with col_b:
                                st.metric("Offers", len(prop['bids']))
                            with col_c:
                                if prop['bids']:
                                    highest = max([b['amount'] for b in prop['bids']])
                                    st.metric("Highest Offer", format_currency(highest))
                                else:
                                    st.metric("Highest Offer", "—")
                        
                        if prop['bids']:
                            st.markdown("<h4>Recent Offers</h4>", unsafe_allow_html=True)
                            offers_data = []
                            for bid in sorted(prop['bids'], key=lambda x: x['amount'], reverse=True):
                                offers_data.append({
                                    'Bidder': bid['bidder'],
                                    'Offer': format_currency(bid['amount']),
                                    'Date': bid['date'].strftime('%d %b %Y'),
                                    'Status': 'Leading' if bid['amount'] == max([b['amount'] for b in prop['bids']]) else 'Active'
                                })
                            
                            df = pd.DataFrame(offers_data)
                            st.dataframe(df, use_container_width=True, hide_index=True)
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            if st.button("Edit Listing", key=f"edit_{prop['id']}", use_container_width=True):
                                st.info("Edit functionality coming soon")
                        with col2:
                            if prop['bids'] and st.button("Accept Offer", key=f"accept_{prop['id']}", 
                                                         use_container_width=True, type="primary"):
                                st.success("Legal documents are being prepared")
                        with col3:
                            if st.button("Delist Property", key=f"delist_{prop['id']}", 
                                       use_container_width=True):
                                prop['status'] = 'delisted'
                                st.rerun()
        
        elif page == "Analytics":
            st.markdown("<h1 class='main-header'>Performance Analytics</h1>", unsafe_allow_html=True)
            
            seller_properties = [p for p in st.session_state.properties 
                               if p.get('seller_id') == st.session_state.logged_in]
            
            if not seller_properties:
                st.info("List properties to access analytics")
            else:
                # Performance Overview
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    avg_views = int(np.mean([p['views'] for p in seller_properties]))
                    st.metric("Average Views", f"{avg_views:,}")
                
                with col2:
                    avg_bids = np.mean([len(p['bids']) for p in seller_properties])
                    st.metric("Average Offers", f"{avg_bids:.1f}")
                
                with col3:
                    properties_with_bids = len([p for p in seller_properties if p['bids']])
                    conversion = (properties_with_bids / len(seller_properties) * 100) if seller_properties else 0
                    st.metric("Offer Rate", f"{conversion:.0f}%")
                
                with col4:
                    all_bid_amounts = []
                    for p in seller_properties:
                        all_bid_amounts.extend([b['amount'] for b in p['bids']])
                    avg_bid_value = np.mean(all_bid_amounts) if all_bid_amounts else 0
                    st.metric("Average Offer Value", format_currency(avg_bid_value))
                
                st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
                
                # Engagement Timeline
                st.markdown("<h2 class='section-header'>Engagement Timeline</h2>", unsafe_allow_html=True)
                
                dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
                views_data = np.random.poisson(15, size=30).cumsum()
                
                fig = px.area(x=dates, y=views_data, 
                            labels={'x': 'Date', 'y': 'Cumulative Views'},
                            line_shape='spline')
                fig.update_traces(fill='tozeroy', fillcolor='rgba(102, 126, 234, 0.2)',
                                line=dict(color='#667eea', width=3))
                fig.update_layout(
                    showlegend=False,
                    height=400,
                    font={'family': 'Inter'},
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)'
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # Property Performance
                if len(seller_properties) > 1:
                    st.markdown("<h2 class='section-header'>Property Comparison</h2>", unsafe_allow_html=True)
                    
                    comparison_data = []
                    for p in seller_properties:
                        comparison_data.append({
                            'Property': p['title'][:30] + '...' if len(p['title']) > 30 else p['title'],
                            'Views': p['views'],
                            'Offers': len(p['bids']),
                            'Days Listed': (datetime.now() - p['listed_date']).days
                        })
                    
                    df = pd.DataFrame(comparison_data)
                    
                    fig = go.Figure()
                    fig.add_trace(go.Bar(name='Views', x=df['Property'], y=df['Views'],
                                       marker_color='#667eea'))
                    fig.add_trace(go.Bar(name='Offers', x=df['Property'], y=df['Offers'],
                                       marker_color='#10b981'))
                    fig.update_layout(
                        barmode='group',
                        height=400,
                        font={'family': 'Inter'},
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)'
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                # Market Insights
                st.markdown("<h2 class='section-header'>Market Insights</h2>", unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("""
                    <div class='feature-card'>
                        <h4 style='color: #1a2332;'>Performance Highlights</h4>
                        <ul style='list-style: none; padding: 0; color: #64748b;'>
                            <li style='margin-bottom: 0.5rem;'>
                                Properties in Dublin 2 receiving 23% more views
                            </li>
                            <li style='margin-bottom: 0.5rem;'>
                                4-bedroom properties have highest demand
                            </li>
                            <li style='margin-bottom: 0.5rem;'>
                                Weekend listings get 35% more initial views
                            </li>
                        </ul>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown("""
                    <div class='feature-card'>
                        <h4 style='color: #1a2332;'>Optimization Tips</h4>
                        <ul style='list-style: none; padding: 0; color: #64748b;'>
                            <li style='margin-bottom: 0.5rem;'>
                                Properties with 15+ photos receive 2.3x more offers
                            </li>
                            <li style='margin-bottom: 0.5rem;'>
                                AI valuation within 5% of asking price sells faster
                            </li>
                            <li style='margin-bottom: 0.5rem;'>
                                Detailed descriptions increase engagement by 40%
                            </li>
                        </ul>
                    </div>
                    """, unsafe_allow_html=True)
        
        elif page == "Legal Centre":
            st.markdown("<h1 class='main-header'>Legal Centre</h1>", unsafe_allow_html=True)
            
            st.markdown("""
            <div class='feature-card'>
                <h2 style='font-family: "Playfair Display", serif;'>McCarthy & Associates Partnership</h2>
                <p style='color: #64748b; line-height: 1.8;'>
                Our exclusive legal partnership ensures every transaction is handled with the highest 
                professional standards. McCarthy & Associates brings over 50 years of property law expertise 
                to every sale.
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<h2 class='section-header'>Services Included</h2>", unsafe_allow_html=True)
            
            services = [
                ("Title Investigation", "Comprehensive verification of property ownership and boundaries"),
                ("Contract Preparation", "Drafting of legally binding sale agreements"),
                ("Escrow Management", "Secure handling of deposits and purchase funds"),
                ("Due Diligence", "Complete property searches and compliance checks"),
                ("Transfer Documentation", "Preparation and filing of all transfer documents"),
                ("Registration", "Property Registration Authority submissions")
            ]
            
            for service, desc in services:
                st.markdown(f"""
                <div class='metric-container'>
                    <strong>{service}</strong><br>
                    <span style='color: #64748b;'>{desc}</span>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
            
            # Sale Progress Tracker
            st.markdown("<h2 class='section-header'>Sale Progress Tracker</h2>", unsafe_allow_html=True)
            
            stages = [
                ("Property Listed", 100, True),
                ("Offer Accepted", 80, True),
                ("Contracts Issued", 60, True),
                ("Surveys Complete", 40, False),
                ("Final Contracts", 20, False),
                ("Sale Closed", 0, False)
            ]
            
            for stage, _, completed in stages:
                col1, col2 = st.columns([4,1])
                with col1:
                    if completed:
                        st.progress(1.0)
                    else:
                        st.progress(0.0)
                with col2:
                    if completed:
                        st.markdown(f"**{stage}** [Completed]")
                    else:
                        st.markdown(f"{stage}")
            
            st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
            
            # Document Centre
            st.markdown("<h2 class='section-header'>Document Centre</h2>", unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.button("Sale Agreement Template", use_container_width=True)
                st.button("Property Disclosure Form", use_container_width=True)
            with col2:
                st.button("Title Documents Guide", use_container_width=True)
                st.button("Tax Clearance Forms", use_container_width=True)
            with col3:
                st.button("Completion Checklist", use_container_width=True)
                st.button("FAQ Document", use_container_width=True)
    
    else:  # Buyer Interface
        if page == "Property Search":
            st.markdown("<h1 class='main-header'>Discover Your Dream Home</h1>", unsafe_allow_html=True)
            
            # Advanced Search
            with st.expander("Advanced Search", expanded=True):
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    min_price = st.number_input("Min Price (€)", 0, 5000000, 0, 100000, format="%d")
                with col2:
                    max_price = st.number_input("Max Price (€)", 0, 5000000, 2000000, 100000, format="%d")
                with col3:
                    min_beds = st.selectbox("Min Bedrooms", [1, 2, 3, 4, 5])
                with col4:
                    property_type = st.selectbox("Property Type", 
                                               ["All", "Detached", "Semi-Detached", 
                                                "Terraced", "Apartment", "Penthouse"])
            
            # Property Listings
            active_properties = [p for p in st.session_state.properties 
                               if p['status'] == 'active' and 
                               p['price'] >= min_price and 
                               p['price'] <= max_price and
                               p['bedrooms'] >= min_beds]
            
            if property_type != "All":
                active_properties = [p for p in active_properties if p['property_type'] == property_type]
            
            st.markdown(f"<p style='color: #64748b;'>{len(active_properties)} properties match your criteria</p>", 
                       unsafe_allow_html=True)
            
            for prop in active_properties:
                with st.container():
                    col1, col2 = st.columns([1.5, 2])
                    
                    with col1:
                        if prop['images']:
                            st.image(prop['images'][0], use_column_width=True)
                    
                    with col2:
                        st.markdown(f"<h3 style='margin: 0;'>{prop['title']}</h3>", 
                                   unsafe_allow_html=True)
                        st.markdown(f"<p style='color: #64748b;'>{prop['address']}</p>", 
                                   unsafe_allow_html=True)
                        
                        st.markdown(f"<div class='price-tag'>{format_currency(prop['price'])}</div>", 
                                   unsafe_allow_html=True)
                        
                        st.markdown(f"""
                        <div class='property-meta'>
                            <span>{prop['bedrooms']} bed</span>
                            <span>•</span>
                            <span>{prop['bathrooms']} bath</span>
                            <span>•</span>
                            <span>{prop['size']}m²</span>
                            <span>•</span>
                            <span>{prop['property_type']}</span>
                            <span>•</span>
                            <span>BER {prop['ber_rating']}</span>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Property highlights
                        col_a, col_b = st.columns(2)
                        with col_a:
                            st.markdown(f"<small>AI Valuation: <strong>{format_currency(prop['ai_valuation'])}</strong></small>", 
                                       unsafe_allow_html=True)
                            if prop['bids']:
                                highest_bid = max([b['amount'] for b in prop['bids']])
                                st.markdown(f"<small>Highest Offer: <strong>{format_currency(highest_bid)}</strong></small>", 
                                           unsafe_allow_html=True)
                        
                        with col_b:
                            st.markdown(f"<small>{prop['views']} views</small>", unsafe_allow_html=True)
                            if prop['bids']:
                                st.markdown(f"<div class='bid-status'>{len(prop['bids'])} Active Offers</div>", 
                                           unsafe_allow_html=True)
                        
                        # Increment views
                        prop['views'] += 1
                
                with st.expander("View Details & Make Offer"):
                    st.markdown(f"**Description:** {prop['description']}")
                    st.markdown(f"**Listed:** {prop['listed_date'].strftime('%d %B %Y')}")
                    
                    # Bidding Section
                    st.markdown("<h4>Make an Offer</h4>", unsafe_allow_html=True)
                    
                    col1, col2 = st.columns([2,1])
                    with col1:
                        bid_amount = st.number_input(
                            "Your Offer (€)", 
                            min_value=int(prop['price'] * 0.9),
                            max_value=int(prop['price'] * 1.5),
                            value=prop['price'],
                            step=5000,
                            key=f"bid_{prop['id']}",
                            format="%d"
                        )
                        
                        deposit = bid_amount * 0.1
                        st.markdown(f"<small>10% deposit required: <strong>{format_currency(deposit)}</strong></small>", 
                                   unsafe_allow_html=True)
                    
                    with col2:
                        st.markdown("<div style='padding-top: 29px;'></div>", unsafe_allow_html=True)
                        if st.button("Submit Offer", key=f"submit_{prop['id']}", 
                                   type="primary", use_container_width=True):
                            prop['bids'].append({
                                'bidder': st.session_state.user['name'],
                                'amount': bid_amount,
                                'date': datetime.now()
                            })
                            st.success(f"Offer submitted! Deposit of {format_currency(deposit)} will be requested.")
                            st.rerun()
                    
                    # Offer History
                    if prop['bids']:
                        st.markdown("<h4>Offer History</h4>", unsafe_allow_html=True)
                        for bid in sorted(prop['bids'], key=lambda x: x['amount'], reverse=True)[:3]:
                            if bid['bidder'] == st.session_state.user['name']:
                                st.markdown(f"**Your offer:** {format_currency(bid['amount'])} - {bid['date'].strftime('%d %b')}")
                            else:
                                st.markdown(f"Competing offer: {format_currency(bid['amount'])} - {bid['date'].strftime('%d %b')}")
                
                st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
        
        elif page == "My Offers":
            st.markdown("<h1 class='main-header'>My Offers</h1>", unsafe_allow_html=True)
            
            # Find all offers by current user
            my_offers = []
            for prop in st.session_state.properties:
                for bid in prop['bids']:
                    if bid['bidder'] == st.session_state.user['name']:
                        highest_bid = max([b['amount'] for b in prop['bids']])
                        my_offers.append({
                            'property': prop,
                            'bid': bid,
                            'is_winning': bid['amount'] == highest_bid,
                            'highest_bid': highest_bid
                        })
            
            if my_offers:
                winning = [o for o in my_offers if o['is_winning']]
                losing = [o for o in my_offers if not o['is_winning']]
                
                if winning:
                    st.markdown("<h2 class='section-header'>Winning Offers</h2>", unsafe_allow_html=True)
                    for offer in winning:
                        prop = offer['property']
                        with st.container():
                            col1, col2 = st.columns([1, 3])
                            with col1:
                                if prop['images']:
                                    st.image(prop['images'][0], use_column_width=True)
                            with col2:
                                st.markdown(f"<h4>{prop['title']}</h4>", unsafe_allow_html=True)
                                st.markdown(f"{prop['address']}")
                                st.markdown(f"**Your Offer:** {format_currency(offer['bid']['amount'])}")
                                st.markdown(f"**Status:** Leading Offer")
                                
                                deposit = offer['bid']['amount'] * 0.1
                                if st.button(f"Proceed to Deposit ({format_currency(deposit)})", 
                                           key=f"deposit_{prop['id']}", type="primary"):
                                    st.success("Deposit instructions sent to your email")
                            
                            st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
                
                if losing:
                    st.markdown("<h2 class='section-header'>Active Offers</h2>", unsafe_allow_html=True)
                    for offer in losing:
                        prop = offer['property']
                        with st.container():
                            col1, col2 = st.columns([1, 3])
                            with col1:
                                if prop['images']:
                                    st.image(prop['images'][0], use_column_width=True)
                            with col2:
                                st.markdown(f"<h4>{prop['title']}</h4>", unsafe_allow_html=True)
                                st.markdown(f"{prop['address']}")
                                st.markdown(f"**Your Offer:** {format_currency(offer['bid']['amount'])}")
                                st.markdown(f"**Leading Offer:** {format_currency(offer['highest_bid'])}")
                                st.markdown(f"**Status:** Outbid by {format_currency(offer['highest_bid'] - offer['bid']['amount'])}")
                                
                                if st.button(f"Increase Offer", key=f"increase_{prop['id']}"):
                                    st.info("Return to Property Search to submit a new offer")
                            
                            st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
            else:
                st.info("You haven't made any offers yet. Browse properties to get started.")
        
        elif page == "Saved Properties":
            st.markdown("<h1 class='main-header'>Saved Properties</h1>", unsafe_allow_html=True)
            st.info("Property watchlist feature coming soon")
        
        elif page == "Account":
            st.markdown("<h1 class='main-header'>Account Settings</h1>", unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                <div class='feature-card'>
                    <h3 style='color: #1a2332;'>Profile Information</h3>
                """, unsafe_allow_html=True)
                
                st.markdown(f"**Name:** {st.session_state.user['name']}")
                st.markdown(f"**Email:** {st.session_state.user['email']}")
                st.markdown(f"**Account Type:** {st.session_state.user_type.title()}")
                
                if st.session_state.user.get('verified'):
                    st.markdown("**Identity:** Verified")
                else:
                    st.markdown("**Identity:** Pending Verification")
                    if st.button("Verify Identity", type="primary"):
                        st.session_state.user['verified'] = True
                        st.success("Identity verified successfully")
                        st.rerun()
                
                if st.session_state.user_type == 'buyer':
                    if st.session_state.user.get('finance_verified'):
                        st.markdown("**Finance Status:** Pre-approved")
                    else:
                        st.markdown("**Finance Status:** Not Verified")
                        if st.button("Verify Finances", type="primary"):
                            st.session_state.user['finance_verified'] = True
                            st.success("Finance verification complete")
                            st.rerun()
                
                st.markdown("</div>", unsafe_allow_html=True)
            
            with col2:
                st.markdown("""
                <div class='feature-card'>
                    <h3 style='color: #1a2332;'>Preferences</h3>
                """, unsafe_allow_html=True)
                
                with st.form("preferences"):
                    notifications = st.checkbox("Email Notifications", value=True)
                    instant_alerts = st.checkbox("Instant Offer Alerts", value=True)
                    newsletter = st.checkbox("Market Updates Newsletter", value=False)
                    
                    st.markdown("<h4>Search Preferences</h4>", unsafe_allow_html=True)
                    
                    preferred_areas = st.multiselect(
                        "Preferred Areas",
                        ["Dublin 2", "Dublin 4", "Dublin 6", "Dublin 8", 
                         "Dun Laoghaire", "Blackrock", "Dalkey"]
                    )
                    
                    budget_range = st.slider(
                        "Budget Range (€)",
                        min_value=100000,
                        max_value=3000000,
                        value=(500000, 1500000),
                        step=50000,
                        format="€%d"
                    )
                    
                    if st.form_submit_button("Update Preferences", use_container_width=True):
                        st.success("Preferences updated successfully")
                
                st.markdown("</div>", unsafe_allow_html=True)

# Premium Footer
st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
st.markdown("""
<div style='text-align: center; color: #64748b; padding: 3rem 0;'>
    <p style='font-size: 1.1rem; margin-bottom: 1rem;'>
        <strong>RealEstateIreland.ie</strong> - The Premium Property Platform
    </p>
    <p style='margin-bottom: 0.5rem;'>
        Revolutionizing property sales with transparency, technology, and trust
    </p>
    <p style='font-size: 0.9rem;'>
        © 2025 RealEstateIreland.ie. All rights reserved. | Terms of Service | Privacy Policy
    </p>
</div>
""", unsafe_allow_html=True)
