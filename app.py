import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import io
import base64
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from streamlit_option_menu import option_menu
import folium
from streamlit_folium import folium_static
import json
import re
import random
from streamlit_extras.switch_page_button import switch_page
from streamlit_extras.colored_header import colored_header
from streamlit_extras.card import card
from streamlit_extras.stylable_container import stylable_container

# Set page configuration
st.set_page_config(
    page_title="RealEstateIreland.ie",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================
# UTILITY FUNCTIONS AND DATA GENERATORS
# =========================================

# Custom CSS for styling
def load_css():
    st.markdown("""
    <style>
        /* Main branding and typography */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }
        
        .main-header {
            font-size: 36px !important;
            font-weight: 700 !important;
            color: #2E7D67 !important;
            margin-bottom: 20px !important;
        }
        
        .sub-header {
            font-size: 24px !important;
            font-weight: 600 !important;
            margin-top: 25px !important;
            margin-bottom: 15px !important;
        }
        
        .section-header {
            font-size: 20px !important;
            font-weight: 600 !important;
            margin-top: 20px !important;
            margin-bottom: 10px !important;
        }
        
        .green-highlight {
            color: #2E7D67 !important;
            font-weight: 600 !important;
        }
        
        /* Component styling */
        .feature-box {
            background-color: #f8f9fa;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
            border-left: 4px solid #2E7D67;
            transition: transform 0.2s;
        }
        
        .feature-box:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 20px rgba(0,0,0,0.05);
        }
        
        .saving-box {
            background-color: #d4edda;
            border-radius: 10px;
            padding: 20px;
            margin: 20px 0;
            text-align: center;
        }
        
        .process-step {
            background-color: #f8f9fa;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
            border-left: 4px solid #2E7D67;
            position: relative;
        }
        
        .process-step-number {
            position: absolute;
            top: -15px;
            left: -15px;
            width: 30px;
            height: 30px;
            background-color: #2E7D67;
            color: white;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
        }
        
        .nav-link {
            text-decoration: none;
            color: #2E7D67;
            font-weight: 600;
            margin-right: 15px;
        }
        
        .nav-link:hover {
            text-decoration: underline;
        }
        
        .footer {
            text-align: center;
            margin-top: 50px;
            padding: 20px;
            background-color: #f8f9fa;
            border-radius: 10px;
        }
        
        .metric-value {
            font-size: 24px;
            font-weight: 700;
            color: #2E7D67;
        }
        
        .btn-primary {
            background-color: #2E7D67;
            color: white;
            padding: 10px 20px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            border-radius: 5px;
            font-weight: 600;
            margin: 10px 0;
            cursor: pointer;
        }
        
        .btn-secondary {
            background-color: #f8f9fa;
            color: #2E7D67;
            border: 1px solid #2E7D67;
            padding: 10px 20px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            border-radius: 5px;
            font-weight: 600;
            margin: 10px 0;
            cursor: pointer;
        }
        
        .btn-primary:hover, .btn-secondary:hover {
            opacity: 0.9;
        }
        
        /* Property card styling */
        .property-card {
            border: 1px solid #e0e0e0;
            border-radius: 10px;
            overflow: hidden;
            transition: transform 0.3s, box-shadow 0.3s;
            height: 100%;
        }
        
        .property-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 20px rgba(0,0,0,0.1);
        }
        
        .property-image {
            height: 200px;
            background-size: cover;
            background-position: center;
        }
        
        .property-details {
            padding: 15px;
        }
        
        .property-price {
            color: #2E7D67;
            font-weight: bold;
            font-size: 20px;
            margin: 5px 0;
        }
        
        .property-address {
            font-weight: 600;
            margin: 5px 0;
        }
        
        .property-features {
            color: #666;
            margin: 5px 0;
        }
        
        .property-description {
            margin: 10px 0;
            color: #333;
        }
        
        /* Timeline styling */
        .timeline-item {
            display: flex;
            margin-bottom: 15px;
        }
        
        .timeline-marker {
            width: 20px;
            height: 20px;
            border-radius: 50%;
            margin-right: 15px;
            margin-top: 5px;
        }
        
        .timeline-content {
            flex-grow: 1;
        }
        
        .timeline-title {
            margin: 0;
            font-weight: bold;
        }
        
        .timeline-date {
            margin: 0;
            color: #666;
        }
        
        .timeline-connector {
            border-left: 2px solid #ddd;
            height: 30px;
            margin-left: 9px;
        }
        
        /* Form styling */
        .form-container {
            background-color: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
        }
        
        /* Notification badge */
        .notification-badge {
            background-color: #e74c3c;
            color: white;
            border-radius: 50%;
            width: 20px;
            height: 20px;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            font-size: 12px;
            margin-left: 5px;
        }
        
        /* Dashboard metrics */
        .dashboard-metric {
            text-align: center;
            padding: 20px;
            background-color: #f8f9fa;
            border-radius: 10px;
            transition: transform 0.2s;
        }
        
        .dashboard-metric:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 20px rgba(0,0,0,0.05);
        }
        
        /* Profile section */
        .profile-section {
            display: flex;
            align-items: center;
        }
        
        .profile-image {
            width: 40px;
            height: 40px;
            border-radius: 50%;
            background-color: #2E7D67;
            color: white;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            margin-right: 10px;
        }
        
        /* Make streatmlit native elements prettier */
        div.stButton > button {
            background-color: #2E7D67;
            color: white;
            font-weight: 600;
            border: none;
            border-radius: 5px;
            padding: 0.5rem 1rem;
            margin-top: 1rem;
        }
        
        div.stButton > button:hover {
            background-color: #246b57;
        }
        
        /* Hide the default Streamlit header/footer */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        /* Responsive adjustments */
        @media (max-width: 768px) {
            .main-header {
                font-size: 28px !important;
            }
            .sub-header {
                font-size: 20px !important;
            }
        }
    </style>
    """, unsafe_allow_html=True)

# Logo placeholder
def get_logo_base64():
    # Create a simple logo as a placeholder
    # In a real app, you would load your actual logo file
    fig, ax = plt.subplots(figsize=(2, 1))
    ax.text(0.5, 0.5, 'RE.ie', fontsize=20, ha='center', va='center', color='#2E7D67')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    
    buf = io.BytesIO()
    fig.savefig(buf, format='png', transparent=True)
    buf.seek(0)
    img_str = base64.b64encode(buf.read()).decode()
    plt.close(fig)
    
    return img_str

# Initialize session state for user authentication
def init_session_state():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'username' not in st.session_state:
        st.session_state.username = ""
    if 'user_type' not in st.session_state:
        st.session_state.user_type = ""  # 'seller' or 'buyer'
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "Home"
    if 'property_data' not in st.session_state:
        st.session_state.property_data = generate_mock_properties(20)
    if 'user_properties' not in st.session_state:
        # For demo: if logged in as seller, they have a property
        st.session_state.user_properties = generate_mock_properties(1)
    if 'saved_properties' not in st.session_state:
        st.session_state.saved_properties = []
    if 'offers_made' not in st.session_state:
        st.session_state.offers_made = []
    if 'offers_received' not in st.session_state:
        st.session_state.offers_received = generate_mock_offers()
    if 'notifications' not in st.session_state:
        st.session_state.notifications = generate_mock_notifications()
    if 'messages' not in st.session_state:
        st.session_state.messages = generate_mock_messages()
    if 'search_filters' not in st.session_state:
        st.session_state.search_filters = {
            'min_price': 0,
            'max_price': 1000000,
            'min_beds': 0,
            'max_beds': 5,
            'property_type': 'All',
            'location': 'All'
        }

# Generate Irish county coordinates for the map
def generate_irish_counties_data():
    counties = {
        'Dublin': (53.3498, -6.2603),
        'Cork': (51.8969, -8.4863),
        'Galway': (53.2707, -9.0568),
        'Limerick': (52.6638, -8.6267),
        'Waterford': (52.2593, -7.1101),
        'Wexford': (52.3369, -6.4633),
        'Kilkenny': (52.6477, -7.2561),
        'Kildare': (53.1589, -6.9091),
        'Meath': (53.6055, -6.6564),
        'Wicklow': (52.9808, -6.0446),
        'Louth': (53.9508, -6.5406),
        'Mayo': (53.8452, -9.3513),
        'Kerry': (52.1543, -9.5668),
        'Tipperary': (52.4738, -8.1619),
        'Clare': (52.9715, -9.0277),
        'Carlow': (52.8408, -6.9261),
        'Cavan': (53.9903, -7.3601),
        'Donegal': (54.6538, -8.1096),
        'Laois': (52.9945, -7.3322),
        'Offaly': (53.2394, -7.7147),
        'Westmeath': (53.5346, -7.4650),
        'Longford': (53.7276, -7.7941),
        'Monaghan': (54.2495, -6.9683),
        'Roscommon': (53.6276, -8.1892),
        'Sligo': (54.2766, -8.4761),
        'Leitrim': (54.1244, -8.0011)
    }
    return counties

# Mock data for demo
def generate_mock_properties(num=6):
    counties = list(generate_irish_counties_data().keys())
    types = ['House', 'Apartment', 'Bungalow', 'Duplex']
    
    # More descriptive property descriptions
    descriptions = [
        "Bright and spacious family home with a south-facing garden in a quiet residential area. Recently renovated kitchen and bathrooms.",
        "Modern apartment in the heart of the city center with stunning views. Secure parking and close to all amenities.",
        "Charming period cottage with original features and character. Includes a private garden and off-street parking.",
        "Luxurious penthouse with panoramic views and a large private terrace. High-end finishes throughout.",
        "Cozy townhouse in a gated community with communal gardens. Perfect for first-time buyers or investors.",
        "Renovated period property with high ceilings and original fireplaces. Close to schools and transport links.",
        "Architect-designed contemporary home with open-plan living spaces and floor-to-ceiling windows.",
        "Traditional farmhouse on a generous plot with outbuildings and potential for expansion.",
        "Waterfront property with private mooring and spectacular views. Rare opportunity in a sought-after location.",
        "Family-friendly semi-detached home in an established neighborhood with excellent schools nearby."
    ]
    
    # More specific addresses
    streets = [
        "Main Street", "Church Road", "Castle Avenue", "Park View", "Riverside Drive",
        "Mill Lane", "High Street", "Ocean View", "Grove Road", "Meadow Way",
        "Abbey Road", "Market Street", "Station Road", "The Green", "New Road",
        "College Road", "Victoria Avenue", "Albert Road", "Brook Lane", "Oak Avenue"
    ]
    
    # Generate county-specific data with realistic coordinates
    county_data = generate_irish_counties_data()
    
    data = []
    for i in range(num):
        county = np.random.choice(counties)
        base_lat, base_lng = county_data[county]
        
        # Add small random offset to base coordinates for property-specific location
        lat = base_lat + (np.random.random() - 0.5) * 0.1
        lng = base_lng + (np.random.random() - 0.5) * 0.1
        
        property_type = np.random.choice(types)
        bedrooms = np.random.randint(1, 6)
        bathrooms = max(1, min(bedrooms, np.random.randint(1, 4)))
        
        # More realistic pricing based on property characteristics and location
        base_price = 250000
        county_multiplier = 1.0
        if county == "Dublin":
            county_multiplier = 1.8
        elif county in ["Cork", "Galway"]:
            county_multiplier = 1.4
        
        type_multiplier = 1.0
        if property_type == "House":
            type_multiplier = 1.2
        elif property_type == "Apartment":
            type_multiplier = 0.9
        
        size_sqm = np.random.randint(30 * bedrooms, 50 * bedrooms)
        
        price = int(base_price * county_multiplier * type_multiplier * (0.8 + 0.4 * np.random.random()) * (0.7 + 0.15 * bedrooms))
        price = round(price / 5000) * 5000  # Round to nearest 5000
        
        # BER (Building Energy Rating) - Irish energy efficiency rating
        ber_ratings = ["A1", "A2", "A3", "B1", "B2", "B3", "C1", "C2", "C3", "D1", "D2", "E1", "E2", "F", "G"]
        ber_weights = [0.01, 0.03, 0.05, 0.08, 0.1, 0.12, 0.15, 0.15, 0.1, 0.08, 0.05, 0.03, 0.02, 0.02, 0.01]
        ber = np.random.choice(ber_ratings, p=ber_weights)
        
        # Add features like garden, parking, etc.
        features = []
        if np.random.random() > 0.3:
            features.append("Garden")
        if np.random.random() > 0.4:
            features.append("Parking")
        if property_type == "Apartment" and np.random.random() > 0.5:
            features.append("Balcony")
        if np.random.random() > 0.7:
            features.append("Newly Renovated")
        if np.random.random() > 0.8:
            features.append("En-suite")
        
        # Generate listing date within the last 30 days
        days_ago = np.random.randint(1, 30)
        listed_date = (datetime.now() - timedelta(days=days_ago)).date()
        
        # Views and saves (for analytics)
        views = np.random.randint(10, 500)
        saves = int(views * np.random.uniform(0.01, 0.1))
        
        # Property ID
        property_id = f"RE{100000 + i}"
        
        # Generate a random street number and select a street
        street_number = np.random.randint(1, 200)
        street = np.random.choice(streets)
        address = f"{street_number} {street}, {county}"
        
        data.append({
            'property_id': property_id,
            'address': address,
            'county': county,
            'price': price,
            'bedrooms': bedrooms,
            'bathrooms': bathrooms,
            'type': property_type,
            'size_sqm': size_sqm,
            'description': np.random.choice(descriptions),
            'ber_rating': ber,
            'features': features,
            'listed_date': listed_date,
            'views': views,
            'saves': saves,
            'lat': lat,
            'lng': lng
        })
    
    return pd.DataFrame(data)

# Generate sample transaction savings data
def generate_savings_data():
    property_values = [400000, 500000, 600000, 700000, 800000]
    
    traditional_fees = [value * 0.015 for value in property_values]  # 1.5% commission
    flat_fee = 1500  # €1,500 flat fee
    savings = [traditional - flat_fee for traditional, flat_fee in zip(traditional_fees, [flat_fee] * len(property_values))]
    
    return property_values, traditional_fees, [flat_fee] * len(property_values), savings

# Generate mock offers for a property
def generate_mock_offers():
    buyer_names = ["John D.", "Sarah M.", "Michael K.", "Emma L.", "David R.", "Anna B."]
    statuses = ["Active", "Active", "Active", "Withdrawn", "Rejected"]
    
    offers = []
    for i in range(3):
        amount = 580000 + i * 5000
        offers.append({
            "buyer": np.random.choice(buyer_names),
            "amount": amount,
            "status": np.random.choice(statuses[:3]),  # Mostly active offers
            "date": (datetime.now() - timedelta(days=i)).strftime("%B %d, %Y"),
            "message": "I'm very interested in this property and would like to arrange a second viewing.",
            "mortgage_approved": np.random.choice([True, False], p=[0.8, 0.2]),
            "deposit_ready": np.random.choice([True, False], p=[0.9, 0.1])
        })
    
    # Sort offers by amount, highest first
    offers = sorted(offers, key=lambda x: x["amount"], reverse=True)
    return offers

# Generate mock notifications
def generate_mock_notifications():
    notification_types = ["offer", "message", "viewing_request", "document", "system"]
    notification_texts = [
        "New offer received: €585,000",
        "New message from John D. regarding your property",
        "New viewing request for Saturday at 2 PM",
        "Sale agreement document requires your signature",
        "Your property listing has been approved and is now live"
    ]
    
    notifications = []
    for i in range(5):
        notifications.append({
            "type": notification_types[i],
            "text": notification_texts[i],
            "date": (datetime.now() - timedelta(days=i)).strftime("%B %d, %Y"),
            "read": i > 1  # First two are unread
        })
    
    return notifications

# Generate mock messages
def generate_mock_messages():
    contacts = ["John D.", "Sarah M.", "Michael K.", "Emma L.", "Support Team"]
    
    conversations = {}
    for contact in contacts:
        # Each contact has a conversation with 3-5 messages
        num_messages = np.random.randint(3, 6)
        messages = []
        
        for i in range(num_messages):
            # Alternate between received and sent messages
            is_from_user = i % 2 == 0
            
            if contact == "Support Team":
                if is_from_user:
                    text = np.random.choice([
                        "I have a question about the legal process. How does the escrow system work?",
                        "When will the property be visible to potential buyers?",
                        "Do I need to be present for all viewings?"
                    ])
                else:
                    text = np.random.choice([
                        "Our escrow system is managed through our secure platform. Buyers place a 10% deposit when their offer is accepted, which is held safely until the sale completes.",
                        "Your property is now live and visible to all users. You can track views in your dashboard.",
                        "You can choose to be present or allow our partner agents to conduct viewings on your behalf."
                    ])
            else:
                if is_from_user:
                    text = np.random.choice([
                        "Thank you for your interest in my property.",
                        "Yes, the property is still available for viewing.",
                        "I've received your offer and will get back to you shortly.",
                        "The garden is approximately 50 square meters."
                    ])
                else:
                    text = np.random.choice([
                        "I'm interested in viewing your property. Is it still available?",
                        "What are the dimensions of the garden?",
                        "I'd like to make an offer of €580,000 for your property.",
                        "Is the parking space included in the sale?"
                    ])
            
            # Message time is between now and 7 days ago
            days_ago = np.random.randint(0, 7)
            hours_ago = np.random.randint(0, 24)
            time = datetime.now() - timedelta(days=days_ago, hours=hours_ago)
            
            messages.append({
                "from_user": is_from_user,
                "text": text,
                "time": time,
                "read": time < datetime.now() - timedelta(days=1)  # Older than 1 day = read
            })
        
        # Sort messages by time
        messages = sorted(messages, key=lambda x: x["time"])
        conversations[contact] = messages
    
    return conversations

# =========================================
# NAVIGATION AND LAYOUT COMPONENTS
# =========================================

# Top navigation
def render_top_navigation():
    cols = st.columns([1, 3, 1])
    
    with cols[0]:
        st.markdown(f'<img src="data:image/png;base64,{get_logo_base64()}" style="height:50px;">', unsafe_allow_html=True)
        
    with cols[1]:
        st.markdown(
            '<div style="display: flex; justify-content: center; margin-top: 10px;">'
            '<a class="nav-link" href="#" onclick="setPage(\'Home\')">Home</a>'
            '<a class="nav-link" href="#" onclick="setPage(\'Properties\')">Properties</a>'
            '<a class="nav-link" href="#" onclick="setPage(\'How It Works\')">How It Works</a>'
            '<a class="nav-link" href="#" onclick="setPage(\'About\')">About</a>'
            '<a class="nav-link" href="#" onclick="setPage(\'Contact\')">Contact</a>'
            '</div>',
            unsafe_allow_html=True
        )
    
    with cols[2]:
        if st.session_state.logged_in:
            # Count unread notifications
            unread_count = sum(1 for n in st.session_state.notifications if not n["read"])
            
            st.markdown(
                f'''
                <div style="text-align: right; margin-top: 10px; display: flex; justify-content: flex-end; align-items: center;">
                    <div class="profile-section">
                        <div class="profile-image">{st.session_state.username[0].upper()}</div>
                        <span>{st.session_state.username}</span>
                        {f'<span class="notification-badge">{unread_count}</span>' if unread_count > 0 else ''}
                    </div>
                </div>
                ''',
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                '<div style="text-align: right; margin-top: 10px;">'
                '<a class="nav-link" href="#" onclick="login()">Sign In</a>'
                '</div>',
                unsafe_allow_html=True
            )
    
    st.markdown('<hr style="margin: 0;">', unsafe_allow_html=True)
    
    # Add JavaScript for navigation
    st.markdown('''
    <script>
        function setPage(page) {
            // In a real app, this would navigate between pages
            // For the demo, we're using Streamlit's sidebar navigation
        }
        
        function login() {
            // In a real app, this would trigger login
            // For the demo, we're using Streamlit's authentication flow
        }
    </script>
    ''', unsafe_allow_html=True)

# Footer
def render_footer():
    st.markdown("""
    <div class="footer">
        <div style="display: flex; justify-content: space-between; margin-bottom: 20px;">
            <div style="flex: 1;">
                <h3>RealEstateIreland.ie</h3>
                <p>A revolutionary approach to buying and selling property in Ireland</p>
            </div>
            <div style="flex: 1;">
                <h3>Quick Links</h3>
                <a href="#" style="display: block; margin: 5px 0; color: #333;">Home</a>
                <a href="#" style="display: block; margin: 5px 0; color: #333;">Properties</a>
                <a href="#" style="display: block; margin: 5px 0; color: #333;">How It Works</a>
                <a href="#" style="display: block; margin: 5px 0; color: #333;">Contact</a>
            </div>
            <div style="flex: 1;">
                <h3>Contact Us</h3>
                <p>📧 support@realestateireland.ie</p>
                <p>☎️ (01) 555-1234</p>
                <p>🏢 42 Grand Canal Square, Dublin 2</p>
            </div>
        </div>
        <hr>
        <p>© 2025 RealEstateIreland.ie | Terms & Conditions | Privacy Policy</p>
    </div>
    """, unsafe_allow_html=True)

# =========================================
# PAGE COMPONENTS - HOME PAGE
# =========================================

# Hero section for homepage
def render_home_hero():
    # Hero section
    st.markdown('<p class="main-header">Sell Your Property for a Flat Fee</p>', unsafe_allow_html=True)
    st.markdown('<p style="font-size: 20px;">Save thousands compared to traditional estate agents.</p>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<div class="saving-box">'
                   '<p style="font-size: 24px;">Just <span class="green-highlight">€1,500 flat fee</span>, no commission.</p>'
                   '<p>Average Dublin seller saves €7,500 in agent fees</p>'
                   '</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.button("List Your Property", key="list_property_btn")
        with col2:
            st.button("Learn More", key="learn_more_btn", type="secondary")

# How it works section for homepage
def render_how_it_works_short():
    st.markdown('---')
    st.markdown('<p class="sub-header">How It Works</p>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="feature-box">'
                   '<h3>1. List Your Property</h3>'
                   '<p>Upload details, photos, and documents. Our AI helps you set the perfect price based on market data.</p>'
                   '</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="feature-box">'
                   '<h3>2. Connect With Buyers</h3>'
                   '<p>Buyers make legally-binding offers with escrow-backed deposits to show serious intent.</p>'
                   '</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="feature-box">'
                   '<h3>3. Secure Sale</h3>'
                   '<p>Our integrated legal partnership handles all the paperwork and ensures a smooth transfer.</p>'
                   '</div>', unsafe_allow_html=True)

# Why choose us section for homepage
def render_why_choose_us():
    st.markdown('---')
    st.markdown('<p class="sub-header">Why Choose RealEstateIreland.ie?</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Create savings comparison chart
        property_values, traditional_fees, flat_fees, savings = generate_savings_data()
        
        # Use Plotly for better looking charts
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=[f"€{value:,}" for value in property_values],
            y=traditional_fees,
            name='Traditional Agent (1.5%)',
            marker_color='#e74c3c'
        ))
        
        fig.add_trace(go.Bar(
            x=[f"€{value:,}" for value in property_values],
            y=flat_fees,
            name='RealEstateIreland.ie (€1,500)',
            marker_color='#2E7D67'
        ))
        
        for i, (trad, flat, saving) in enumerate(zip(traditional_fees, flat_fees, savings)):
            fig.add_annotation(
                x=i,
                y=flat + 500,
                text=f"Save €{int(saving):,}",
                showarrow=False,
                font=dict(
                    color="#2E7D67",
                    size=14,
                    family="Inter, sans-serif"
                )
            )
        
        fig.update_layout(
            title="Fee Comparison: Traditional vs. RealEstateIreland.ie",
            xaxis_title="Property Value",
            yaxis_title="Fee Amount (€)",
            barmode='group',
            plot_bgcolor='white',
            font=dict(
                family="Inter, sans-serif"
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown('<div class="feature-box">'
                   '<h3>🔒 Secure Transactions</h3>'
                   '<p>Legally-binding offer agreements and escrow-backed deposits protect both buyers and sellers.</p>'
                   '</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="feature-box">'
                   '<h3>💼 Legal Partnership</h3>'
                   '<p>Our partner law firm handles all legal aspects of the property transfer efficiently and at pre-agreed rates.</p>'
                   '</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="feature-box">'
                   '<h3>👁️ Full Transparency</h3>'
                   '<p>Track all offers, legal progress, and communication in real-time through our digital dashboard.</p>'
                   '</div>', unsafe_allow_html=True)

# Featured properties section for homepage
def render_featured_properties():
    st.markdown('---')
    st.markdown('<p class="sub-header">Featured Properties</p>', unsafe_allow_html=True)
    
    # Get 6 random properties for featured section
    properties = st.session_state.property_data.sample(min(6, len(st.session_state.property_data)))
    
    # Display properties in a grid
    num_cols = 3
    rows = len(properties) // num_cols + (1 if len(properties) % num_cols > 0 else 0)
    
    for row in range(rows):
        cols = st.columns(num_cols)
        for col_idx in range(num_cols):
            prop_idx = row * num_cols + col_idx
            if prop_idx < len(properties):
                prop = properties.iloc[prop_idx]
                with cols[col_idx]:
                    # Property card with hover effect
                    features_str = ", ".join(prop['features']) if len(prop['features']) > 0 else ""
                    
                    st.markdown(f"""
                    <div class="property-card">
                        <div class="property-image" style="background-color: #eee; display: flex; align-items: center; justify-content: center;">
                            <span style="color: #999;">Property Image</span>
                        </div>
                        <div class="property-details">
                            <p class="property-address">{prop['address']}</p>
                            <p class="property-price">€{prop['price']:,}</p>
                            <p class="property-features">{prop['bedrooms']} bed • {prop['bathrooms']} bath • {prop['size_sqm']} m² • {prop['type']}</p>
                            <p class="property-features">BER: {prop['ber_rating']} {f"• {features_str}" if features_str else ""}</p>
                            <p class="property-description">{prop['description'][:100]}...</p>
                            <p style="color: #666; font-size: 14px;">Listed: {prop['listed_date']}</p>
                            <div style="text-align: center; margin-top: 15px;">
                                <a href="#" class="btn-primary" style="width: 100%;">View Details</a>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

# Market statistics section
def render_market_statistics():
    st.markdown('---')
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="text-align: center;">
            <div class="metric-value">€7,500+</div>
            <p>Average Seller Savings</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="text-align: center;">
            <div class="metric-value">14%</div>
            <p>of Irish Homes Sell 20% Above Asking</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="text-align: center;">
            <div class="metric-value">100%</div>
            <p>Secure Transactions</p>
        </div>
        """, unsafe_allow_html=True)

# =========================================
# PAGE COMPONENTS - SELLER DASHBOARD
# =========================================

# Property listing section
def render_property_listing():
    st.markdown('<p class="sub-header">Your Property Listing</p>', unsafe_allow_html=True)
    
    # If the user has properties
    if len(st.session_state.user_properties) > 0:
        prop = st.session_state.user_properties.iloc[0]
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("""
            <div style="height: 200px; background-color: #eee; border-radius: 5px; display: flex; align-items: center; justify-content: center;">
                <span style="color: #999;">Property Image</span>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            features_str = ", ".join(prop['features']) if len(prop['features']) > 0 else ""
            
            st.markdown(f"""
            <h3>{prop['address']}</h3>
            <p style="color: #2E7D67; font-weight: bold; font-size: 20px;">€{prop['price']:,}</p>
            <p>{prop['bedrooms']} bed • {prop['bathrooms']} bath • {prop['size_sqm']} m² • {prop['type']}</p>
            <p>BER: {prop['ber_rating']} {f"• {features_str}" if features_str else ""}</p>
            <p>{prop['description']}</p>
            <p style="color: #666; font-size: 14px;">Listed: {prop['listed_date']} • <span style="color: #2E7D67;">Active</span></p>
            """, unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.button("Edit Listing", key="edit_listing_btn")
            with col2:
                st.button("Manage Viewings", key="manage_viewings_btn")
            with col3:
                st.button("View Analytics", key="view_analytics_btn")
    else:
        st.markdown("""
        <div style="text-align: center; padding: 40px; background-color: #f8f9fa; border-radius: 10px; margin-bottom: 20px;">
            <h3>You don't have any active property listings</h3>
            <p>Start selling your property today with our flat fee service!</p>
            <a href="#" class="btn-primary">List Your Property</a>
        </div>
        """, unsafe_allow_html=True)

# Analytics section for seller dashboard
def render_seller_analytics():
    st.markdown('<p class="sub-header">Listing Performance</p>', unsafe_allow_html=True)
    
    # Performance metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="dashboard-metric">
            <div class="metric-value">143</div>
            <p>Page Views</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="dashboard-metric">
            <div class="metric-value">12</div>
            <p>Saved by Buyers</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="dashboard-metric">
            <div class="metric-value">8</div>
            <p>Viewing Requests</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="dashboard-metric">
            <div class="metric-value">3</div>
            <p>Offers Received</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Visitor analytics chart
    st.markdown('<p class="section-header">Visitor Activity (Last 30 days)</p>', unsafe_allow_html=True)
    
    # Generate mock analytics data
    dates = pd.date_range(end=datetime.now(), periods=30)
    views_data = np.random.randint(1, 15, size=30).cumsum()  # Cumulative views
    
    # Create chart with plotly
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dates,
        y=views_data,
        mode='lines+markers',
        name='Cumulative Views',
        line=dict(color='#2E7D67', width=2),
        marker=dict(size=6, color='#2E7D67')
    ))
    
    fig.update_layout(
        title='Property Viewing Activity',
        xaxis_title='Date',
        yaxis_title='Cumulative Views',
        plot_bgcolor='white',
        font=dict(
            family="Inter, sans-serif"
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Visitor demographics
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<p class="section-header">Visitor Demographics</p>', unsafe_allow_html=True)
        
        # Mock demographics data
        demographics = {
            'First-time Buyers': 45,
            'Moving Up': 30,
            'Investors': 15,
            'Downsizers': 10
        }
        
        fig = px.pie(
            values=list(demographics.values()),
            names=list(demographics.keys()),
            color_discrete_sequence=px.colors.sequential.Viridis
        )
        
        fig.update_layout(
            font=dict(
                family="Inter, sans-serif"
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown('<p class="section-header">Interest by Location</p>', unsafe_allow_html=True)
        
        # Mock location data
        locations = {
            'Dublin': 60,
            'Cork': 15,
            'Galway': 10,
            'Other Counties': 15
        }
        
        fig = px.bar(
            x=list(locations.keys()),
            y=list(locations.values()),
            color=list(locations.keys()),
            color_discrete_sequence=px.colors.sequential.Viridis
        )
        
        fig.update_layout(
            xaxis_title='Location',
            yaxis_title='Percentage of Viewers',
            showlegend=False,
            font=dict(
                family="Inter, sans-serif"
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)

# Offers section for seller dashboard
def render_seller_offers():
    st.markdown('<p class="sub-header">Current Offers</p>', unsafe_allow_html=True)
    
    if len(st.session_state.offers_received) > 0:
        for offer in st.session_state.offers_received:
            mortgage_status = "✅ Mortgage Approved" if offer["mortgage_approved"] else "⚠️ Mortgage Pending"
            deposit_status = "✅ Deposit Ready" if offer["deposit_ready"] else "⚠️ Deposit Pending"
            
            st.markdown(f"""
            <div style="border: 1px solid #ddd; border-radius: 10px; padding: 15px; margin-bottom: 15px;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <h3 style="margin: 0; color: #2E7D67;">€{offer['amount']:,}</h3>
                        <p style="margin: 5px 0;">From: {offer['buyer']} • {offer['date']}</p>
                        <p>{offer['message']}</p>
                        <p style="margin: 5px 0;">{mortgage_status} • {deposit_status}</p>
                    </div>
                    <div>
                        <a href="#" class="btn-secondary">View Details</a>
                        <a href="#" class="btn-primary" style="background-color: #28a745; margin-left: 10px;">Accept Offer</a>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="text-align: center; padding: 20px; background-color: #f8f9fa; border-radius: 10px; margin-bottom: 20px;">
            <p>No offers received yet. Offers will appear here once buyers make them.</p>
        </div>
        """, unsafe_allow_html=True)

# Sale timeline section for seller dashboard
def render_sale_timeline():
    st.markdown('<p class="sub-header">Sale Timeline</p>', unsafe_allow_html=True)
    
    timeline_items = [
        {"date": "May 10, 2025", "event": "Property Listed", "status": "Completed"},
        {"date": "May 12-20, 2025", "event": "Viewing Period", "status": "In Progress"},
        {"date": "May 18-25, 2025", "event": "Offer Collection", "status": "In Progress"},
        {"date": "TBD", "event": "Offer Acceptance", "status": "Pending"},
        {"date": "TBD", "event": "Legal Process", "status": "Pending"},
        {"date": "TBD", "event": "Sale Completion", "status": "Pending"}
    ]
    
    for i, item in enumerate(timeline_items):
        status_color = "#28a745" if item["status"] == "Completed" else "#ffc107" if item["status"] == "In Progress" else "#6c757d"
        
        st.markdown(f"""
        <div class="timeline-item">
            <div class="timeline-marker" style="background-color: {status_color};"></div>
            <div class="timeline-content">
                <p class="timeline-title">{item['event']}</p>
                <p class="timeline-date">{item['date']} • <span style="color: {status_color};">{item['status']}</span></p>
            </div>
        </div>
        {"<div class='timeline-connector'></div>" if i < len(timeline_items) - 1 else ""}
        """, unsafe_allow_html=True)

# Messaging interface
def render_messaging():
    st.markdown('<p class="sub-header">Messages</p>', unsafe_allow_html=True)
    
    if st.session_state.messages:
        # Create two columns: contact list and conversation view
        col1, col2 = st.columns([1, 3])
        
        with col1:
            st.markdown("<h3>Contacts</h3>", unsafe_allow_html=True)
            
            # Display contact list
            for contact in st.session_state.messages.keys():
                # Get the last message
                last_message = st.session_state.messages[contact][-1]
                # Check if there are unread messages
                has_unread = any(not m["read"] for m in st.session_state.messages[contact] if not m["from_user"])
                
                st.markdown(f"""
                <div style="border: 1px solid #ddd; border-radius: 10px; padding: 10px; margin-bottom: 10px; cursor: pointer; 
                     background-color: {'#f0f7f4' if has_unread else '#f8f9fa'};">
                    <div style="display: flex; justify-content: space-between;">
                        <strong>{contact}</strong>
                        {f'<span class="notification-badge">•</span>' if has_unread else ''}
                    </div>
                    <p style="margin: 5px 0; font-size: 12px; color: #666; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
                        {last_message["text"][:30] + "..." if len(last_message["text"]) > 30 else last_message["text"]}
                    </p>
                    <p style="margin: 0; font-size: 11px; color: #999;">
                        {last_message["time"].strftime("%b %d, %H:%M")}
                    </p>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            # Display selected conversation (first contact for demo)
            selected_contact = list(st.session_state.messages.keys())[0]
            
            st.markdown(f"<h3>Conversation with {selected_contact}</h3>", unsafe_allow_html=True)
            
            # Display messages
            for message in st.session_state.messages[selected_contact]:
                alignment = "flex-end" if message["from_user"] else "flex-start"
                bg_color = "#2E7D67" if message["from_user"] else "#f1f1f1"
                text_color = "white" if message["from_user"] else "#333"
                
                st.markdown(f"""
                <div style="display: flex; justify-content: {alignment}; margin-bottom: 10px;">
                    <div style="background-color: {bg_color}; color: {text_color}; padding: 10px; border-radius: 10px; max-width: 80%;">
                        <p style="margin: 0;">{message["text"]}</p>
                        <p style="margin: 0; font-size: 11px; color: {'#e0e0e0' if message["from_user"] else '#999'}; text-align: right;">
                            {message["time"].strftime("%H:%M")}
                        </p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            # Message input
            st.markdown("""
            <div style="display: flex; margin-top: 20px;">
                <input type="text" placeholder="Type a message..." style="flex-grow: 1; padding: 10px; border-radius: 5px; border: 1px solid #ddd;">
                <button class="btn-primary" style="margin-left: 10px;">Send</button>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="text-align: center; padding: 20px; background-color: #f8f9fa; border-radius: 10px;">
            <p>No messages yet. When buyers contact you, conversations will appear here.</p>
        </div>
        """, unsafe_allow_html=True)

# =========================================
# PAGE COMPONENTS - BUYER DASHBOARD
# =========================================

# Saved properties section for buyer dashboard
def render_buyer_saved_properties():
    st.markdown('<p class="sub-header">Saved Properties</p>', unsafe_allow_html=True)
    
    if len(st.session_state.saved_properties) > 0:
        # Display saved properties in a grid
        num_cols = 2
        rows = len(st.session_state.saved_properties) // num_cols + (1 if len(st.session_state.saved_properties) % num_cols > 0 else 0)
        
        for row in range(rows):
            cols = st.columns(num_cols)
            for col_idx in range(num_cols):
                prop_idx = row * num_cols + col_idx
                if prop_idx < len(st.session_state.saved_properties):
                    prop = st.session_state.saved_properties[prop_idx]
                    with cols[col_idx]:
                        features_str = ", ".join(prop['features']) if len(prop['features']) > 0 else ""
                        
                        st.markdown(f"""
                        <div class="property-card">
                            <div class="property-image" style="background-color: #eee; display: flex; align-items: center; justify-content: center;">
                                <span style="color: #999;">Property Image</span>
                            </div>
                            <div class="property-details">
                                <p class="property-address">{prop['address']}</p>
                                <p class="property-price">€{prop['price']:,}</p>
                                <p class="property-features">{prop['bedrooms']} bed • {prop['bathrooms']} bath • {prop['size_sqm']} m² • {prop['type']}</p>
                                <p class="property-features">BER: {prop['ber_rating']} {f"• {features_str}" if features_str else ""}</p>
                                <div style="display: flex; justify-content: space-between; margin-top: 15px;">
                                    <a href="#" class="btn-secondary">Remove</a>
                                    <a href="#" class="btn-primary">View Details</a>
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="text-align: center; padding: 40px; background-color: #f8f9fa; border-radius: 10px; margin-bottom: 20px;">
            <h3>You haven't saved any properties yet</h3>
            <p>Browse properties and click the save button to add them to your favorites.</p>
            <a href="#" class="btn-primary">Browse Properties</a>
        </div>
        """, unsafe_allow_html=True)

# Offers made section for buyer dashboard
def render_buyer_offers():
    st.markdown('<p class="sub-header">Your Offers</p>', unsafe_allow_html=True)
    
    if len(st.session_state.offers_made) > 0:
        for offer in st.session_state.offers_made:
            st.markdown(f"""
            <div style="border: 1px solid #ddd; border-radius: 10px; padding: 15px; margin-bottom: 15px;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <h3 style="margin: 0; color: #2E7D67;">€{offer['amount']:,}</h3>
                        <p style="margin: 5px 0;">For: {offer['address']} • {offer['date']}</p>
                        <p>Status: <span style="color: {'#28a745' if offer['status'] == 'Accepted' else '#ffc107' if offer['status'] == 'Pending' else '#dc3545'};">{offer['status']}</span></p>
                    </div>
                    <div>
                        <a href="#" class="btn-secondary">Withdraw Offer</a>
                        <a href="#" class="btn-primary" style="margin-left: 10px;">View Property</a>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="text-align: center; padding: 20px; background-color: #f8f9fa; border-radius: 10px; margin-bottom: 20px;">
            <p>You haven't made any offers yet. When you make an offer, it will appear here with its current status.</p>
        </div>
        """, unsafe_allow_html=True)

# Saved searches section for buyer dashboard
def render_buyer_saved_searches():
    st.markdown('<p class="sub-header">Saved Searches</p>', unsafe_allow_html=True)
    
    # Mock saved searches
    saved_searches = [
        {"name": "Dublin 4 Apartments", "criteria": "Dublin 4 • Apartment • 1-2 beds • €300k-€450k"},
        {"name": "Family Homes in Galway", "criteria": "Galway • House • 3+ beds • €400k-€600k"}
    ]
    
    if saved_searches:
        for search in saved_searches:
            st.markdown(f"""
            <div style="border: 1px solid #ddd; border-radius: 10px; padding: 15px; margin-bottom: 15px;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <h3 style="margin: 0;">{search['name']}</h3>
                        <p style="margin: 5px 0;">{search['criteria']}</p>
                    </div>
                    <div>
                        <a href="#" class="btn-secondary">Delete</a>
                        <a href="#" class="btn-primary" style="margin-left: 10px;">Run Search</a>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="text-align: center; padding: 20px; background-color: #f8f9fa; border-radius: 10px; margin-bottom: 20px;">
            <p>No saved searches yet. Save your search criteria to receive alerts when new properties match.</p>
        </div>
        """, unsafe_allow_html=True)

# =========================================
# PAGE COMPONENTS - PROPERTY SEARCH
# =========================================

# Search filters for property search page
def render_search_filters():
    st.markdown('<p class="sub-header">Find Your Perfect Property</p>', unsafe_allow_html=True)
    
    st.markdown('<div class="form-container">', unsafe_allow_html=True)
    
    # Layout the filters in columns
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Location filter
        st.selectbox("Location", ["All"] + sorted(list(generate_irish_counties_data().keys())), key="location_filter")
        
        # Property type filter
        st.selectbox("Property Type", ["All", "House", "Apartment", "Bungalow", "Duplex"], key="type_filter")
    
    with col2:
        # Price range filter
        col1, col2 = st.columns(2)
        with col1:
            st.number_input("Min Price (€)", min_value=0, max_value=5000000, value=0, step=50000, key="min_price_filter")
        with col2:
            st.number_input("Max Price (€)", min_value=0, max_value=5000000, value=1000000, step=50000, key="max_price_filter")
        
        # Bedrooms filter
        col1, col2 = st.columns(2)
        with col1:
            st.number_input("Min Beds", min_value=0, max_value=10, value=0, step=1, key="min_beds_filter")
        with col2:
            st.number_input("Max Beds", min_value=0, max_value=10, value=5, step=1, key="max_beds_filter")
    
    with col3:
        # More filters
        st.multiselect("Features", ["Garden", "Parking", "Balcony", "Newly Renovated", "En-suite"], key="features_filter")
        
        # BER rating filter
        st.multiselect("BER Rating", ["A1", "A2", "A3", "B1", "B2", "B3", "C1", "C2", "C3", "D1", "D2", "E1", "E2", "F", "G"], key="ber_filter")
    
    # Search button and save search
    col1, col2 = st.columns(2)
    with col1:
        st.button("Search Properties", key="search_btn", type="primary")
    with col2:
        st.button("Save This Search", key="save_search_btn")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Property search results
def render_search_results():
    st.markdown('<p class="sub-header">Search Results</p>', unsafe_allow_html=True)
    
    # Get the full property dataset
    properties = st.session_state.property_data
    
    # Filter the properties based on search filters (for the demo, just show all)
    # In a real app, you would apply the filters from st.session_state.search_filters
    
    # Sort options
    sort_options = st.selectbox(
        "Sort By",
        ["Newest First", "Price (Low to High)", "Price (High to Low)", "Most Popular"],
        key="sort_option"
    )
    
    # Display count
    st.markdown(f"<p>{len(properties)} properties found</p>", unsafe_allow_html=True)
    
    # Display properties in a grid
    num_cols = 2
    rows = len(properties) // num_cols + (1 if len(properties) % num_cols > 0 else 0)
    
    for row in range(min(5, rows)):  # Limit to 10 properties for demo
        cols = st.columns(num_cols)
        for col_idx in range(num_cols):
            prop_idx = row * num_cols + col_idx
            if prop_idx < len(properties):
                prop = properties.iloc[prop_idx]
                with cols[col_idx]:
                    features_str = ", ".join(prop['features']) if len(prop['features']) > 0 else ""
                    
                    st.markdown(f"""
                    <div class="property-card">
                        <div class="property-image" style="background-color: #eee; display: flex; align-items: center; justify-content: center;">
                            <span style="color: #999;">Property Image</span>
                        </div>
                        <div class="property-details">
                            <p class="property-address">{prop['address']}</p>
                            <p class="property-price">€{prop['price']:,}</p>
                            <p class="property-features">{prop['bedrooms']} bed • {prop['bathrooms']} bath • {prop['size_sqm']} m² • {prop['type']}</p>
                            <p class="property-features">BER: {prop['ber_rating']} {f"• {features_str}" if features_str else ""}</p>
                            <p class="property-description">{prop['description'][:100]}...</p>
                            <p style="color: #666; font-size: 14px;">Listed: {prop['listed_date']}</p>
                            <div style="display: flex; justify-content: space-between; margin-top: 15px;">
                                <a href="#" class="btn-secondary">Save Property</a>
                                <a href="#" class="btn-primary">View Details</a>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
    
    # Pagination
    st.markdown("""
    <div style="display: flex; justify-content: center; margin-top: 20px;">
        <a href="#" class="btn-secondary">Previous</a>
        <span style="margin: 0 20px; line-height: 40px;">Page 1 of 5</span>
        <a href="#" class="btn-secondary">Next</a>
    </div>
    """, unsafe_allow_html=True)

# Property map view
def render_property_map():
    st.markdown('<p class="sub-header">Map View</p>', unsafe_allow_html=True)
    
    # Create a map centered on Ireland
    m = folium.Map(location=[53.3498, -7.2603], zoom_start=7)
    
    # Add property markers to the map
    for idx, prop in st.session_state.property_data.iterrows():
        # Only process the first 20 properties for performance
        if idx >= 20:
            break
            
        # Create popup content
        popup_content = f"""
        <div style="width: 200px;">
            <h4>{prop['address']}</h4>
            <p style="font-weight: bold; color: #2E7D67;">€{prop['price']:,}</p>
            <p>{prop['bedrooms']} bed • {prop['bathrooms']} bath • {prop['type']}</p>
            <a href="#" style="color: #2E7D67;">View Details</a>
        </div>
        """
        
        # Add marker
        folium.Marker(
            location=[prop['lat'], prop['lng']],
            popup=folium.Popup(popup_content, max_width=300),
            icon=folium.Icon(color='green', icon='home')
        ).add_to(m)
    
    # Display the map
    folium_static(m, width=1200, height=600)

# =========================================
# PAGE COMPONENTS - HOW IT WORKS
# =========================================

# Detailed process steps for How It Works page
def render_process_steps():
    st.markdown('<p class="main-header">How RealEstateIreland.ie Works</p>', unsafe_allow_html=True)
    st.markdown('<p>Our platform revolutionizes property transactions in Ireland with a transparent, secure, and cost-effective process.</p>', unsafe_allow_html=True)
    
    # For Sellers section
    st.markdown('<p class="sub-header">For Sellers</p>', unsafe_allow_html=True)
    
    st.markdown('''
    <div class="process-step">
        <div class="process-step-number">1</div>
        <h3>List Your Property</h3>
        <p>Create your property listing with comprehensive details:</p>
        <ul>
            <li>Upload high-quality photos and floor plans</li>
            <li>Provide detailed property information and features</li>
            <li>Upload necessary documents (title deeds, BER certificate, etc.)</li>
            <li>Our AI pricing algorithm suggests an optimal asking price based on market data</li>
        </ul>
        <p>Pay a flat €1,500 fee – no hidden costs or commissions.</p>
    </div>
    
    <div class="process-step">
        <div class="process-step-number">2</div>
        <h3>Manage Viewings & Inquiries</h3>
        <p>Take control of the viewing process:</p>
        <ul>
            <li>Potential buyers can book viewings through our calendar system</li>
            <li>Receive real-time notifications for new viewing requests</li>
            <li>Communicate with interested buyers via our secure messaging system</li>
            <li>Get feedback from viewings to help improve your listing</li>
        </ul>
    </div>
    
    <div class="process-step">
        <div class="process-step-number">3</div>
        <h3>Receive & Manage Offers</h3>
        <p>Our secure offer management system provides:</p>
        <ul>
            <li>Legally-binding digital offer agreements</li>
            <li>Transparency with all offers visible in your dashboard</li>
            <li>Buyer verification with mortgage approval and deposit confirmation</li>
            <li>Easy comparison of multiple offers</li>
        </ul>
    </div>
    
    <div class="process-step">
        <div class="process-step-number">4</div>
        <h3>Complete the Sale</h3>
        <p>Our integrated legal process ensures a smooth closing:</p>
        <ul>
            <li>Partner with our network of trusted solicitors at pre-agreed rates</li>
            <li>Secure escrow system for buyer deposits</li>
            <li>Digital document signing for all legal paperwork</li>
            <li>Real-time tracking of the legal process</li>
            <li>Transparent timeline to completion</li>
        </ul>
    </div>
    ''', unsafe_allow_html=True)
    
    # For Buyers section
    st.markdown('<p class="sub-header">For Buyers</p>', unsafe_allow_html=True)
    
    st.markdown('''
    <div class="process-step">
        <div class="process-step-number">1</div>
        <h3>Find Your Dream Property</h3>
        <p>Our advanced search tools help you find the perfect home:</p>
        <ul>
            <li>Filter properties by location, price, features, and more</li>
            <li>View high-resolution photos and detailed property information</li>
            <li>Save favorite properties and create alerts for new listings</li>
            <li>See property history and market data insights</li>
        </ul>
    </div>
    
    <div class="process-step">
        <div class="process-step-number">2</div>
        <h3>Schedule Viewings</h3>
        <p>Book property viewings directly through the platform:</p>
        <ul>
            <li>See available viewing slots in real-time</li>
            <li>Request private viewings at your convenience</li>
            <li>Communicate with sellers through our secure messaging system</li>
            <li>Store notes and ratings for viewed properties</li>
        </ul>
    </div>
    
    <div class="process-step">
        <div class="process-step-number">3</div>
        <h3>Make a Serious Offer</h3>
        <p>Our platform ensures your offer is taken seriously:</p>
        <ul>
            <li>Submit legally-binding offers with your mortgage approval details</li>
            <li>Place a secure deposit in escrow to show your commitment</li>
            <li>Track the status of your offer in real-time</li>
            <li>Receive notifications of counter-offers or acceptance</li>
        </ul>
    </div>
    
    <div class="process-step">
        <div class="process-step-number">4</div>
        <h3>Secure Your New Home</h3>
        <p>Once your offer is accepted, our streamlined closing process begins:</p>
        <ul>
            <li>Connect with our network of trusted solicitors at competitive rates</li>
            <li>Access all necessary legal documents through your dashboard</li>
            <li>Monitor the progress of surveys, searches, and title transfers</li>
            <li>Complete the purchase with confidence through our secure platform</li>
        </ul>
    </div>
    ''', unsafe_allow_html=True)

# Key benefits comparison section for How It Works page
def render_benefits_comparison():
    st.markdown('<p class="sub-header">Why Choose Our Platform?</p>', unsafe_allow_html=True)
    
    # Create comparison table
    comparison_data = {
        "Feature": [
            "Seller Fees", 
            "Transparency", 
            "Transaction Security", 
            "Legal Integration", 
            "Communication", 
            "Sale Timeline"
        ],
        "Traditional Estate Agents": [
            "1-2% commission + VAT (€6,000-€12,000+ on average sale)",
            "Limited visibility into offers and negotiation process",
            "No standard deposit or offer protection",
            "Separate, often disconnected legal process",
            "Agent-mediated, often delayed",
            "Typically 3-6 months with delays"
        ],
        "RealEstateIreland.ie": [
            "€1,500 flat fee (save €4,500+ on average sale)",
            "Full visibility of all offers and property interest",
            "Legally-binding offers with escrow-backed deposits",
            "Integrated legal partnership with streamlined process",
            "Direct, real-time messaging between parties",
            "Typically 2-4 months with real-time tracking"
        ]
    }
    
    # Convert to DataFrame
    df_comparison = pd.DataFrame(comparison_data)
    
    # Display as HTML table with styling
    st.markdown(f"""
    <div style="overflow-x: auto;">
        <table style="width: 100%; border-collapse: collapse; margin: 20px 0;">
            <thead>
                <tr style="background-color: #2E7D67; color: white;">
                    <th style="padding: 12px; text-align: left; border: 1px solid #ddd;">{df_comparison.columns[0]}</th>
                    <th style="padding: 12px; text-align: left; border: 1px solid #ddd;">{df_comparison.columns[1]}</th>
                    <th style="padding: 12px; text-align: left; border: 1px solid #ddd;">{df_comparison.columns[2]}</th>
                </tr>
            </thead>
            <tbody>
                {"".join([f"""
                <tr style="background-color: {'#f8f9fa' if i % 2 == 0 else 'white'};">
                    <td style="padding: 12px; text-align: left; border: 1px solid #ddd; font-weight: bold;">{df_comparison.iloc[i, 0]}</td>
                    <td style="padding: 12px; text-align: left; border: 1px solid #ddd;">{df_comparison.iloc[i, 1]}</td>
                    <td style="padding: 12px; text-align: left; border: 1px solid #ddd; color: #2E7D67; font-weight: {'bold' if i == 0 else 'normal'};">{df_comparison.iloc[i, 2]}</td>
                </tr>
                """ for i in range(len(df_comparison))])}
            </tbody>
        </table>
    </div>
    """, unsafe_allow_html=True)

# Testimonials section for How It Works page
def render_testimonials():
    st.markdown('<p class="sub-header">What Our Users Say</p>', unsafe_allow_html=True)
    
    # Create testimonials
    testimonials = [
        {
            "name": "Sarah O'Sullivan",
            "location": "Dublin",
            "type": "Seller",
            "quote": "I saved over €9,000 in agent fees and sold my house within 3 weeks! The platform made everything transparent and I always knew exactly what was happening.",
            "rating": 5
        },
        {
            "name": "John Murphy",
            "location": "Galway",
            "type": "Buyer",
            "quote": "As a first-time buyer, the legally-binding offer system gave me confidence that once my offer was accepted, the property was secured. No more gazumping!",
            "rating": 5
        },
        {
            "name": "Emma Kennedy",
            "location": "Cork",
            "type": "Seller",
            "quote": "The integrated legal process was a game-changer. What normally takes months was completed in just 6 weeks, with far less stress.",
            "rating": 4
        }
    ]
    
    # Display testimonials in columns
    cols = st.columns(len(testimonials))
    
    for i, (col, testimonial) in enumerate(zip(cols, testimonials)):
        with col:
            stars = "★" * testimonial["rating"] + "☆" * (5 - testimonial["rating"])
            
            st.markdown(f"""
            <div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; height: 100%;">
                <p style="font-style: italic;">"{testimonial['quote']}"</p>
                <p style="color: #2E7D67; margin-bottom: 5px;">{stars}</p>
                <p style="font-weight: bold; margin-bottom: 0;">{testimonial['name']}</p>
                <p style="margin-top: 0; color: #666;">{testimonial['location']} • {testimonial['type']}</p>
            </div>
            """, unsafe_allow_html=True)

# FAQ section for How It Works page
def render_faq():
    st.markdown('<p class="sub-header">Frequently Asked Questions</p>', unsafe_allow_html=True)
    
    # FAQ items
    faqs = [
        {
            "question": "How much can I save using RealEstateIreland.ie instead of a traditional estate agent?",
            "answer": "On average, sellers save €4,500-€10,500 on a typical Dublin property. Traditional agents charge 1-2% + VAT of the sale price (€6,000-€12,000 on a €600,000 property), while our flat fee is just €1,500 regardless of your property value."
        },
        {
            "question": "Is my deposit secure when making an offer?",
            "answer": "Yes, all deposits are held in a secure escrow account managed by our regulated financial partners. The funds are only released according to the terms of the offer agreement, providing protection for both buyers and sellers."
        },
        {
            "question": "Who handles the legal aspects of the property transfer?",
            "answer": "We partner with a network of experienced property solicitors across Ireland who handle the legal transfer process. You can choose from our list of partner firms, all offering competitive rates negotiated for our users."
        },
        {
            "question": "How long does the entire process take from listing to sale completion?",
            "answer": "While every property is different, our users typically complete sales within 2-4 months, compared to the traditional 3-6 months. Our integrated platform and streamlined legal process help reduce unnecessary delays."
        },
        {
            "question": "What happens if a buyer withdraws after making an offer?",
            "answer": "Our legally-binding offer agreements include clear withdrawal conditions and penalties. If a buyer withdraws without a valid reason (such as failed survey or mortgage approval), they may forfeit their deposit, providing sellers with compensation for time lost."
        }
    ]
    
    # Create expandable FAQ items
    for i, faq in enumerate(faqs):
        with st.expander(faq["question"]):
            st.markdown(f"<p>{faq['answer']}</p>", unsafe_allow_html=True)

# =========================================
# PAGE COMPONENTS - ABOUT US
# =========================================

# Company story section for About Us page
def render_company_story():
    st.markdown('<p class="main-header">About RealEstateIreland.ie</p>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="margin-bottom: 30px;">
        <h3>Our Mission</h3>
        <p>At RealEstateIreland.ie, we're revolutionizing property transactions in Ireland by creating a more transparent, efficient, and cost-effective alternative to traditional estate agencies.</p>
        
        <p>We believe that selling your home shouldn't cost you thousands in commission fees. We believe that buying a property shouldn't be a stressful experience filled with uncertainty. And we believe that technology can transform the outdated property market to benefit everyone.</p>
    </div>
    
    <div style="margin-bottom: 30px;">
        <h3>Our Story</h3>
        <p>Founded in 2025 by Nathan Walsh, RealEstateIreland.ie emerged from a personal frustration with the traditional property market. After experiencing the inefficiency, lack of transparency, and high costs associated with buying and selling property in Ireland, Nathan saw an opportunity to create something better.</p>
        
        <p>Drawing on experience in finance and technology, he developed a platform that combines the efficiency of online property listings with the security of integrated legal processes and the transparency of a digital transaction management system.</p>
    </div>
    
    <div style="margin-bottom: 30px;">
        <h3>Our Vision</h3>
        <p>We envision a future where property transactions in Ireland are:</p>
        <ul>
            <li><strong>Transparent:</strong> Where all parties have full visibility into the process</li>
            <li><strong>Efficient:</strong> Where sales complete in weeks, not months</li>
            <li><strong>Affordable:</strong> Where sellers keep more of their equity</li>
            <li><strong>Secure:</strong> Where offers are binding and deposits are protected</li>
        </ul>
        
        <p>We're starting in Ireland, but our ambition is to expand our model to other markets where property transactions remain inefficient and costly.</p>
    </div>
    """, unsafe_allow_html=True)

# Team section for About Us page
def render_team():
    st.markdown('<p class="sub-header">Our Team</p>', unsafe_allow_html=True)
    
    # Team members
    team_members = [
        {
            "name": "Nathan Walsh",
            "title": "Founder & CEO",
            "bio": "MSc in Finance with experience in fintech and real estate. Passionate about using technology to solve market inefficiencies."
        },
        {
            "name": "Sarah O'Brien",
            "title": "Head of Operations",
            "bio": "Former real estate agent with 15 years of experience in the Irish property market. Expert in property transactions and customer service."
        },
        {
            "name": "Michael Chen",
            "title": "Chief Technology Officer",
            "bio": "Software engineer with a background in secure payment systems and blockchain technology. Leading our platform development and security."
        },
        {
            "name": "Emma Kelly",
            "title": "Legal Partnerships Director",
            "bio": "Solicitor with expertise in property law. Manages our network of legal partners to ensure smooth and compliant transactions."
        }
    ]
    
    # Display team in grid
    cols = st.columns(len(team_members) // 2)
    
    for i, team_member in enumerate(team_members):
        with cols[i % len(cols)]:
            st.markdown(f"""
            <div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
                <div style="width: 100px; height: 100px; border-radius: 50%; background-color: #2E7D67; color: white; display: flex; align-items: center; justify-content: center; margin: 0 auto 15px auto;">
                    <span style="font-size: 36px; font-weight: bold;">{team_member['name'][0]}</span>
                </div>
                <h3 style="text-align: center; margin-bottom: 5px;">{team_member['name']}</h3>
                <p style="text-align: center; color: #2E7D67; margin-top: 0; font-weight: 600;">{team_member['title']}</p>
                <p style="text-align: center;">{team_member['bio']}</p>
            </div>
            """, unsafe_allow_html=True)

# Press section for About Us page
def render_press():
    st.markdown('<p class="sub-header">Press & Media</p>', unsafe_allow_html=True)
    
    # Press mentions
    press_items = [
        {
            "source": "Irish Times",
            "title": "New Property Platform Aims to Disrupt Traditional Estate Agents",
            "date": "April 2025",
            "excerpt": "RealEstateIreland.ie launches with a mission to save Irish homeowners thousands in estate agent fees..."
        },
        {
            "source": "Silicon Republic",
            "title": "Irish Fintech Startup Secures €1.2M Seed Funding",
            "date": "March 2025",
            "excerpt": "Property technology platform RealEstateIreland.ie has secured seed funding to expand its innovative flat-fee model..."
        },
        {
            "source": "Irish Independent",
            "title": "Property Market Disruptor Could Save Sellers Thousands",
            "date": "February 2025",
            "excerpt": "A new Irish startup is challenging traditional estate agents with a transparent, flat-fee approach..."
        }
    ]
    
    # Display press items
    for item in press_items:
        st.markdown(f"""
        <div style="border-left: 4px solid #2E7D67; padding-left: 20px; margin-bottom: 20px;">
            <p style="font-weight: bold; margin-bottom: 5px;">{item['title']}</p>
            <p style="color: #666; margin-top: 0; margin-bottom: 5px;">{item['source']} • {item['date']}</p>
            <p>"{item['excerpt']}"</p>
            <a href="#" style="color: #2E7D67;">Read Full Article</a>
        </div>
        """, unsafe_allow_html=True)

# =========================================
# PAGE COMPONENTS - CONTACT
# =========================================

# Contact form
def render_contact_form():
    st.markdown('<p class="main-header">Contact Us</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown('<div class="form-container">', unsafe_allow_html=True)
        
        st.text_input("Name", key="contact_name")
        st.text_input("Email", key="contact_email")
        st.selectbox("Inquiry Type", [
            "General Question",
            "Selling a Property",
            "Buying a Property",
            "Legal Process",
            "Technical Support",
            "Partnership Opportunity",
            "Press Inquiry"
        ], key="contact_type")
        st.text_area("Message", height=150, key="contact_message")
        
        st.button("Send Message", key="send_message_btn", type="primary")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px;">
            <h3>Contact Information</h3>
            <p><strong>Email:</strong> support@realestateireland.ie</p>
            <p><strong>Phone:</strong> (01) 555-1234</p>
            <p><strong>Address:</strong> 42 Grand Canal Square, Dublin 2</p>
            
            <h3 style="margin-top: 20px;">Operating Hours</h3>
            <p>Monday - Friday: 9:00 AM - 6:00 PM</p>
            <p>Saturday: 10:00 AM - 2:00 PM</p>
            <p>Sunday: Closed</p>
        </div>
        
        <div style="margin-top: 20px; background-color: #f8f9fa; padding: 20px; border-radius: 10px;">
            <h3>Join Our Team</h3>
            <p>We're growing! Check out our <a href="#" style="color: #2E7D67;">careers page</a> for current opportunities.</p>
        </div>
        """, unsafe_allow_html=True)

# =========================================
# PAGE COMPONENTS - PROPERTY UPLOAD
# =========================================

# Property upload form
def render_property_upload():
    st.markdown('<p class="main-header">List Your Property</p>', unsafe_allow_html=True)
    st.markdown('<p>Complete the form below to list your property on RealEstateIreland.ie for a flat fee of €1,500.</p>', unsafe_allow_html=True)
    
    # Create tabs for the multi-step form
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "1. Property Details", 
        "2. Description & Features", 
        "3. Photos & Documents", 
        "4. Price & Availability", 
        "5. Review & Payment"
    ])
    
    with tab1:
        st.markdown('<div class="form-container">', unsafe_allow_html=True)
        st.markdown('<h3>Property Location & Type</h3>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("Address Line 1", key="property_address1")
            st.text_input("Address Line 2 (Optional)", key="property_address2")
            st.text_input("Town/City", key="property_city")
        with col2:
            st.selectbox("County", sorted(list(generate_irish_counties_data().keys())), key="property_county")
            st.text_input("Eircode", key="property_eircode")
            st.selectbox("Property Type", ["House", "Apartment", "Bungalow", "Duplex"], key="property_type")
        
        st.markdown('<h3>Property Specifications</h3>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.number_input("Bedrooms", min_value=0, max_value=20, value=3, key="property_bedrooms")
        with col2:
            st.number_input("Bathrooms", min_value=0, max_value=10, value=2, key="property_bathrooms")
        with col3:
            st.number_input("Size (m²)", min_value=0, max_value=1000, value=120, key="property_size")
        
        col1, col2 = st.columns(2)
        with col1:
            st.selectbox("Property Style", [
                "Detached", "Semi-detached", "Terraced", "End of Terrace", 
                "Apartment", "Duplex", "Penthouse", "Studio"
            ], key="property_style")
        with col2:
            st.selectbox("BER Rating", [
                "A1", "A2", "A3", "B1", "B2", "B3", "C1", "C2", "C3", 
                "D1", "D2", "E1", "E2", "F", "G", "Exempt"
            ], key="property_ber")
        
        st.button("Continue to Next Step", key="property_details_continue")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        st.markdown('<div class="form-container">', unsafe_allow_html=True)
        st.markdown('<h3>Property Description</h3>', unsafe_allow_html=True)
        
        st.text_area("Property Title", height=60, placeholder="e.g. Spacious 3-bed family home in Dublin 6", key="property_title")
        st.text_area("Property Description", height=200, placeholder="Describe your property in detail...", key="property_description")
        
        st.markdown('<h3>Features & Amenities</h3>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown('<p style="font-weight: bold;">Interior Features</p>', unsafe_allow_html=True)
            st.checkbox("Central Heating", key="feature_heating")
            st.checkbox("Alarm System", key="feature_alarm")
            st.checkbox("Double Glazing", key="feature_glazing")
            st.checkbox("Open Fireplace", key="feature_fireplace")
            st.checkbox("Fitted Kitchen", key="feature_kitchen")
            st.checkbox("Utility Room", key="feature_utility")
        
        with col2:
            st.markdown('<p style="font-weight: bold;">Exterior Features</p>', unsafe_allow_html=True)
            st.checkbox("Garden", key="feature_garden")
            st.checkbox("Patio/Deck", key="feature_patio")
            st.checkbox("Parking", key="feature_parking")
            st.checkbox("Garage", key="feature_garage")
            st.checkbox("South-facing", key="feature_south_facing")
            st.checkbox("Sea View", key="feature_sea_view")
        
        with col3:
            st.markdown('<p style="font-weight: bold;">Additional Features</p>', unsafe_allow_html=True)
            st.checkbox("Recently Renovated", key="feature_renovated")
            st.checkbox("En-suite Bathroom", key="feature_ensuite")
            st.checkbox("Home Office", key="feature_office")
            st.checkbox("Close to Schools", key="feature_schools")
            st.checkbox("Close to Transport", key="feature_transport")
            st.checkbox("Balcony/Terrace", key="feature_balcony")
        
        st.text_area("Additional Features", placeholder="Any other features not listed above...", key="feature_additional")
        
        st.button("Continue to Next Step", key="property_features_continue")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab3:
        st.markdown('<div class="form-container">', unsafe_allow_html=True)
        st.markdown('<h3>Property Photos</h3>', unsafe_allow_html=True)
        
        st.markdown('''
        <p>High-quality photos significantly increase interest in your property. We recommend uploading:</p>
        <ul>
            <li>Exterior shots (front, back, garden)</li>
            <li>All major rooms (living areas, kitchen, bedrooms, bathrooms)</li>
            <li>Special features or selling points</li>
        </ul>
        <p>Minimum 5 photos recommended. Maximum 20 photos.</p>
        ''', unsafe_allow_html=True)
        
        st.file_uploader("Upload Photos", accept_multiple_files=True, type=["jpg", "jpeg", "png"], key="property_photos")
        
        st.markdown('<h3>Floor Plans & Documents</h3>', unsafe_allow_html=True)
        
        st.markdown('''
        <p>Upload your floor plan and any relevant property documents:</p>
        <ul>
            <li>Floor plans</li>
            <li>BER certificate</li>
            <li>Property details/brochure</li>
            <li>Planning permissions (if applicable)</li>
        </ul>
        ''', unsafe_allow_html=True)
        
        st.file_uploader("Upload Floor Plan", type=["jpg", "jpeg", "png", "pdf"], key="property_floorplan")
        st.file_uploader("Upload BER Certificate", type=["jpg", "jpeg", "png", "pdf"], key="property_ber_cert")
        st.file_uploader("Upload Additional Documents", accept_multiple_files=True, type=["jpg", "jpeg", "png", "pdf"], key="property_documents")
        
        st.button("Continue to Next Step", key="property_photos_continue")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab4:
        st.markdown('<div class="form-container">', unsafe_allow_html=True)
        st.markdown('<h3>Pricing Your Property</h3>', unsafe_allow_html=True)
        
        # AI-powered pricing recommendation
        st.markdown('''
        <div style="background-color: #d4edda; padding: 15px; border-radius: 5px; margin-bottom: 20px;">
            <p style="font-weight: bold; margin-bottom: 5px;">AI Price Recommendation</p>
            <p>Based on similar properties in your area, we recommend a price range of <strong>€580,000 - €620,000</strong>.</p>
            <p style="font-size: 12px; margin-top: 5px;">This is based on recent sales data, your property specifications, and current market conditions.</p>
        </div>
        ''', unsafe_allow_html=True)
        
        st.number_input("Asking Price (€)", min_value=50000, max_value=10000000, value=595000, step=5000, key="property_price")
        
        st.markdown('<h3>Viewing Availability</h3>', unsafe_allow_html=True)
        
        st.markdown('<p>When are you typically available for property viewings?</p>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.checkbox("Weekday Mornings", key="viewing_weekday_am")
            st.checkbox("Weekday Afternoons", key="viewing_weekday_pm")
            st.checkbox("Weekday Evenings", key="viewing_weekday_eve")
        
        with col2:
            st.checkbox("Saturday Morning", key="viewing_saturday_am")
            st.checkbox("Saturday Afternoon", key="viewing_saturday_pm")
            st.checkbox("Saturday Evening", key="viewing_saturday_eve")
        
        with col3:
            st.checkbox("Sunday Morning", key="viewing_sunday_am")
            st.checkbox("Sunday Afternoon", key="viewing_sunday_pm")
            st.checkbox("Sunday Evening", key="viewing_sunday_eve")
        
        st.markdown('<h3>Property Availability</h3>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.selectbox("When is the property available for sale?", [
                "Immediately", "Within 1 month", "Within 3 months", "Specific date"
            ], key="property_availability")
        
        with col2:
            st.date_input("Specific availability date", value=None, key="property_availability_date", disabled=True)
        
        st.button("Continue to Final Step", key="property_pricing_continue")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab5:
        st.markdown('<div class="form-container">', unsafe_allow_html=True)
        st.markdown('<h3>Review Your Listing</h3>', unsafe_allow_html=True)
        
        st.markdown('''
        <div style="background-color: #f8f9fa; padding: 20px; border-radius: 5px; margin-bottom: 20px;">
            <h4>Property Summary</h4>
            <p><strong>Address:</strong> 15 Claremont Road, Dublin 6</p>
            <p><strong>Type:</strong> Semi-detached House, 3 bed, 2 bath, 120 m²</p>
            <p><strong>BER Rating:</strong> B2</p>
            <p><strong>Price:</strong> €595,000</p>
            <p><strong>Key Features:</strong> Garden, Parking, Recently Renovated, Central Heating, Double Glazing</p>
        </div>
        ''', unsafe_allow_html=True)
        
        st.markdown('<h3>Service Fee</h3>', unsafe_allow_html=True)
        
        st.markdown('''
        <div style="border: 1px solid #ddd; padding: 20px; border-radius: 5px; margin-bottom: 20px;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                <span>Flat Listing Fee</span>
                <span>€1,500</span>
            </div>
            <div style="display: flex; justify-content: space-between; font-weight: bold; margin-top: 10px; padding-top: 10px; border-top: 1px solid #ddd;">
                <span>Total Due Now</span>
                <span>€1,500</span>
            </div>
            <p style="font-size: 12px; color: #666; margin-top: 10px;">This is a one-time fee. No commission or additional charges.</p>
        </div>
        ''', unsafe_allow_html=True)
        
        st.checkbox("I confirm that I am the owner or have the legal right to sell this property", key="property_confirmation")
        st.checkbox("I agree to the Terms of Service and Privacy Policy", key="property_terms")
        
        st.markdown('<h3>Payment Details</h3>', unsafe_allow_html=True)
        
        payment_method = st.radio("Select Payment Method", ["Credit/Debit Card", "Bank Transfer"], key="payment_method")
        
        if payment_method == "Credit/Debit Card":
            col1, col2 = st.columns(2)
            with col1:
                st.text_input("Card Number", key="card_number")
                st.text_input("Cardholder Name", key="card_name")
            with col2:
                st.text_input("Expiry Date (MM/YY)", key="card_expiry")
                st.text_input("CVC", key="card_cvc", type="password")
        else:
            st.markdown('''
            <div style="background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin-bottom: 20px;">
                <p><strong>Bank Transfer Details:</strong></p>
                <p>Account Name: RealEstateIreland.ie Ltd</p>
                <p>IBAN: IE29AIBK93115212345678</p>
                <p>Bank: AIB, College Green, Dublin 2</p>
                <p>Reference: Please use your email address as the payment reference</p>
            </div>
            ''', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.button("Save as Draft", key="property_save_draft")
        with col2:
            st.button("Submit & Pay", key="property_submit", type="primary")
        
        st.markdown('</div>', unsafe_allow_html=True)

# =========================================
# PAGE COMPONENTS - AUTHENTICATION
# =========================================

# Login form
def render_login():
    st.markdown('<p class="main-header">Sign In</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown('<div class="form-container">', unsafe_allow_html=True)
        
        st.text_input("Email", key="login_email")
        st.text_input("Password", type="password", key="login_password")
        
        col1, col2 = st.columns(2)
        with col1:
            st.checkbox("Remember me", key="login_remember")
        with col2:
            st.markdown('<p style="text-align: right;"><a href="#" style="color: #2E7D67;">Forgot Password?</a></p>', unsafe_allow_html=True)
        
        if st.button("Sign In", key="login_button", type="primary"):
            # Demo login (in real app, this would check credentials against a database)
            if st.session_state.login_email and st.session_state.login_password:
                st.session_state.logged_in = True
                st.session_state.username = st.session_state.login_email.split('@')[0]
                st.session_state.user_type = "seller"  # For demo, assume seller
                st.experimental_rerun()
        
        st.markdown('<p style="text-align: center; margin-top: 20px;">Don\'t have an account? <a href="#" style="color: #2E7D67;">Sign Up</a></p>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('''
        <div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; height: 100%;">
            <h3>Welcome Back!</h3>
            <p>Sign in to access your dashboard, manage your property listings, or continue your property search.</p>
            
            <h4 style="margin-top: 30px;">Benefits of Your Account:</h4>
            <ul>
                <li>Track your property listing performance</li>
                <li>Manage property viewings and offers</li>
                <li>Communicate directly with buyers or sellers</li>
                <li>Save your favorite properties</li>
                <li>Set up property alerts</li>
            </ul>
        </div>
        ''', unsafe_allow_html=True)

# Registration form
def render_register():
    st.markdown('<p class="main-header">Create an Account</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown('<div class="form-container">', unsafe_allow_html=True)
        
        st.radio("I am a:", ["Seller", "Buyer", "Both"], key="register_type")
        
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("First Name", key="register_first_name")
        with col2:
            st.text_input("Last Name", key="register_last_name")
        
        st.text_input("Email", key="register_email")
        st.text_input("Phone Number", key="register_phone")
        
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("Password", type="password", key="register_password")
        with col2:
            st.text_input("Confirm Password", type="password", key="register_password_confirm")
        
        st.checkbox("I agree to the Terms of Service and Privacy Policy", key="register_terms")
        
        if st.button("Create Account", key="register_button", type="primary"):
            # Demo registration (in real app, this would save to a database)
            if (st.session_state.register_first_name and st.session_state.register_email and 
                st.session_state.register_password and st.session_state.register_password_confirm and 
                st.session_state.register_terms):
                
                if st.session_state.register_password == st.session_state.register_password_confirm:
                    st.session_state.logged_in = True
                    st.session_state.username = st.session_state.register_first_name
                    st.session_state.user_type = st.session_state.register_type.lower()
                    st.experimental_rerun()
                else:
                    st.error("Passwords do not match.")
            else:
                st.error("Please fill in all required fields and accept the terms.")
        
        st.markdown('<p style="text-align: center; margin-top: 20px;">Already have an account? <a href="#" style="color: #2E7D67;">Sign In</a></p>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('''
        <div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; height: 100%;">
            <h3>Join RealEstateIreland.ie</h3>
            <p>Create an account to start your property journey with us.</p>
            
            <h4 style="margin-top: 30px;">As a Seller, You Can:</h4>
            <ul>
                <li>List your property for a flat fee of €1,500</li>
                <li>Save thousands compared to traditional agents</li>
                <li>Manage viewings and offers through our platform</li>
                <li>Complete legal processes efficiently</li>
            </ul>
            
            <h4 style="margin-top: 20px;">As a Buyer, You Can:</h4>
            <ul>
                <li>Browse properties with detailed information</li>
                <li>Schedule viewings directly with sellers</li>
                <li>Make secure, legally-binding offers</li>
                <li>Track your purchase progress in real-time</li>
            </ul>
        </div>
        ''', unsafe_allow_html=True)

# =========================================
# PAGE COMPONENTS - PROPERTY DETAILS
# =========================================

# Property details page
def render_property_details():
    # For demo, use the first property in the dataset
    property = st.session_state.property_data.iloc[0]
    
    st.markdown(f'<p class="main-header">{property["address"]}</p>', unsafe_allow_html=True)
    
    # Property overview
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('''
        <div style="height: 400px; background-color: #eee; border-radius: 5px; display: flex; align-items: center; justify-content: center;">
            <span style="color: #999;">Property Image Gallery</span>
        </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        features_str = ", ".join(property['features']) if len(property['features']) > 0 else ""
        
        st.markdown(f'''
        <div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; height: 100%;">
            <p class="property-price">€{property['price']:,}</p>
            <p>{property['bedrooms']} bed • {property['bathrooms']} bath • {property['size_sqm']} m²</p>
            <p>{property['type']} • BER: {property['ber_rating']}</p>
            <p>Listed: {property['listed_date']}</p>
            
            <div style="margin-top: 20px;">
                <a href="#" class="btn-primary" style="width: 100%; display: block; text-align: center; margin-bottom: 10px;">Request Viewing</a>
                <a href="#" class="btn-secondary" style="width: 100%; display: block; text-align: center; margin-bottom: 10px;">Make Offer</a>
                <a href="#" class="btn-secondary" style="width: 100%; display: block; text-align: center; background-color: white;">Save Property</a>
            </div>
        </div>
        ''', unsafe_allow_html=True)
    
    # Property details tabs
    tab1, tab2, tab3, tab4 = st.tabs(["Description", "Features", "Map & Location", "Legal & BER"])
    
    with tab1:
        st.markdown(f'''
        <div style="padding: 20px;">
            <h3>About This Property</h3>
            <p>{property['description']}</p>
            
            <h3 style="margin-top: 30px;">Key Information</h3>
            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-top: 20px;">
                <div>
                    <p style="font-weight: bold;">Property Type</p>
                    <p>{property['type']}</p>
                </div>
                <div>
                    <p style="font-weight: bold;">Floor Area</p>
                    <p>{property['size_sqm']} m²</p>
                </div>
                <div>
                    <p style="font-weight: bold;">BER Rating</p>
                    <p>{property['ber_rating']}</p>
                </div>
                <div>
                    <p style="font-weight: bold;">Year Built</p>
                    <p>2005 (approx.)</p>
                </div>
                <div>
                    <p style="font-weight: bold;">Heating System</p>
                    <p>Gas Central Heating</p>
                </div>
                <div>
                    <p style="font-weight: bold;">Garden Size</p>
                    <p>50 m² (approx.)</p>
                </div>
            </div>
        </div>
        ''', unsafe_allow_html=True)
    
    with tab2:
        st.markdown('''
        <div style="padding: 20px;">
            <h3>Property Features</h3>
            
            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 30px; margin-top: 20px;">
                <div>
                    <h4>Interior</h4>
                    <ul>
                        <li>Central Heating</li>
                        <li>Double Glazing</li>
                        <li>Fitted Kitchen</li>
                        <li>Utility Room</li>
                        <li>Wooden Flooring</li>
                        <li>Alarm System</li>
                    </ul>
                </div>
                <div>
                    <h4>Exterior</h4>
                    <ul>
                        <li>Garden</li>
                        <li>Patio Area</li>
                        <li>Off-street Parking</li>
                        <li>South-facing Rear</li>
                        <li>Brick Façade</li>
                        <li>Gated Entrance</li>
                    </ul>
                </div>
                <div>
                    <h4>Additional</h4>
                    <ul>
                        <li>Recently Renovated</li>
                        <li>En-suite in Master Bedroom</li>
                        <li>Close to Schools</li>
                        <li>Close to Transport</li>
                        <li>Shopping Nearby</li>
                        <li>Quiet Neighborhood</li>
                    </ul>
                </div>
            </div>
            
            <h3 style="margin-top: 30px;">Room Dimensions</h3>
            <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; margin-top: 20px;">
                <div>
                    <p style="font-weight: bold;">Living Room</p>
                    <p>4.5m x 3.8m</p>
                </div>
                <div>
                    <p style="font-weight: bold;">Kitchen/Dining</p>
                    <p>6.2m x 3.5m</p>
                </div>
                <div>
                    <p style="font-weight: bold;">Master Bedroom</p>
                    <p>4.2m x 3.6m</p>
                </div>
                <div>
                    <p style="font-weight: bold;">Bedroom 2</p>
                    <p>3.8m x 3.2m</p>
                </div>
                <div>
                    <p style="font-weight: bold;">Bedroom 3</p>
                    <p>3.5m x 2.8m</p>
                </div>
                <div>
                    <p style="font-weight: bold;">Bathroom</p>
                    <p>2.5m x 1.8m</p>
                </div>
            </div>
        </div>
        ''', unsafe_allow_html=True)
    
    with tab3:
        # Use property coordinates for map
        m = folium.Map(location=[property['lat'], property['lng']], zoom_start=15)
        
        # Add property marker
        folium.Marker(
            location=[property['lat'], property['lng']],
            popup=property['address'],
            icon=folium.Icon(color='green', icon='home')
        ).add_to(m)
        
        # Display map
        st.markdown('<h3>Property Location</h3>', unsafe_allow_html=True)
        folium_static(m, width=800, height=400)
        
        # Local amenities
        st.markdown('''
        <h3 style="margin-top: 30px;">Local Amenities</h3>
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-top: 20px;">
            <div>
                <p style="font-weight: bold;">Education</p>
                <ul>
                    <li>St. Mary's Primary School (0.4 km)</li>
                    <li>Oakwood Secondary School (1.2 km)</li>
                    <li>Little Stars Childcare (0.6 km)</li>
                </ul>
            </div>
            <div>
                <p style="font-weight: bold;">Transport</p>
                <ul>
                    <li>Bus Stop (0.2 km)</li>
                    <li>Train Station (1.5 km)</li>
                    <li>M50 Motorway (3.2 km)</li>
                </ul>
            </div>
            <div>
                <p style="font-weight: bold;">Amenities</p>
                <ul>
                    <li>Local Shopping Centre (0.8 km)</li>
                    <li>Riverside Park (0.5 km)</li>
                    <li>Medical Centre (1.0 km)</li>
                </ul>
            </div>
        </div>
        ''', unsafe_allow_html=True)
    
    with tab4:
        st.markdown('''
        <div style="padding: 20px;">
            <h3>BER Information</h3>
            <div style="display: flex; align-items: center; margin-top: 20px; margin-bottom: 30px;">
                <div style="background-color: #2E7D67; color: white; padding: 10px 20px; font-size: 24px; font-weight: bold; border-radius: 5px;">
                    B2
                </div>
                <div style="margin-left: 20px;">
                    <p style="margin: 0;">Energy Performance Indicator: <strong>125.7 kWh/m²/yr</strong></p>
                    <p style="margin: 0;">BER Number: <strong>105827392</strong></p>
                    <p style="margin: 0;">Valid until: <strong>May 2030</strong></p>
                </div>
            </div>
            
            <h3 style="margin-top: 30px;">Legal Information</h3>
            <div style="margin-top: 20px;">
                <p style="font-weight: bold;">Property Title</p>
                <p>Freehold</p>
                
                <p style="font-weight: bold; margin-top: 15px;">Planning Permission</p>
                <p>All extensions and modifications have appropriate planning permission (documentation available upon request)</p>
                
                <p style="font-weight: bold; margin-top: 15px;">Property Tax</p>
                <p>Local Property Tax Band: €315 per annum</p>
                
                <p style="font-weight: bold; margin-top: 15px;">Management Fees</p>
                <p>Not applicable for this property</p>
            </div>
            
            <h3 style="margin-top: 30px;">Purchase Process</h3>
            <div style="background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin-top: 20px;">
                <p>When you make an offer through RealEstateIreland.ie:</p>
                <ol>
                    <li>Your offer becomes legally binding once accepted</li>
                    <li>You'll place a 10% deposit in our secure escrow account</li>
                    <li>Our partner solicitors will handle all legal aspects of the transfer</li>
                    <li>You can track all stages of the process through your dashboard</li>
                </ol>
                <p style="margin-top: 15px;"><a href="#" style="color: #2E7D67;">Learn more about our secure purchase process</a></p>
            </div>
        </div>
        ''', unsafe_allow_html=True)
    
    # Seller information and similar properties
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<h3>Similar Properties</h3>', unsafe_allow_html=True)
        
        # Create a row of similar properties
        cols = st.columns(3)
        
        # Get 3 random properties of the same type for "similar properties"
        similar_properties = st.session_state.property_data[st.session_state.property_data['type'] == property['type']].sample(min(3, len(st.session_state.property_data)))
        
        for i, (col, prop) in enumerate(zip(cols, similar_properties.iterrows())):
            with col:
                prop = prop[1]  # Get the Series from the tuple
                st.markdown(f"""
                <div class="property-card">
                    <div class="property-image" style="background-color: #eee; display: flex; align-items: center; justify-content: center; height: 120px;">
                        <span style="color: #999;">Property Image</span>
                    </div>
                    <div class="property-details">
                        <p class="property-price">€{prop['price']:,}</p>
                        <p>{prop['bedrooms']} bed • {prop['type']}</p>
                        <p>{prop['address']}</p>
                        <a href="#" class="btn-secondary" style="width: 100%; display: block; text-align: center; margin-top: 10px;">View Details</a>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f'''
        <div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px;">
            <h3>Contact the Seller</h3>
            <div style="display: flex; align-items: center; margin-bottom: 15px;">
                <div style="width: 50px; height: 50px; border-radius: 50%; background-color: #2E7D67; color: white; display: flex; align-items: center; justify-content: center; font-weight: bold; margin-right: 15px;">
                    J
                </div>
                <div>
                    <p style="margin: 0; font-weight: bold;">John D.</p>
                    <p style="margin: 0; color: #666;">Property Owner</p>
                </div>
            </div>
            
            <div style="margin-top: 20px;">
                <textarea placeholder="Write a message to the seller..." style="width: 100%; height: 100px; padding: 10px; border-radius: 5px; border: 1px solid #ddd; margin-bottom: 10px;"></textarea>
                <a href="#" class="btn-primary" style="width: 100%; display: block; text-align: center;">Send Message</a>
            </div>
        </div>
        ''', unsafe_allow_html=True)

# =========================================
# MAIN APP
# =========================================

def main():
    # Initialize session state
    init_session_state()
    
    # Load CSS
    load_css()
    
    # Render top navigation
    render_top_navigation()
    
    # Sidebar navigation
    with st.sidebar:
        if st.session_state.logged_in:
            # Show user-specific dashboard options
            if st.session_state.user_type == "seller":
                selected = option_menu(
                    "Dashboard",
                    ["My Listings", "Analytics", "Offers", "Messages", "Documents", "Account"],
                    icons=["house", "graph-up", "cash", "chat", "file-text", "person"],
                    menu_icon="speedometer",
                    default_index=0
                )
                
                # Show logout button
                if st.button("Log Out", key="logout_btn"):
                    st.session_state.logged_in = False
                    st.session_state.username = ""
                    st.session_state.user_type = ""
                    st.experimental_rerun()
            
            elif st.session_state.user_type == "buyer":
                selected = option_menu(
                    "Dashboard",
                    ["Saved Properties", "My Offers", "Viewings", "Messages", "Account"],
                    icons=["heart", "cash", "calendar", "chat", "person"],
                    menu_icon="speedometer",
                    default_index=0
                )
                
                # Show logout button
                if st.button("Log Out", key="logout_btn"):
                    st.session_state.logged_in = False
                    st.session_state.username = ""
                    st.session_state.user_type = ""
                    st.experimental_rerun()
        else:
            # Show general navigation
            selected = option_menu(
                "Navigation",
                ["Home", "Properties", "How It Works", "About Us", "Contact", "Login", "Register"],
                icons=["house", "search", "info-circle", "building", "envelope", "box-arrow-in-right", "person-plus"],
                menu_icon="list",
                default_index=0
            )
    
    # Main content area
    if st.session_state.logged_in:
        # Render user dashboard based on type
        if st.session_state.user_type == "seller":
            if selected == "My Listings":
                st.markdown('<p class="main-header">My Property Listings</p>', unsafe_allow_html=True)
                render_property_listing()
            elif selected == "Analytics":
                st.markdown('<p class="main-header">Listing Analytics</p>', unsafe_allow_html=True)
                render_seller_analytics()
            elif selected == "Offers":
                st.markdown('<p class="main-header">Offers Received</p>', unsafe_allow_html=True)
                render_seller_offers()
                render_sale_timeline()
            elif selected == "Messages":
                st.markdown('<p class="main-header">Messages</p>', unsafe_allow_html=True)
                render_messaging()
            elif selected == "Documents":
                st.markdown('<p class="main-header">Legal Documents</p>', unsafe_allow_html=True)
                st.write("Document management interface coming soon.")
            elif selected == "Account":
                st.markdown('<p class="main-header">Account Settings</p>', unsafe_allow_html=True)
                st.write("Account settings interface coming soon.")
        
        elif st.session_state.user_type == "buyer":
            if selected == "Saved Properties":
                st.markdown('<p class="main-header">Saved Properties</p>', unsafe_allow_html=True)
                render_buyer_saved_properties()
                render_buyer_saved_searches()
            elif selected == "My Offers":
                st.markdown('<p class="main-header">My Offers</p>', unsafe_allow_html=True)
                render_buyer_offers()
            elif selected == "Viewings":
                st.markdown('<p class="main-header">My Viewings</p>', unsafe_allow_html=True)
                st.write("Viewing management interface coming soon.")
            elif selected == "Messages":
                st.markdown('<p class="main-header">Messages</p>', unsafe_allow_html=True)
                render_messaging()
            elif selected == "Account":
                st.markdown('<p class="main-header">Account Settings</p>', unsafe_allow_html=True)
                st.write("Account settings interface coming soon.")
    
    else:
        # Render general pages
        if selected == "Home":
            render_home_hero()
            render_how_it_works_short()
            render_why_choose_us()
            render_featured_properties()
            render_market_statistics()
        
        elif selected == "Properties":
            render_search_filters()
            tab1, tab2 = st.tabs(["List View", "Map View"])
            with tab1:
                render_search_results()
            with tab2:
                render_property_map()
        
        elif selected == "How It Works":
            render_process_steps()
            render_benefits_comparison()
            render_testimonials()
            render_faq()
        
        elif selected == "About Us":
            render_company_story()
            render_team()
            render_press()
        
        elif selected == "Contact":
            render_contact_form()
        
        elif selected == "Login":
            render_login()
        
        elif selected == "Register":
            render_register()
    
    # Footer
    render_footer()

if __name__ == "__main__":
    main()
