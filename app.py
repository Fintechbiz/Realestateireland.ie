import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import base64
from io import BytesIO
import matplotlib.pyplot as plt
import plotly.express as px
import requests
from datetime import datetime

# Set page configuration
st.set_page_config(
    page_title="RealEstateIreland.ie",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Function to create a logo using svg - ensures high quality and consistent loading
def create_logo():
    return '''
    <svg width="180" height="60" viewBox="0 0 180 60" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M30.4 13.6L45.2 24.8V46.4H37.6V28.8H23.2V46.4H15.6V24.8L30.4 13.6Z" fill="#2A7A78"/>
        <path d="M47.2 22.8L30.4 10L13.6 22.8V48.4H25.2V30.8H35.6V48.4H47.2V22.8Z" stroke="#2A7A78" stroke-width="3"/>
        <path d="M65 15.6V43.6H60.4V24.8L53.6 26.9V22.9L64.4 19.2L65 15.6Z" fill="#2A7A78"/>
        <text x="70" y="30" font-family="Arial, sans-serif" font-size="16" font-weight="bold" fill="#2A7A78">RealEstate</text>
        <text x="70" y="46" font-family="Arial, sans-serif" font-size="16" font-weight="bold" fill="#2A7A78">Ireland.ie</text>
    </svg>
    '''

# Function to create ireland map svg
def create_ireland_map():
    return '''
    <svg width="300" height="400" viewBox="0 0 300 400" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M149.5 38C90 76 70 125 73 160C76 195 85.5 226 92 240.5C98.5 255 110 285 131 315.5C152 346 177 365.5 191 375C205 365.5 238 346 260 315.5C282 285 288 255 290 240.5C292 226 298 195 294 160C290 125 209 0 149.5 38Z" fill="#2A7A78" fill-opacity="0.8"/>
        <path d="M149.5 38C90 76 70 125 73 160C76 195 85.5 226 92 240.5C98.5 255 110 285 131 315.5C152 346 177 365.5 191 375C205 365.5 238 346 260 315.5C282 285 288 255 290 240.5C292 226 298 195 294 160C290 125 209 0 149.5 38Z" stroke="#2A7A78" stroke-opacity="0.4"/>
        <path d="M147 130.5C147 130.5 142 137 140.5 146C139 155 145.5 162 145.5 162" stroke="white" stroke-opacity="0.6"/>
        <path d="M170 120C170 120 180 126.5 183 133.5C186 140.5 186 148.5 186 148.5" stroke="white" stroke-opacity="0.6"/>
        <path d="M202 175.5C202 175.5 209 184 209 194C209 204 202 215 202 215" stroke="white" stroke-opacity="0.6"/>
        <path d="M173 230C173 230 179.5 240 180 247C180.5 254 178 261.5 178 261.5" stroke="white" stroke-opacity="0.6"/>
        <path d="M142 249.5C142 249.5 137.5 257.5 136 264C134.5 270.5 136 277.5 136 277.5" stroke="white" stroke-opacity="0.6"/>
        <path d="M117 220C117 220 111 226.5 108.5 235C106 243.5 108.5 251.5 108.5 251.5" stroke="white" stroke-opacity="0.6"/>
        <path d="M118 178C118 178 110.5 191.5 110.5 199C110.5 206.5 112.5 216 112.5 216" stroke="white" stroke-opacity="0.6"/>
    </svg>
    '''

# Custom CSS with careful attention to detail and consistency
def apply_custom_css():
    st.markdown("""
    <style>
        /* Import fonts for consistent typography */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        /* Reset and base styles */
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Inter', sans-serif;
        }
        
        /* Variables for consistent colors and measurements */
        :root {
            --primary: #2A7A78;
            --primary-light: rgba(42, 122, 120, 0.8);
            --primary-very-light: rgba(42, 122, 120, 0.1);
            --secondary: #264653;
            --dark-text: #31373f;
            --light-text: #6B7280;
            --light-bg: #F9FAFB;
            --white: #FFFFFF;
            --light-border: #E5E7EB;
            --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
            --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
            --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
            --spacing-xs: 0.25rem;
            --spacing-sm: 0.5rem;
            --spacing-md: 1rem;
            --spacing-lg: 1.5rem;
            --spacing-xl: 2rem;
            --spacing-2xl: 3rem;
            --radius-sm: 0.25rem;
            --radius-md: 0.375rem;
            --radius-lg: 0.5rem;
            --radius-xl: 1rem;
            --radius-full: 9999px;
            --container-width: 1200px;
        }
        
        /* Top-level container */
        .main {
            max-width: var(--container-width);
            margin: 0 auto;
            padding: 0 var(--spacing-xl);
        }
        
        /* Header styles */
        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: var(--spacing-lg) 0;
            margin-bottom: var(--spacing-xl);
        }
        
        .logo-container {
            display: flex;
            align-items: center;
        }
        
        .nav-container {
            display: flex;
            gap: var(--spacing-2xl);
        }
        
        .nav-link {
            color: var(--dark-text);
            font-weight: 600;
            font-size: 1.05rem;
            text-decoration: none;
            padding-bottom: var(--spacing-xs);
            border-bottom: 2px solid transparent;
            transition: border-color 0.2s ease;
        }
        
        .nav-link:hover {
            border-color: var(--primary);
            color: var(--primary);
        }
        
        /* Hero section styles */
        .hero-section {
            display: flex;
            align-items: flex-start;
            justify-content: space-between;
            gap: var(--spacing-xl);
            margin-bottom: var(--spacing-2xl);
        }
        
        .hero-content {
            flex: 3;
        }
        
        .hero-map {
            flex: 2;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        
        .hero-title {
            font-size: 2.5rem;
            font-weight: 700;
            color: var(--dark-text);
            margin-bottom: var(--spacing-xl);
            line-height: 1.2;
        }
        
        .search-container {
            display: flex;
            gap: var(--spacing-md);
            margin-bottom: var(--spacing-md);
        }
        
        .search-select {
            flex: 1;
            padding: var(--spacing-md);
            border: 1px solid var(--light-border);
            border-radius: var(--radius-md);
            background-color: var(--white);
            color: var(--dark-text);
            font-size: 1rem;
            -webkit-appearance: none;
            -moz-appearance: none;
            appearance: none;
            background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="%23666" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"></polyline></svg>');
            background-repeat: no-repeat;
            background-position: right 0.75rem center;
            background-size: 1rem;
            cursor: pointer;
        }
        
        .search-select:focus {
            outline: none;
            border-color: var(--primary);
            box-shadow: 0 0 0 3px rgba(42, 122, 120, 0.1);
        }
        
        .search-button {
            width: 100%;
            padding: var(--spacing-md);
            background-color: var(--primary);
            color: var(--white);
            border: none;
            border-radius: var(--radius-md);
            font-weight: 600;
            font-size: 1.05rem;
            cursor: pointer;
            transition: background-color 0.2s ease;
            text-align: center;
        }
        
        .search-button:hover {
            background-color: #236361;
        }
        
        /* Featured properties section */
        .section-title {
            font-size: 1.75rem;
            font-weight: 700;
            color: var(--dark-text);
            margin-bottom: var(--spacing-xl);
        }
        
        .properties-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: var(--spacing-lg);
            margin-bottom: var(--spacing-2xl);
        }
        
        .property-card {
            border-radius: var(--radius-lg);
            overflow: hidden;
            box-shadow: var(--shadow-md);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
            background-color: var(--white);
        }
        
        .property-card:hover {
            transform: translateY(-4px);
            box-shadow: var(--shadow-lg);
        }
        
        .property-image {
            width: 100%;
            height: 200px;
            object-fit: cover;
        }
        
        .property-details {
            padding: var(--spacing-md);
        }
        
        .property-price {
            font-size: 1.3rem;
            font-weight: 700;
            color: var(--dark-text);
            margin-bottom: var(--spacing-xs);
        }
        
        .property-location {
            font-size: 1.05rem;
            color: var(--light-text);
        }
        
        /* Pricing section */
        .pricing-section {
            display: flex;
            justify-content: space-between;
            margin-bottom: var(--spacing-2xl);
            gap: var(--spacing-xl);
        }
        
        .pricing-left {
            flex: 1;
        }
        
        .pricing-right {
            flex: 1;
            display: flex;
            gap: var(--spacing-md);
        }
        
        .pricing-title {
            font-size: 1.75rem;
            font-weight: 700;
            color: var(--dark-text);
            margin-bottom: var(--spacing-sm);
        }
        
        .pricing-subtitle {
            font-size: 1.05rem;
            color: var(--light-text);
            margin-bottom: var(--spacing-xl);
            line-height: 1.5;
        }
        
        .testimonial {
            background-color: var(--light-bg);
            padding: var(--spacing-lg);
            border-radius: var(--radius-lg);
        }
        
        .testimonial-with-image {
            display: flex;
            align-items: center;
            gap: var(--spacing-md);
        }
        
        .testimonial-image {
            width: 60px;
            height: 60px;
            border-radius: var(--radius-full);
            object-fit: cover;
        }
        
        .testimonial-content {
            flex: 1;
        }
        
        .testimonial-text {
            font-style: italic;
            margin-bottom: var(--spacing-sm);
            color: var(--dark-text);
            line-height: 1.5;
        }
        
        .testimonial-author {
            font-weight: 600;
            color: var(--dark-text);
        }
        
        .euro-circle {
            display: flex;
            justify-content: center;
            align-items: center;
            width: 80px;
            height: 80px;
            border-radius: var(--radius-full);
            border: 3px solid var(--primary);
            flex-shrink: 0;
        }
        
        .euro-symbol {
            font-size: 2.5rem;
            color: var(--primary);
            font-weight: 700;
        }
        
        /* Security section */
        .security-section {
            display: flex;
            align-items: center;
            gap: var(--spacing-xl);
            margin-bottom: var(--spacing-2xl);
        }
        
        .check-circle {
            display: flex;
            justify-content: center;
            align-items: center;
            width: 80px;
            height: 80px;
            border-radius: var(--radius-full);
            border: 3px solid var(--primary);
            flex-shrink: 0;
        }
        
        .check-symbol {
            font-size: 2.5rem;
            color: var(--primary);
            font-weight: 700;
        }
        
        .security-content {
            flex: 1;
        }
        
        /* Streamlit overrides - critical for consistent styling */
        .block-container {
            padding-top: 1rem !important;
            padding-bottom: 0 !important;
            max-width: 100% !important;
        }
        
        .main .block-container {
            padding-left: 0 !important;
            padding-right: 0 !important;
        }
        
        /* Hide Streamlit elements */
        .stApp header {
            display: none !important;
        }
        
        #MainMenu {
            visibility: hidden;
        }
        
        footer {
            visibility: hidden;
        }
        
        /* Ensure images resize properly on smaller screens */
        @media (max-width: 1000px) {
            .properties-grid {
                grid-template-columns: repeat(2, 1fr);
            }
            
            .hero-section, .pricing-section, .security-section {
                flex-direction: column;
            }
            
            .search-container {
                flex-direction: column;
            }
            
            .hero-map {
                display: none;
            }
        }
        
        @media (max-width: 600px) {
            .properties-grid {
                grid-template-columns: 1fr;
            }
            
            .pricing-right {
                flex-direction: column;
            }
            
            .header {
                flex-direction: column;
                gap: var(--spacing-lg);
            }
        }
    </style>
    """, unsafe_allow_html=True)

# Apply CSS
apply_custom_css()

def main():
    # Main container
    st.markdown('<div class="main">', unsafe_allow_html=True)
    
    # Header with navigation
    st.markdown(f"""
    <div class="header">
        <div class="logo-container">
            {create_logo()}
        </div>
        <div class="nav-container">
            <a href="#" class="nav-link">Buy</a>
            <a href="#" class="nav-link">Sell</a>
            <a href="#" class="nav-link">How It Works</a>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Hero section with search
    st.markdown(f"""
    <div class="hero-section">
        <div class="hero-content">
            <h1 class="hero-title">Find your new home</h1>
            <div class="search-container">
                <select class="search-select">
                    <option value="" disabled selected>Price</option>
                    <option value="100000-200000">€100,000 - €200,000</option>
                    <option value="200000-300000">€200,000 - €300,000</option>
                    <option value="300000-400000">€300,000 - €400,000</option>
                    <option value="400000-500000">€400,000 - €500,000</option>
                    <option value="500000+">€500,000+</option>
                </select>
                <select class="search-select">
                    <option value="" disabled selected>Location</option>
                    <option value="dublin">Dublin</option>
                    <option value="cork">Cork</option>
                    <option value="galway">Galway</option>
                    <option value="limerick">Limerick</option>
                    <option value="waterford">Waterford</option>
                    <option value="other">Other</option>
                </select>
                <select class="search-select">
                    <option value="" disabled selected>Property-type</option>
                    <option value="house">House</option>
                    <option value="apartment">Apartment</option>
                    <option value="bungalow">Bungalow</option>
                    <option value="duplex">Duplex</option>
                    <option value="site">Site</option>
                </select>
            </div>
            <div class="search-button">
                Search
            </div>
        </div>
        <div class="hero-map">
            {create_ireland_map()}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Featured properties
    st.markdown("""
    <h2 class="section-title">Featured Properties</h2>
    <div class="properties-grid">
        <div class="property-card">
            <img class="property-image" src="https://images.unsplash.com/photo-1564013799919-ab600027ffc6?w=800&auto=format&fit=crop" alt="House in Ausland">
            <div class="property-details">
                <div class="property-price">€450,000</div>
                <div class="property-location">Ausland</div>
            </div>
        </div>
        
        <div class="property-card">
            <img class="property-image" src="https://images.unsplash.com/photo-1570129477492-45c003edd2be?w=800&auto=format&fit=crop" alt="House in Huntavv">
            <div class="property-details">
                <div class="property-price">€375,000</div>
                <div class="property-location">Huntavv</div>
            </div>
        </div>
        
        <div class="property-card">
            <img class="property-image" src="https://images.unsplash.com/photo-1576941089067-2de3c901e126?w=800&auto=format&fit=crop" alt="House in Landhaus">
            <div class="property-details">
                <div class="property-price">€520,000</div>
                <div class="property-location">Landhaus</div>
            </div>
        </div>
        
        <div class="property-card">
            <img class="property-image" src="https://images.unsplash.com/photo-1568605114967-8130f3a36994?w=800&auto=format&fit=crop" alt="House in Greinhain">
            <div class="property-details">
                <div class="property-price">€610,000</div>
                <div class="property-location">Greinhain</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Pricing section with testimonials
    st.markdown("""
    <div class="pricing-section">
        <div class="pricing-left">
            <h2 class="pricing-title">Simple, flat-fee pricing</h2>
            <p class="pricing-subtitle">No commissions, no hidden costs — just one transparent price.</p>
            
            <div class="testimonial testimonial-with-image">
                <img class="testimonial-image" src="https://randomuser.me/api/portraits/men/32.jpg" alt="Customer">
                <div class="testimonial-content">
                    <p class="testimonial-text">"Selling my home was completely hassle-free."</p>
                </div>
            </div>
        </div>
        
        <div class="pricing-right">
            <div class="euro-circle">
                <span class="euro-symbol">€</span>
            </div>
            
            <div class="testimonial">
                <p class="testimonial-text">"Selling my home was completely hassle-free. Highly recommended!"</p>
                <p class="testimonial-author">John Doe</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Security section
    st.markdown("""
    <div class="security-section">
        <div class="check-circle">
            <span class="check-symbol">✓</span>
        </div>
        
        <div class="security-content">
            <h2 class="pricing-title">Secure and legal transactions</h2>
            <p class="pricing-subtitle">All properties are verified and transactions are protected by our secure escrow system.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Close main container
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
