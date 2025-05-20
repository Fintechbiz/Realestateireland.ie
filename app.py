import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image
import time
import base64
from datetime import datetime
import io
import altair as alt
import re

# Set page configuration
st.set_page_config(
    page_title="RealEstateIreland.ie",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
def local_css():
    st.markdown("""
    <style>
        /* Main theme colors */
        :root {
            --primary: #006648;
            --secondary: #ff6b35;
            --light: #f8f9fa;
            --dark: #343a40;
            --success: #28a745;
            --info: #17a2b8;
            --warning: #ffc107;
            --danger: #dc3545;
        }
        
        /* Header styling */
        .main-header {
            color: var(--primary);
            font-size: 3.2rem;
            font-weight: 700;
            margin-bottom: 1rem;
            text-align: center;
        }
        
        .sub-header {
            color: var(--dark);
            font-size: 1.8rem;
            font-weight: 600;
            margin-bottom: 1rem;
        }
        
        /* Card-like containers */
        .card {
            background-color: white;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            border-left: 5px solid var(--primary);
        }
        
        /* Feature boxes */
        .feature-box {
            background-color: #f8f9fa;
            border-radius: 10px;
            padding: 1.5rem;
            margin-bottom: 1rem;
            border-top: 4px solid var(--secondary);
            transition: transform 0.3s ease;
        }
        
        .feature-box:hover {
            transform: translateY(-5px);
        }
        
        /* Buttons */
        .custom-button {
            background-color: var(--primary);
            color: white;
            border: none;
            border-radius: 5px;
            padding: 0.5rem 1rem;
            font-weight: 600;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }
        
        .custom-button:hover {
            background-color: #005238;
        }
        
        .custom-button-secondary {
            background-color: var(--secondary);
            color: white;
            border: none;
            border-radius: 5px;
            padding: 0.5rem 1rem;
            font-weight: 600;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }
        
        .custom-button-secondary:hover {
            background-color: #e55a2b;
        }
        
        /* Testimonial styling */
        .testimonial {
            padding: 1.5rem;
            margin-bottom: 1rem;
            background-color: #f8f9fa;
            border-radius: 10px;
            border-left: 4px solid var(--info);
            font-style: italic;
        }
        
        /* Footer */
        .footer {
            background-color: var(--dark);
            color: white;
            padding: 1rem;
            text-align: center;
            border-radius: 5px;
            margin-top: 2rem;
        }
        
        /* Hero section */
        .hero {
            padding: 3rem 0;
            background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), url('https://images.unsplash.com/photo-1560518883-ce09059eeffa?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1073&q=80');
            background-size: cover;
            background-position: center;
            color: white;
            text-align: center;
            border-radius: 10px;
            margin-bottom: 2rem;
        }
        
        .hero h1 {
            font-size: 3.5rem;
            font-weight: 700;
            margin-bottom: 1rem;
        }
        
        .hero p {
            font-size: 1.3rem;
            margin-bottom: 1.5rem;
            max-width: 800px;
            margin-left: auto;
            margin-right: auto;
        }
        
        /* Savings calculator */
        .calculator {
            background-color: white;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            padding: 1.5rem;
            margin-bottom: 1.5rem;
        }
        
        /* Highlights */
        .highlight {
            color: var(--secondary);
            font-weight: 700;
        }
        
        /* Process steps */
        .process-step {
            display: flex;
            align-items: center;
            margin-bottom: 1rem;
        }
        
        .step-number {
            background-color: var(--primary);
            color: white;
            width: 40px;
            height: 40px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 700;
            margin-right: 1rem;
        }
        
        .step-content {
            flex: 1;
        }
        
        /* For hiding Streamlit elements */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        .viewerBadge_container__1QSob {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

local_css()

# Function to create a nav bar
def create_nav():
    st.markdown("""
    <div style="display: flex; justify-content: space-around; margin-bottom: 20px; background-color: #006648; padding: 10px; border-radius: 5px;">
        <a href="#" style="color: white; text-decoration: none; font-weight: 600;">Home</a>
        <a href="#how-it-works" style="color: white; text-decoration: none; font-weight: 600;">How It Works</a>
        <a href="#features" style="color: white; text-decoration: none; font-weight: 600;">Features</a>
        <a href="#pricing" style="color: white; text-decoration: none; font-weight: 600;">Pricing</a>
        <a href="#calculator" style="color: white; text-decoration: none; font-weight: 600;">Savings Calculator</a>
        <a href="#about" style="color: white; text-decoration: none; font-weight: 600;">About Us</a>
        <a href="#contact" style="color: white; text-decoration: none; font-weight: 600;">Contact</a>
    </div>
    """, unsafe_allow_html=True)

# Function to create a hero section
def create_hero():
    st.markdown("""
    <div class="hero">
        <h1>Transform How You Sell Property in Ireland</h1>
        <p>Sell your home with a low flat fee and save thousands. Take control of your property sale with our transparent, secure, and easy-to-use platform.</p>
        <button class="custom-button" style="margin-right: 10px;">Sell Your Property</button>
        <button class="custom-button-secondary">Find a Property</button>
    </div>
    """, unsafe_allow_html=True)

# Function to display USP section
def display_usp():
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-box">
            <h3>💰 Save Thousands</h3>
            <p>Sell your home for a transparent flat fee of €1,500, rather than paying 1-2% commission to traditional agents.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-box">
            <h3>🔒 Secure Transactions</h3>
            <p>Legally-binding offer agreements and escrow-backed deposits provide protection for both buyers and sellers.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-box">
            <h3>📊 Complete Control</h3>
            <p>Manage your entire property sale online with full transparency and direct access to offers and negotiations.</p>
        </div>
        """, unsafe_allow_html=True)

# Function to create How It Works section
def how_it_works():
    st.markdown("<h2 id='how-it-works' class='sub-header'>How It Works</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown("""
        <div class="card">
            <div class="process-step">
                <div class="step-number">1</div>
                <div class="step-content">
                    <h4>Create Your Listing</h4>
                    <p>Upload your property details, photos, and documents. Our AI-powered system will suggest an optimal asking price based on market data.</p>
                </div>
            </div>
            
            <div class="process-step">
                <div class="step-number">2</div>
                <div class="step-content">
                    <h4>Manage Viewings</h4>
                    <p>Schedule and conduct viewings at times that suit you. Our platform helps you organize and track interested buyers.</p>
                </div>
            </div>
            
            <div class="process-step">
                <div class="step-number">3</div>
                <div class="step-content">
                    <h4>Receive & Negotiate Offers</h4>
                    <p>Buyers submit legally-binding offers through our platform. Our transparent system shows you all offers, letting you negotiate from a position of strength.</p>
                </div>
            </div>
            
            <div class="process-step">
                <div class="step-number">4</div>
                <div class="step-content">
                    <h4>Secure the Sale</h4>
                    <p>Once you accept an offer, the buyer places a deposit in our secure escrow system. Our partner law firm handles the legal process efficiently.</p>
                </div>
            </div>
            
            <div class="process-step">
                <div class="step-number">5</div>
                <div class="step-content">
                    <h4>Complete the Transaction</h4>
                    <p>Track the sale progress in real-time. The final sale is completed securely, with the proceeds transferred directly to you.</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Create a simple process flow chart
        chart_data = pd.DataFrame({
            'Stage': ['List', 'Viewings', 'Offers', 'Acceptance', 'Completion'],
            'Time (days)': [1, 7, 5, 1, 30]
        })
        
        fig = px.bar(chart_data, x='Stage', y='Time (days)', 
                     title='Timeline: Typical Property Sale Process',
                     color_discrete_sequence=['#006648'])
        
        fig.update_layout(
            xaxis_title='Sale Stage',
            yaxis_title='Average Duration (days)',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("""
        <div style="background-color: #f8f9fa; padding: 15px; border-radius: 10px; margin-top: 20px;">
            <h4>Average Time to Sale: <span style="color: #006648">44 days</span></h4>
            <p>Traditional agent sales in Ireland typically take 60-90 days from listing to completion.</p>
        </div>
        """, unsafe_allow_html=True)

# Function to create features section
def features_section():
    st.markdown("<h2 id='features' class='sub-header'>Platform Features</h2>", unsafe_allow_html=True)
    
    # Features grid
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="card">
            <h3>For Sellers</h3>
            <ul>
                <li><strong>AI-Powered Valuation:</strong> Get an accurate property valuation based on market data and comparable properties.</li>
                <li><strong>Direct Listing Control:</strong> Update your property details, photos, and availability in real-time.</li>
                <li><strong>Viewing Management:</strong> Schedule and track property viewings with an integrated calendar.</li>
                <li><strong>Transparent Offer System:</strong> See all offers in one place with no hidden information.</li>
                <li><strong>Legal Process Tracking:</strong> Follow the progress of your sale with our digital timeline tracker.</li>
                <li><strong>Flat Fee Structure:</strong> Pay just €1,500 regardless of your property's value.</li>
                <li><strong>Integrated Legal Support:</strong> Access our partner law firm at pre-negotiated rates.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="card">
            <h3>For Buyers</h3>
            <ul>
                <li><strong>Verified Listings:</strong> All properties undergo basic verification to ensure legitimacy.</li>
                <li><strong>Secure Offer Process:</strong> Make legally-binding offers that prevent gazumping and last-minute seller withdrawals.</li>
                <li><strong>Escrow Protection:</strong> Your deposit is held safely in our secure escrow system.</li>
                <li><strong>Direct Seller Communication:</strong> Ask questions and negotiate directly with property owners.</li>
                <li><strong>Document Vault:</strong> Access property documents, certificates, and surveys in one secure location.</li>
                <li><strong>Transparent History:</strong> See the full bidding history and property timeline.</li>
                <li><strong>Identity Verification:</strong> Ensure all parties are legitimate with our verification system.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# Function to create pricing section
def pricing_section():
    st.markdown("<h2 id='pricing' class='sub-header'>Simple, Transparent Pricing</h2>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div style="text-align: center; padding: 30px; background-color: white; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
            <h2 style="color: #006648; margin-bottom: 15px;">€1,500 Flat Fee</h2>
            <p style="font-size: 1.2rem; margin-bottom: 20px;">No hidden costs. No percentage-based commission.</p>
            <hr style="margin: 20px 0;">
            <h3>What's Included:</h3>
            <ul style="text-align: left; list-style-type: none; padding-left: 0;">
                <li style="margin-bottom: 10px;">✅ <strong>Property Listing</strong> - Professional online presence</li>
                <li style="margin-bottom: 10px;">✅ <strong>AI Valuation Tool</strong> - Get an accurate market valuation</li>
                <li style="margin-bottom: 10px;">✅ <strong>Viewing Management</strong> - Organize and track interested buyers</li>
                <li style="margin-bottom: 10px;">✅ <strong>Legal Document Handling</strong> - Through our partner law firm</li>
                <li style="margin-bottom: 10px;">✅ <strong>Offer Management System</strong> - Receive and evaluate offers</li>
                <li style="margin-bottom: 10px;">✅ <strong>Secure Transaction Process</strong> - Escrow protection and legal safeguards</li>
                <li style="margin-bottom: 10px;">✅ <strong>Dedicated Support</strong> - Help when you need it</li>
            </ul>
            <hr style="margin: 20px 0;">
            <p><strong>Introductory Offer: €1,000</strong> for early adopters!</p>
            <button class="custom-button" style="padding: 10px 20px; margin-top: 15px;">Start Selling Now</button>
        </div>
        """, unsafe_allow_html=True)

# Function to create savings calculator
def savings_calculator():
    st.markdown("<h2 id='calculator' class='sub-header'>Savings Calculator</h2>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="calculator">
        <p>See how much you could save by selling with RealEstateIreland.ie compared to a traditional estate agent.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 3])
    
    with col1:
        property_value = st.slider('Estimated Property Value (€)', 100000, 2000000, 600000, step=10000)
        traditional_fee = st.slider('Traditional Agent Commission (%)', 1.0, 2.5, 1.5, step=0.1)
        
    # Calculate savings
    traditional_cost = property_value * (traditional_fee / 100) * 1.23  # Adding 23% VAT
    flat_fee = 1500
    savings = traditional_cost - flat_fee
    
    with col2:
        # Create a comparison chart
        data = pd.DataFrame({
            'Service': ['Traditional Agent', 'RealEstateIreland.ie'],
            'Cost (€)': [traditional_cost, flat_fee]
        })
        
        fig = px.bar(data, x='Service', y='Cost (€)', 
                     title=f'Cost Comparison: €{property_value:,} Property',
                     color='Service',
                     color_discrete_map={'Traditional Agent': '#dc3545', 'RealEstateIreland.ie': '#006648'})
        
        fig.update_layout(
            xaxis_title='',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Display the savings
    st.markdown(f"""
    <div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; text-align: center; margin-top: 20px;">
        <h3>Your Estimated Savings: <span style="color: #006648; font-size: 2rem;">€{savings:,.2f}</span></h3>
        <p>Traditional agent cost (including 23% VAT): €{traditional_cost:,.2f} vs. Our flat fee: €{flat_fee:,.2f}</p>
    </div>
    """, unsafe_allow_html=True)

# Function to create testimonials section
def testimonials_section():
    st.markdown("<h2 class='sub-header'>What Our Customers Say</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="testimonial">
            <p>"I saved over €10,000 selling my Dublin apartment with RealEstateIreland.ie. The platform was intuitive, and the legal partnership gave me complete peace of mind."</p>
            <p style="text-align: right; font-weight: 600;">— Michael D., Dublin</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="testimonial">
            <p>"As a first-time seller, I was nervous about managing the process myself. The step-by-step guidance and support were exceptional, and the savings were substantial!"</p>
            <p style="text-align: right; font-weight: 600;">— Sarah O., Galway</p>
        </div>
        """, unsafe_allow_html=True)

# Function to create about section
def about_section():
    st.markdown("<h2 id='about' class='sub-header'>About RealEstateIreland.ie</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 3])
    
    with col1:
        # Placeholder for company logo or team image
        st.image("https://images.unsplash.com/photo-1557804506-669a67965ba0?ixlib=rb-1.2.1&auto=format&fit=crop&w=1074&q=80", caption="Our Vision: Transforming Irish Real Estate")
    
    with col2:
        st.markdown("""
        <div class="card">
            <h3>Our Mission</h3>
            <p>RealEstateIreland.ie is transforming the Irish property market by providing a faster, more transparent, and significantly more cost-effective way to sell property.</p>
            
            <p>In a market where Dublin homes sold for an average of 8.6% above asking price in late 2024, and where 14% of homes nationally exceeded their asking price by at least 20%, traditional estate agents continue to charge high commissions of 1-2% plus VAT. We believe this is inefficient and unfair to sellers.</p>
            
            <p>Our innovative platform empowers property owners to take control of their sales while providing security through our legal partnerships and escrow-backed deposit system.</p>
            
            <h3>Our Vision</h3>
            <p>We aim to revolutionize the Irish property market, bringing greater efficiency, transparency, and fairness to both buyers and sellers. After establishing ourselves in Ireland, we plan to expand our model to other promising markets including the UK, Spain, and the UAE.</p>
        </div>
        """, unsafe_allow_html=True)

# Function to create contact form
def contact_form():
    st.markdown("<h2 id='contact' class='sub-header'>Contact Us</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="card">
            <h3>Get in Touch</h3>
            <p>Have questions about selling your property with RealEstateIreland.ie? Our team is here to help.</p>
            
            <form>
                <div style="margin-bottom: 15px;">
                    <label for="name" style="display: block; margin-bottom: 5px; font-weight: 600;">Name</label>
                    <input type="text" id="name" placeholder="Your Name" style="width: 100%; padding: 10px; border-radius: 5px; border: 1px solid #ccc;">
                </div>
                
                <div style="margin-bottom: 15px;">
                    <label for="email" style="display: block; margin-bottom: 5px; font-weight: 600;">Email</label>
                    <input type="email" id="email" placeholder="Your Email" style="width: 100%; padding: 10px; border-radius: 5px; border: 1px solid #ccc;">
                </div>
                
                <div style="margin-bottom: 15px;">
                    <label for="phone" style="display: block; margin-bottom: 5px; font-weight: 600;">Phone</label>
                    <input type="tel" id="phone" placeholder="Your Phone Number" style="width: 100%; padding: 10px; border-radius: 5px; border: 1px solid #ccc;">
                </div>
                
                <div style="margin-bottom: 15px;">
                    <label for="message" style="display: block; margin-bottom: 5px; font-weight: 600;">Message</label>
                    <textarea id="message" placeholder="Your Message" style="width: 100%; padding: 10px; border-radius: 5px; border: 1px solid #ccc; height: 120px;"></textarea>
                </div>
                
                <button class="custom-button" style="width: 100%;">Send Message</button>
            </form>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="card">
            <h3>Our Details</h3>
            <p><strong>Email:</strong> info@realestateIreland.ie</p>
            <p><strong>Phone:</strong> +353 (0)1 234 5678</p>
            <p><strong>Address:</strong> Trinity Business School, Trinity College Dublin, Dublin 2, Ireland</p>
            
            <h4 style="margin-top: 20px;">Office Hours</h4>
            <p>Monday - Friday: 9:00am - 5:30pm</p>
            <p>Saturday: 10:00am - 2:00pm</p>
            <p>Sunday: Closed</p>
            
            <h4 style="margin-top: 20px;">Follow Us</h4>
            <div style="display: flex; gap: 10px;">
                <div style="background-color: #3b5998; color: white; width: 40px; height: 40px; border-radius: 50%; display: flex; align-items: center; justify-content: center;">F</div>
                <div style="background-color: #1da1f2; color: white; width: 40px; height: 40px; border-radius: 50%; display: flex; align-items: center; justify-content: center;">T</div>
                <div style="background-color: #0077b5; color: white; width: 40px; height: 40px; border-radius: 50%; display: flex; align-items: center; justify-content: center;">L</div>
                <div style="background-color: #c32aa3; color: white; width: 40px; height: 40px; border-radius: 50%; display: flex; align-items: center; justify-content: center;">I</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# Function to create footer
def create_footer():
    st.markdown("""
    <div class="footer">
        <div style="display: flex; justify-content: space-around; margin-bottom: 20px;">
            <div>
                <h4>RealEstateIreland.ie</h4>
                <p>Transforming property sales in Ireland</p>
            </div>
            <div>
                <h4>Quick Links</h4>
                <p><a href="#" style="color: white; text-decoration: none;">Home</a></p>
                <p><a href="#features" style="color: white; text-decoration: none;">Features</a></p>
                <p><a href="#pricing" style="color: white; text-decoration: none;">Pricing</a></p>
            </div>
            <div>
                <h4>Legal</h4>
                <p><a href="#" style="color: white; text-decoration: none;">Terms & Conditions</a></p>
                <p><a href="#" style="color: white; text-decoration: none;">Privacy Policy</a></p>
                <p><a href="#" style="color: white; text-decoration: none;">Cookie Policy</a></p>
            </div>
        </div>
        <hr style="border-color: #555;">
        <p>© 2025 RealEstateIreland.ie. All rights reserved.</p>
    </div>
    """, unsafe_allow_html=True)

# Function to create a seller dashboard
def seller_dashboard():
    st.markdown("<h2 class='sub-header'>Seller Dashboard Demo</h2>", unsafe_allow_html=True)
    
    tabs = st.tabs(["Overview", "Property Details", "Viewings", "Offers", "Legal Progress"])
    
    with tabs[0]:
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col1:
            st.metric("Property Views", "342", "+28")
            st.metric("Saved by Buyers", "47", "+5")
            st.metric("Active Offers", "3", "+1")
        
        with col2:
            # Property activity chart
            dates = pd.date_range(start='2025-05-01', periods=14)
            views = [12, 24, 18, 32, 45, 38, 27, 42, 39, 45, 52, 48, 35, 28]
            activity_data = pd.DataFrame({
                'Date': dates,
                'Views': views
            })
            
            fig = px.line(activity_data, x='Date', y='Views', 
                         title='Property Listing Activity',
                         markers=True,
                         color_discrete_sequence=['#006648'])
            
            fig.update_layout(
                xaxis_title='',
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col3:
            st.metric("Asking Price", "€575,000", "")
            st.metric("Highest Offer", "€590,000", "+€15,000")
            st.metric("Days Listed", "7", "")
    
    with tabs[1]:
        col1, col2 = st.columns(2)
        
        with col1:
            st.image("https://images.unsplash.com/photo-1605276374104-dee2a0ed3cd6?ixlib=rb-1.2.1&auto=format&fit=crop&w=1170&q=80", caption="Property Front View")
            
            st.markdown("""
            <div class="card">
                <h3>Property Details</h3>
                <p><strong>Address:</strong> 24 Pembroke Road, Dublin 4</p>
                <p><strong>Type:</strong> Semi-detached house</p>
                <p><strong>Bedrooms:</strong> 4</p>
                <p><strong>Bathrooms:</strong> 3</p>
                <p><strong>Size:</strong> 185 sq.m (1,991 sq.ft)</p>
                <p><strong>BER Rating:</strong> B2</p>
                <p><strong>Year Built:</strong> 2018</p>
                <p><strong>Asking Price:</strong> €575,000</p>
                <button class="custom-button-secondary" style="margin-top: 15px;">Edit Details</button>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="card">
                <h3>Property Description</h3>
                <p>A stunning semi-detached family home in a prime Dublin 4 location. This property features a modern open-plan kitchen/dining area, spacious living room, and high-quality finishes throughout.</p>
                <p>The property benefits from excellent energy efficiency with a B2 BER rating, underfloor heating on the ground floor, and a heat recovery ventilation system.</p>
                <p>The rear garden is south-facing and professionally landscaped, with a large patio area perfect for entertaining.</p>
                <p>Located within walking distance of excellent schools, transportation links, and amenities.</p>
                <button class="custom-button-secondary" style="margin-top: 15px;">Edit Description</button>
            </div>
            
            <div class="card" style="margin-top: 20px;">
                <h3>Property Documents</h3>
                <ul>
                    <li>📄 BER Certificate</li>
                    <li>📄 Property Plans</li>
                    <li>📄 Title Deeds (Summary)</li>
                    <li>📄 Planning Permissions</li>
                </ul>
                <button class="custom-button-secondary" style="margin-top: 15px;">Upload New Document</button>
            </div>
            """, unsafe_allow_html=True)
def main():
    # (Re-apply CSS in case Streamlit reload resets styling)
    local_css()

    # Build out the page
    create_nav()
    create_hero()
    display_usp()
    how_it_works()
    features_section()
    pricing_section()
    savings_calculator()
    testimonials_section()
    about_section()
    contact_form()
    create_footer()

    # If you want to preview the seller dashboard demo, uncomment this line:
    # seller_dashboard()

if __name__ == "__main__":
    main()
