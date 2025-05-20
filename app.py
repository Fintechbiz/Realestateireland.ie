import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import re
from PIL import Image
import io
import base64

# Set page configuration
st.set_page_config(
    page_title="RealEstateIreland.ie",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS to match the modern design
def local_css():
    st.markdown("""
    <style>
        /* Main theme colors */
        :root {
            --primary: #2A7A78;
            --secondary: #264653;
            --light: #f8f9fa;
            --dark: #31373f;
            --success: #28a745;
            --info: #17a2b8;
            --warning: #ffc107;
            --danger: #dc3545;
        }
        
        /* Global styles */
        body {
            font-family: 'Open Sans', sans-serif;
            color: #31373f;
            background-color: white;
        }
        
        /* Header styling */
        .main-header {
            color: var(--secondary);
            font-size: 3rem;
            font-weight: 700;
            margin-bottom: 1rem;
        }
        
        .sub-header {
            color: var(--secondary);
            font-size: 2rem;
            font-weight: 600;
            margin-bottom: 1rem;
            padding-top: 1.5rem;
        }
        
        /* Navigation and header */
        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 1rem 0;
            margin-bottom: 2rem;
        }
        
        .logo {
            font-size: 1.5rem;
            font-weight: 700;
            color: var(--secondary);
        }
        
        .nav-menu {
            display: flex;
            gap: 2rem;
        }
        
        .nav-item {
            color: var(--secondary);
            font-weight: 600;
            text-decoration: none;
            font-size: 1.1rem;
        }
        
        /* Search section */
        .search-section {
            padding: 2rem 0;
            margin-bottom: 3rem;
        }
        
        .search-heading {
            font-size: 3rem;
            font-weight: 700;
            color: var(--secondary);
            margin-bottom: 1.5rem;
        }
        
        .search-container {
            display: flex;
            gap: 10px;
            margin-bottom: 1rem;
        }
        
        .search-dropdown {
            flex: 1;
            padding: 0.75rem;
            border: 1px solid #ddd;
            border-radius: 5px;
            background-color: white;
            font-size: 1rem;
        }
        
        .search-button {
            background-color: var(--primary);
            color: white;
            border: none;
            border-radius: 5px;
            padding: 0.75rem 2rem;
            font-weight: 600;
            font-size: 1.1rem;
            cursor: pointer;
            width: 100%;
        }
        
        /* Property cards */
        .property-section {
            margin-bottom: 3rem;
        }
        
        .property-heading {
            font-size: 2rem;
            font-weight: 700;
            color: var(--secondary);
            margin-bottom: 1.5rem;
        }
        
        .property-card {
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        
        .property-image {
            width: 100%;
            height: 200px;
            object-fit: cover;
        }
        
        .property-details {
            padding: 1rem;
        }
        
        .property-price {
            font-size: 1.5rem;
            font-weight: 700;
            color: var(--secondary);
            margin-bottom: 0.25rem;
        }
        
        .property-location {
            font-size: 1.2rem;
            color: #666;
        }
        
        /* Features section */
        .feature-section {
            background-color: #f9f9f9;
            padding: 3rem 0;
            margin-bottom: 3rem;
        }
        
        .feature-heading {
            font-size: 2rem;
            font-weight: 700;
            color: var(--secondary);
            margin-bottom: 1rem;
        }
        
        .feature-subheading {
            font-size: 1.2rem;
            color: #666;
            margin-bottom: 2rem;
        }
        
        .feature-icon {
            font-size: 2.5rem;
            color: var(--primary);
            margin-bottom: 1rem;
        }
        
        /* Testimonial section */
        .testimonial-section {
            margin-bottom: 3rem;
        }
        
        .testimonial-container {
            background-color: #f9f9f9;
            padding: 2rem;
            border-radius: 10px;
        }
        
        .testimonial-text {
            font-size: 1.2rem;
            font-style: italic;
            margin-bottom: 1rem;
        }
        
        .testimonial-author {
            font-weight: 600;
            color: var(--secondary);
        }
        
        /* Custom button */
        .custom-button {
            background-color: var(--primary);
            color: white;
            border: none;
            border-radius: 5px;
            padding: 0.75rem 1.5rem;
            font-weight: 600;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }
        
        .custom-button:hover {
            background-color: #236361;
        }
        
        /* Footer */
        .footer {
            background-color: var(--secondary);
            color: white;
            padding: 2rem 0;
            margin-top: 3rem;
        }
        
        /* Remove default Streamlit styling */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        .viewerBadge_container__1QSob {visibility: hidden;}
        
        .stApp {
            max-width: 1200px;
            margin: 0 auto;
        }
        
        /* Ireland map styling */
        .ireland-map {
            max-width: 100%;
            height: auto;
        }
    </style>
    """, unsafe_allow_html=True)

local_css()

# Function to create a navigation bar
def create_header():
    st.markdown("""
    <div class="header">
        <div class="logo">
            <img src="https://raw.githubusercontent.com/yourusername/realestateireland/main/logo.png" alt="RealEstateIreland.ie Logo" style="height: 50px;">
            RealEstateIreland.ie
        </div>
        <div class="nav-menu">
            <a href="#" class="nav-item">Buy</a>
            <a href="#" class="nav-item">Sell</a>
            <a href="#" class="nav-item">How It Works</a>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Function to create the search section
def create_search_section():
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown("""
        <div class="search-section">
            <h1 class="search-heading">Find your new home</h1>
            <div class="search-container">
                <select class="search-dropdown">
                    <option selected disabled>Price</option>
                    <option>€100,000 - €200,000</option>
                    <option>€200,000 - €300,000</option>
                    <option>€300,000 - €400,000</option>
                    <option>€400,000 - €500,000</option>
                    <option>€500,000+</option>
                </select>
                <select class="search-dropdown">
                    <option selected disabled>Location</option>
                    <option>Dublin</option>
                    <option>Cork</option>
                    <option>Galway</option>
                    <option>Limerick</option>
                    <option>Waterford</option>
                </select>
                <select class="search-dropdown">
                    <option selected disabled>Property-type</option>
                    <option>House</option>
                    <option>Apartment</option>
                    <option>Bungalow</option>
                    <option>Duplex</option>
                    <option>Land</option>
                </select>
            </div>
            <button class="search-button">Search</button>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Ireland map image
        st.markdown("""
        <img src="https://raw.githubusercontent.com/jkunst/d3-ireland-map/master/data/ireland.svg" alt="Map of Ireland" class="ireland-map">
        """, unsafe_allow_html=True)

# Function to display featured properties
def featured_properties():
    st.markdown("""
    <h2 class="property-heading">Featured Properties</h2>
    """, unsafe_allow_html=True)
    
    # Featured properties grid
    col1, col2, col3, col4 = st.columns(4)
    
    property_data = [
        {
            "image": "https://images.unsplash.com/photo-1564013799919-ab600027ffc6?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80",
            "price": "€450,000",
            "location": "Ausland"
        },
        {
            "image": "https://images.unsplash.com/photo-1570129477492-45c003edd2be?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80",
            "price": "€375,000",
            "location": "Huntavv"
        },
        {
            "image": "https://images.unsplash.com/photo-1576941089067-2de3c901e126?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80",
            "price": "€520,000",
            "location": "Landhaus"
        },
        {
            "image": "https://images.unsplash.com/photo-1568605114967-8130f3a36994?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80",
            "price": "€610,000",
            "location": "Greinhain"
        }
    ]
    
    columns = [col1, col2, col3, col4]
    
    for i, prop in enumerate(property_data):
        with columns[i]:
            st.markdown(f"""
            <div class="property-card">
                <img src="{prop['image']}" alt="Property" class="property-image">
                <div class="property-details">
                    <div class="property-price">{prop['price']}</div>
                    <div class="property-location">{prop['location']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

# Function to display pricing section
def pricing_section():
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div>
            <h2 class="feature-heading">Simple, flat-fee pricing</h2>
            <p class="feature-subheading">No commissions, no hidden costs — just one transparent price.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Testimonial
        st.markdown("""
        <div class="testimonial-container">
            <img src="https://randomuser.me/api/portraits/men/32.jpg" alt="Customer" style="width: 80px; height: 80px; border-radius: 50%; margin-bottom: 1rem;">
            <div class="testimonial-text">"Selling my home was completely hassle-free."</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Euro symbol and second testimonial
        col2a, col2b = st.columns([1, 2])
        
        with col2a:
            st.markdown("""
            <div style="display: flex; justify-content: center; align-items: center; height: 100%;">
                <div style="width: 100px; height: 100px; border-radius: 50%; border: 3px solid var(--primary); display: flex; justify-content: center; align-items: center;">
                    <span style="font-size: 3rem; color: var(--primary);">€</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2b:
            st.markdown("""
            <div class="testimonial-container">
                <div class="testimonial-text">"Selling my home was completely hassle-free. Highly recommended!"</div>
                <div class="testimonial-author">John Doe</div>
            </div>
            """, unsafe_allow_html=True)

# Function to display security features
def security_section():
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.markdown("""
        <div style="display: flex; justify-content: center; align-items: center; height: 100%;">
            <div style="width: 100px; height: 100px; border-radius: 50%; border: 3px solid var(--primary); display: flex; justify-content: center; align-items: center;">
                <span style="font-size: 3rem; color: var(--primary);">✓</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <h2 class="feature-heading">Secure and legal transactions</h2>
        <p class="feature-subheading">All properties are verified and transactions are protected by our secure escrow system.</p>
        """, unsafe_allow_html=True)

# Main app function
def main():
    # Header with navigation
    create_header()
    
    # Search section with map
    create_search_section()
    
    # Featured properties
    featured_properties()
    
    # Pricing section with testimonials
    pricing_section()
    
    # Security features
    security_section()

if __name__ == "__main__":
    main()
