# Function to get person image for testimonial
def get_testimonial_image():
    return "https://randomuser.me/api/portraits/men/32.jpg"

# Define custom CSS for exact match to design
def custom_css():
    return """
    <style>
        /* Reset and global styles */
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
        }
        
        /* Hide Streamlit elements */
        #MainMenu, footer, header {
            visibility: hidden;
        }
        
        .stApp {
            margin: 0 auto;
            max-width: 1200px;
            padding: 0 20px;
        }
        
        .block-container {
            padding-top: 1rem !important;
            padding-bottom: 3rem !important;
            max-width: 100% !important;
        }
        
        /* Custom classes for RealEstateIreland.ie */
        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 20px 0;
            border-bottom: 1px solid #f0f0f0;
        }
        
        .logo {
            display: flex;
            align-items: center;
        }
        
        .nav {
            display: flex;
            gap: 40px;
        }
        
        .nav-link {
            color: #333;
            text-decoration: none;
            font-weight: 500;
            font-size: 16px;
        }
        
        .hero {
            display: flex;
            align-items: flex-start;
            gap: 40px;
            margin: 40px 0;
        }
        
        .hero-content {
            flex: 3;
        }
        
        .hero-title {
            font-size: 48px;
            font-weight: 700;
            color: #333;
            margin-bottom: 30px;
            line-height: 1.2;
        }
        
        .search-form {
            width: 100%;
        }
        
        .search-row {
            display: flex;
            gap: 10px;
            margin-bottom: 10px;
        }
        
        .search-input {
            flex: 1;
            padding: 12px 15px;
            border: 1px solid #ddd;
            border-radius: 5px;
            font-size: 16px;
            color: #333;
            background-color: white;
            appearance: none;
            -webkit-appearance: none;
            background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="%23666" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"></polyline></svg>');
            background-repeat: no-repeat;
            background-position: right 15px center;
            background-size: 16px;
        }
        
        .search-button {
            width: 100%;
            padding: 12px;
            background-color: #2A7A78;
            color: white;
            border: none;
            border-radius: 5px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: background-color 0.3s;
        }
        
        .search-button:hover {
            background-color: #236361;
        }
        
        .hero-map {
            flex: 2;
            display: flex;
            justify-content: center;
            align-items: flex-start;
        }
        
        .section-title {
            font-size: 32px;
            font-weight: 700;
            color: #333;
            margin: 40px 0 20px;
        }
        
        .property-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 20px;
            margin-bottom: 60px;
        }
        
        .property-card {
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
            transition: transform 0.3s ease;
        }
        
        .property-card:hover {
            transform: translateY(-5px);
        }
        
        .property-image {
            width: 100%;
            height: 180px;
            object-fit: cover;
        }
        
        .property-details {
            padding: 15px;
        }
        
        .property-price {
            font-size: 24px;
            font-weight: 700;
            color: #333;
            margin-bottom: 5px;
        }
        
        .property-location {
            font-size: 16px;
            color: #666;
        }
        
        .pricing-section {
            display: flex;
            justify-content: space-between;
            margin: 60px 0;
        }
        
        .pricing-left {
            flex: 1;
            padding-right: 20px;
        }
        
        .pricing-title {
            font-size: 32px;
            font-weight: 700;
            color: #333;
            margin-bottom: 10px;
        }
        
        .pricing-subtitle {
            font-size: 18px;
            color: #666;
            margin-bottom: 30px;
        }
        
        .pricing-right {
            flex: 1;
            display: flex;
            align-items: flex-start;
            gap: 20px;
        }
        
        .testimonial {
            background-color: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            margin-top: 20px;
        }
        
        .testimonial-with-image {
            display: flex;
            align-items: center;
            gap: 15px;
        }
        
        .testimonial-image {
            width: 60px;
            height: 60px;
            border-radius: 50%;
            object-fit: cover;
        }
        
        .testimonial-text {
            font-style: italic;
            margin-bottom: 10px;
            color: #333;
        }
        
        .testimonial-author {
            font-weight: 600;
            color: #333;
        }
        
        .security-section {
            display: flex;
            align-items: center;
            gap: 30px;
            margin: 60px 0;
        }
        
        .security-icon {
            flex-shrink: 0;
        }
        
        .security-content {
            flex: 1;
        }
        
        /* Make website responsive */
        @media screen and (max-width: 1024px) {
            .property-grid {
                grid-template-columns: repeat(3, 1fr);
            }
        }
        
        @media screen and (max-width: 768px) {
            .hero {
                flex-direction: column;
            }
            
            .hero-content {
                flex: 1;
                width: 100%;
            }
            
            .hero-map {
                width: 100%;
                justify-content: center;
            }
            
            .property-grid {
                grid-template-columns: repeat(2, 1fr);
            }
            
            .pricing-section {
                flex-direction: column;
            }
            
            .pricing-right {
                margin-top: 30px;
            }
        }
        
        @media screen and (max-width: 480px) {
            .property-grid {
                grid-template-columns: 1fr;
            }
            
            .search-row {
                flex-direction: column;
            }
            
            .nav {
                gap: 20px;
            }
        }
    </style>
    """

def main():
    # Apply custom CSS
    st.markdown(custom_css(), unsafe_allow_html=True)
    
    # Header with logo and navigation
    st.markdown(f"""
    <div class="header">
        <div class="logo">
            <img src="{get_logo_base64()}" alt="RealEstateIreland.ie Logo" width="180">
        </div>
        <div class="nav">
            <a href="#" class="nav-link">Buy</a>
            <a href="#" class="nav-link">Sell</a>
            <a href="#" class="nav-link">How It Works</a>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Hero section with search and map
    st.markdown(f"""
    <div class="hero">
        <div class="hero-content">
            <h1 class="hero-title">Find your new home</h1>
            <div class="search-form">
                <div class="search-row">
                    <select class="search-input">
                        <option value="" disabled selected>Price</option>
                        <option>€100,000 - €200,000</option>
                        <option>€200,000 - €300,000</option>
                        <option>€300,000 - €400,000</option>
                        <option>€400,000 - €500,000</option>
                        <option>€500,000+</option>
                    </select>
                    <select class="search-input">
                        <option value="" disabled selected>Location</option>
                        <option>Dublin</option>
                        <option>Cork</option>
                        <option>Galway</option>
                        <option>Limerick</option>
                        <option>Waterford</option>
                    </select>
                    <select class="search-input">
                        <option value="" disabled selected>Property-type</option>
                        <option>House</option>
                        <option>Apartment</option>
                        <option>Bungalow</option>
                        <option>Duplex</option>
                        <option>Land</option>
                    </select>
                </div>
                <button class="search-button">Search</button>
            </div>
        </div>
        <div class="hero-map">
            <img src="{get_ireland_map_base64()}" alt="Map of Ireland" width="300">
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Featured Properties section
    st.markdown("""
    <h2 class="section-title">Featured Properties</h2>
    """, unsafe_allow_html=True)
    
    # Property grid
    property_grid_html = """
    <div class="property-grid">
    """
    
    # Define property data
    properties = [
        {"price": "€450,000", "location": "Ausland", "image": get_house_image(0)},
        {"price": "€375,000", "location": "Huntavv", "image": get_house_image(1)},
        {"price": "€520,000", "location": "Landhaus", "image": get_house_image(2)},
        {"price": "€610,000", "location": "Greinhain", "image": get_house_image(3)}
    ]
    
    # Create property cards
    for property in properties:
        property_grid_html += f"""
        <div class="property-card">
            <img class="property-image" src="{property['image']}" alt="Property in {property['location']}">
            <div class="property-details">
                <div class="property-price">{property['price']}</div>
                <div class="property-location">{property['location']}</div>
            </div>
        </div>
        """
    
    property_grid_html += """
    </div>
    """
    
    st.markdown(property_grid_html, unsafe_allow_html=True)
    
    # Simple, flat-fee pricing section
    st.markdown(f"""
    <div class="pricing-section">
        <div class="pricing-left">
            <h2 class="pricing-title">Simple, flat-fee pricing</h2>
            <p class="pricing-subtitle">No commissions, no hidden costs — just one transparent price.</p>
            
            <div class="testimonial testimonial-with-image">
                <img class="testimonial-image" src="{get_testimonial_image()}" alt="Customer">
                <div>
                    <p class="testimonial-text">"Selling my home was completely hassle-free."</p>
                </div>
            </div>
        </div>
        
        <div class="pricing-right">
            <div class="security-icon">
                <img src="{get_euro_icon_base64()}" alt="Euro symbol" width="70">
            </div>
            
            <div>
                <div class="testimonial">
                    <p class="testimonial-text">"Selling my home was completely hassle-free. Highly recommended!"</p>
                    <p class="testimonial-author">John Doe</p>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Secure and legal transactions section
    st.markdown(f"""
    <div class="security-section">
        <div class="security-icon">
            <img src="{get_checkmark_icon_base64()}" alt="Checkmark" width="70">
        </div>
        
        <div class="security-content">
            <h2 class="pricing-title">Secure and legal transactions</h2>
            <p class="pricing-subtitle">All properties are verified and transactions are protected by our secure escrow system.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
    # Fallback images as base64 in case the external URLs fail
    fallback_images = [
        "data:image/jpeg;base64,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 streamlit as st
import pandas as pd
import numpy as np
import base64

# Set page configuration
st.set_page_config(
    page_title="RealEstateIreland.ie",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Function to get ireland map svg as base64
def get_ireland_map_base64():
    ireland_map_svg = '''
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
    return f"data:image/svg+xml;base64,{base64.b64encode(ireland_map_svg.encode('utf-8')).decode('utf-8')}"

# Function to get euro icon as base64
def get_euro_icon_base64():
    euro_icon_svg = '''
    <svg width="70" height="70" viewBox="0 0 70 70" fill="none" xmlns="http://www.w3.org/2000/svg">
        <circle cx="35" cy="35" r="33" stroke="#2A7A78" stroke-width="4"/>
        <path d="M45 25H31C29 25 27 26 25.5 27.5C24 29 23 31 22.5 33H40V38H22C21.8 39 21.8 40 22 41H40V46H22.5C23 48 24 50 25.5 51.5C27 53 29 54 31 54H45V59H31C28 59 25 58 22.5 56C20 54 18 51 17.5 48H15V42H17.5V38H15V32H17.5C18 29 20 26 22.5 24C25 22 28 21 31 21H45V25Z" fill="#2A7A78"/>
    </svg>
    '''
    return f"data:image/svg+xml;base64,{base64.b64encode(euro_icon_svg.encode('utf-8')).decode('utf-8')}"

# Function to get checkmark icon as base64
def get_checkmark_icon_base64():
    checkmark_icon_svg = '''
    <svg width="70" height="70" viewBox="0 0 70 70" fill="none" xmlns="http://www.w3.org/2000/svg">
        <circle cx="35" cy="35" r="33" stroke="#2A7A78" stroke-width="4"/>
        <path d="M20 35L30 45L50 25" stroke="#2A7A78" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>
    '''
    return f"data:image/svg+xml;base64,{base64.b64encode(checkmark_icon_svg.encode('utf-8')).decode('utf-8')}"

# Function to get logo as base64
def get_logo_base64():
    logo_svg = '''
    <svg width="180" height="60" viewBox="0 0 180 60" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M30.4 13.6L45.2 24.8V46.4H37.6V28.8H23.2V46.4H15.6V24.8L30.4 13.6Z" fill="#2A7A78"/>
        <path d="M47.2 22.8L30.4 10L13.6 22.8V48.4H25.2V30.8H35.6V48.4H47.2V22.8Z" stroke="#2A7A78" stroke-width="3"/>
        <text x="57" y="27" font-family="Arial, sans-serif" font-size="16" font-weight="bold" fill="#2A7A78">RealEstate</text>
        <text x="57" y="45" font-family="Arial, sans-serif" font-size="16" font-weight="bold" fill="#2A7A78">Ireland.ie</text>
    </svg>
    '''
    return f"data:image/svg+xml;base64,{base64.b64encode(logo_svg.encode('utf-8')).decode('utf-8')}"

# Function to get house images for properties
def get_house_image(index):
    house_images = [
        "https://images.unsplash.com/photo-1564013799919-ab600027ffc6?auto=format&fit=crop&w=600&q=80",
        "https://images.unsplash.com/photo-1570129477492-45c003edd2be?auto=format&fit=crop&w=600&q=80",
        "https://images.unsplash.com/photo-1576941089067-2de3c901e126?auto=format&fit=crop&w=600&q=80",
        "https://images.unsplash.com/photo-1568605114967-8130f3a36994?auto=format&fit=crop&w=600&q=80"
    ]
    
    # Fallback images as base64 in case the external URLs fail
    fallback_images = [
        "data:image/jpeg;base64,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
