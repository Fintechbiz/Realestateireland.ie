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
    
    with tabs[2]:
        # Viewing calendar and management
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Calendar view
            st.markdown("<h3>Viewing Calendar</h3>", unsafe_allow_html=True)
            
            # Create a simple calendar view
            today = datetime.now()
            month_start = today.replace(day=1)
            
            # Generate some sample viewing data
            viewings = [
                {"date": "2025-05-22", "time": "17:30", "name": "John & Mary Smith", "status": "Confirmed"},
                {"date": "2025-05-23", "time": "11:00", "name": "David Brown", "status": "Confirmed"},
                {"date": "2025-05-23", "time": "14:30", "name": "Sarah Johnson", "status": "Pending"},
                {"date": "2025-05-25", "time": "12:00", "name": "Michael O'Connor", "status": "Confirmed"},
                {"date": "2025-05-26", "time": "18:00", "name": "Emma Wilson", "status": "Pending"}
            ]
            
            # Display the calendar (simplified view)
            st.markdown("""
            <div style="border: 1px solid #ddd; border-radius: 5px; padding: 10px; background-color: white;">
                <h4 style="text-align: center;">May 2025</h4>
                <table style="width: 100%; text-align: center; border-collapse: collapse;">
                    <tr>
                        <th style="padding: 8px; border: 1px solid #ddd;">Mon</th>
                        <th style="padding: 8px; border: 1px solid #ddd;">Tue</th>
                        <th style="padding: 8px; border: 1px solid #ddd;">Wed</th>
                        <th style="padding: 8px; border: 1px solid #ddd;">Thu</th>
                        <th style="padding: 8px; border: 1px solid #ddd;">Fri</th>
                        <th style="padding: 8px; border: 1px solid #ddd;">Sat</th>
                        <th style="padding: 8px; border: 1px solid #ddd;">Sun</th>
                    </tr>
                    <tr>
                        <td style="padding: 8px; border: 1px solid #ddd;">-</td>
                        <td style="padding: 8px; border: 1px solid #ddd;">-</td>
                        <td style="padding: 8px; border: 1px solid #ddd;">1</td>
                        <td style="padding: 8px; border: 1px solid #ddd;">2</td>
                        <td style="padding: 8px; border: 1px solid #ddd;">3</td>
                        <td style="padding: 8px; border: 1px solid #ddd;">4</td>
                        <td style="padding: 8px; border: 1px solid #ddd;">5</td>
                    </tr>
                    <tr>
                        <td style="padding: 8px; border: 1px solid #ddd;">6</td>
                        <td style="padding: 8px; border: 1px solid #ddd;">7</td>
                        <td style="padding: 8px; border: 1px solid #ddd;">8</td>
                        <td style="padding: 8px; border: 1px solid #ddd;">9</td>
                        <td style="padding: 8px; border: 1px solid #ddd;">10</td>
                        <td style="padding: 8px; border: 1px solid #ddd;">11</td>
                        <td style="padding: 8px; border: 1px solid #ddd;">12</td>
                    </tr>
                    <tr>
                        <td style="padding: 8px; border: 1px solid #ddd;">13</td>
                        <td style="padding: 8px; border: 1px solid #ddd;">14</td>
                        <td style="padding: 8px; border: 1px solid #ddd;">15</td>
                        <td style="padding: 8px; border: 1px solid #ddd;">16</td>
                        <td style="padding: 8px; border: 1px solid #ddd;">17</td>
                        <td style="padding: 8px; border: 1px solid #ddd;">18</td>
                        <td style="padding: 8px; border: 1px solid #ddd;">19</td>
                    </tr>
                    <tr>
                        <td style="padding: 8px; border: 1px solid #ddd;">20</td>
                        <td style="padding: 8px; border: 1px solid #ddd;">21</td>
                        <td style="padding: 8px; border: 1px solid #ddd;">22 <span style="display: block; background-color: #006648; color: white; border-radius: 50%; width: 20px; height: 20px; line-height: 20px; margin: 0 auto;">1</span></td>
                        <td style="padding: 8px; border: 1px solid #ddd;">23 <span style="display: block; background-color: #006648; color: white; border-radius: 50%; width: 20px; height: 20px; line-height: 20px; margin: 0 auto;">2</span></td>
                        <td style="padding: 8px; border: 1px solid #ddd;">24</td>
                        <td style="padding: 8px; border: 1px solid #ddd;">25 <span style="display: block; background-color: #006648; color: white; border-radius: 50%; width: 20px; height: 20px; line-height: 20px; margin: 0 auto;">1</span></td>
                        <td style="padding: 8px; border: 1px solid #ddd;">26 <span style="display: block; background-color: #006648; color: white; border-radius: 50%; width: 20px; height: 20px; line-height: 20px; margin: 0 auto;">1</span></td>
                    </tr>
                    <tr>
                        <td style="padding: 8px; border: 1px solid #ddd;">27</td>
                        <td style="padding: 8px; border: 1px solid #ddd;">28</td>
                        <td style="padding: 8px; border: 1px solid #ddd;">29</td>
                        <td style="padding: 8px; border: 1px solid #ddd;">30</td>
                        <td style="padding: 8px; border: 1px solid #ddd;">31</td>
                        <td style="padding: 8px; border: 1px solid #ddd;">-</td>
                        <td style="padding: 8px; border: 1px solid #ddd;">-</td>
                    </tr>
                </table>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("<h3>Upcoming Viewings</h3>", unsafe_allow_html=True)
            
            # Display upcoming viewings
            for viewing in viewings:
                status_color = "#28a745" if viewing["status"] == "Confirmed" else "#ffc107"
                
                st.markdown(f"""
                <div style="border: 1px solid #ddd; border-radius: 5px; padding: 10px; margin-bottom: 10px; background-color: white;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <h4 style="margin: 0;">{viewing["date"]} at {viewing["time"]}</h4>
                        <span style="background-color: #ffc107; color: white; width: 20px; height: 20px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin-right: 10px;">!</span>
                    <span>Property Survey</span>
                </div>
                <div style="display: flex; align-items: center; margin-bottom: 10px;">
                    <span style="background-color: #6c757d; color: white; width: 20px; height: 20px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin-right: 10px;">○</span>
                    <span>Signed Contract</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Communication log
            st.markdown("""
            <div class="card">
                <h4>Communication Log</h4>
                <div style="max-height: 300px; overflow-y: auto;">
                    <div style="border-left: 3px solid #17a2b8; padding-left: 15px; margin-bottom: 15px;">
                        <p style="margin: 0; font-size: 0.8rem; color: #6c757d;">May 20, 2025 - 14:30</p>
                        <p style="margin: 5px 0 0 0;">Deposit payment of €59,000 received and confirmed in escrow.</p>
                    </div>
                    <div style="border-left: 3px solid #17a2b8; padding-left: 15px; margin-bottom: 15px;">
                        <p style="margin: 0; font-size: 0.8rem; color: #6c757d;">May 19, 2025 - 16:45</p>
                        <p style="margin: 5px 0 0 0;">Offer of €590,000 accepted by seller.</p>
                    </div>
                    <div style="border-left: 3px solid #17a2b8; padding-left: 15px; margin-bottom: 15px;">
                        <p style="margin: 0; font-size: 0.8rem; color: #6c757d;">May 19, 2025 - 11:20</p>
                        <p style="margin: 5px 0 0 0;">Offer of €590,000 submitted.</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="text-align: center; padding: 50px 0;">
                <h3>No Active Transactions</h3>
                <p>When you have an accepted offer, you'll see your transaction progress here.</p>
                <button class="custom-button" style="margin-top: 15px;">Browse Properties</button>
            </div>
            """, unsafe_allow_html=True)

# Function to create a AI valuation demo
def ai_valuation_demo():
    st.markdown("<h2 class='sub-header'>AI Property Valuation Tool</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 3])
    
    with col1:
        st.markdown("""
        <div class="card">
            <h3>Get an Accurate Valuation</h3>
            <p>Our AI-powered valuation tool uses advanced algorithms to analyze market data, property features, and location factors to provide an accurate valuation of your property.</p>
            
            <form>
                <div style="margin-bottom: 15px;">
                    <label for="address" style="display: block; margin-bottom: 5px; font-weight: 600;">Property Address</label>
                    <input type="text" id="address" placeholder="Enter your full property address" style="width: 100%; padding: 10px; border-radius: 5px; border: 1px solid #ccc;">
                </div>
                
                <div style="margin-bottom: 15px;">
                    <label for="property_type" style="display: block; margin-bottom: 5px; font-weight: 600;">Property Type</label>
                    <select id="property_type" style="width: 100%; padding: 10px; border-radius: 5px; border: 1px solid #ccc;">
                        <option>Apartment</option>
                        <option>Semi-detached house</option>
                        <option>Detached house</option>
                        <option>Terraced house</option>
                        <option>Bungalow</option>
                    </select>
                </div>
                
                <div style="display: flex; gap: 10px; margin-bottom: 15px;">
                    <div style="flex: 1;">
                        <label for="bedrooms" style="display: block; margin-bottom: 5px; font-weight: 600;">Bedrooms</label>
                        <select id="bedrooms" style="width: 100%; padding: 10px; border-radius: 5px; border: 1px solid #ccc;">
                            <option>1</option>
                            <option>2</option>
                            <option>3</option>
                            <option selected>4</option>
                            <option>5+</option>
                        </select>
                    </div>
                    <div style="flex: 1;">
                        <label for="bathrooms" style="display: block; margin-bottom: 5px; font-weight: 600;">Bathrooms</label>
                        <select id="bathrooms" style="width: 100%; padding: 10px; border-radius: 5px; border: 1px solid #ccc;">
                            <option>1</option>
                            <option>2</option>
                            <option selected>3</option>
                            <option>4+</option>
                        </select>
                    </div>
                </div>
                
                <div style="margin-bottom: 15px;">
                    <label for="size" style="display: block; margin-bottom: 5px; font-weight: 600;">Property Size (sq.m)</label>
                    <input type="number" id="size" value="185" style="width: 100%; padding: 10px; border-radius: 5px; border: 1px solid #ccc;">
                </div>
                
                <div style="margin-bottom: 15px;">
                    <label for="year_built" style="display: block; margin-bottom: 5px; font-weight: 600;">Year Built</label>
                    <input type="number" id="year_built" value="2018" style="width: 100%; padding: 10px; border-radius: 5px; border: 1px solid #ccc;">
                </div>
                
                <div style="margin-bottom: 15px;">
                    <label for="ber" style="display: block; margin-bottom: 5px; font-weight: 600;">BER Rating</label>
                    <select id="ber" style="width: 100%; padding: 10px; border-radius: 5px; border: 1px solid #ccc;">
                        <option>A1</option>
                        <option>A2</option>
                        <option>A3</option>
                        <option>B1</option>
                        <option selected>B2</option>
                        <option>B3</option>
                        <option>C1</option>
                        <option>C2</option>
                        <option>C3</option>
                        <option>D1</option>
                        <option>D2</option>
                        <option>E1</option>
                        <option>E2</option>
                        <option>F</option>
                        <option>G</option>
                    </select>
                </div>
                
                <button class="custom-button" style="width: 100%;">Calculate Valuation</button>
            </form>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Valuation result
        st.markdown("""
        <div class="card">
            <h3>Valuation Result</h3>
            <div style="text-align: center; padding: 20px 0;">
                <h1 style="color: #006648; font-size: 3rem; margin-bottom: 10px;">€575,000</h1>
                <p style="font-size: 1.2rem;">Estimated Market Value</p>
                <p style="font-size: 0.9rem; color: #6c757d;">Confidence Range: €550,000 - €600,000</p>
            </div>
            
            <hr style="margin: 20px 0;">
            
            <h4>Valuation Factors</h4>
            <div style="margin-bottom: 20px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 5px;">
                    <span>Location Premium</span>
                    <span style="color: #28a745; font-weight: 600;">+€45,000</span>
                </div>
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 5px;">
                    <span>Property Size (185 sq.m)</span>
                    <span style="color: #28a745; font-weight: 600;">+€25,000</span>
                </div>
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 5px;">
                    <span>Modern Build (2018)</span>
                    <span style="color: #28a745; font-weight: 600;">+€30,000</span>
                </div>
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 5px;">
                    <span>Energy Efficiency (B2)</span>
                    <span style="color: #28a745; font-weight: 600;">+€15,000</span>
                </div>
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 5px;">
                    <span>Market Demand (Dublin 4)</span>
                    <span style="color: #28a745; font-weight: 600;">+€40,000</span>
                </div>
            </div>
            
            <h4>Recent Comparable Sales</h4>
            <div style="max-height: 200px; overflow-y: auto;">
                <div style="border: 1px solid #ddd; border-radius: 5px; padding: 10px; margin-bottom: 10px;">
                    <div style="display: flex; justify-content: space-between;">
                        <span><strong>22 Pembroke Road</strong></span>
                        <span>€585,000</span>
                    </div>
                    <p style="margin: 5px 0; font-size: 0.9rem;">4 bed, 2 bath, 180 sq.m</p>
                    <p style="margin: 0; font-size: 0.8rem; color: #6c757d;">Sold: March 2025</p>
                </div>
                <div style="border: 1px solid #ddd; border-radius: 5px; padding: 10px; margin-bottom: 10px;">
                    <div style="display: flex; justify-content: space-between;">
                        <span><strong>15 Pembroke Gardens</strong></span>
                        <span>€560,000</span>
                    </div>
                    <p style="margin: 5px 0; font-size: 0.9rem;">3 bed, 3 bath, 175 sq.m</p>
                    <p style="margin: 0; font-size: 0.8rem; color: #6c757d;">Sold: April 2025</p>
                </div>
                <div style="border: 1px solid #ddd; border-radius: 5px; padding: 10px; margin-bottom: 10px;">
                    <div style="display: flex; justify-content: space-between;">
                        <span><strong>30 Wellington Lane</strong></span>
                        <span>€595,000</span>
                    </div>
                    <p style="margin: 5px 0; font-size: 0.9rem;">4 bed, 3 bath, 190 sq.m</p>
                    <p style="margin: 0; font-size: 0.8rem; color: #6c757d;">Sold: February 2025</p>
                </div>
            </div>
            
            <div style="display: flex; gap: 10px; margin-top: 20px;">
                <button class="custom-button" style="flex: 1;">Save Valuation</button>
                <button class="custom-button-secondary" style="flex: 1;">Start Selling</button>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Market trends
        st.markdown("<h3>Local Market Trends</h3>", unsafe_allow_html=True)
        
        # Create market trends chart
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May']
        prices = [540000, 550000, 560000, 570000, 575000]
        
        fig = px.line(x=months, y=prices, 
                     title='Average Property Prices - Dublin 4 (2025)',
                     markers=True,
                     color_discrete_sequence=['#006648'])
        
        fig.update_layout(
            xaxis_title='Month',
            yaxis_title='Average Price (€)',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            yaxis=dict(tickformat='€,.0f')
        )
        
        st.plotly_chart(fig, use_container_width=True)

# Function to create a market insights section
def market_insights():
    st.markdown("<h2 class='sub-header'>Market Insights</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Average price by area
        st.markdown("<h3>Average Property Prices by Area</h3>", unsafe_allow_html=True)
        
        areas = ['Dublin 1', 'Dublin 2', 'Dublin 3', 'Dublin 4', 'Dublin 6', 'Dublin 8', 'Dublin 12']
        prices = [450000, 520000, 480000, 575000, 550000, 420000, 380000]
        
        area_data = pd.DataFrame({
            'Area': areas,
            'Average Price (€)': prices
        })
        
        fig = px.bar(area_data, x='Area', y='Average Price (€)', 
                   color_discrete_sequence=['#006648'])
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            yaxis=dict(tickformat='€,.0f')
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Days on market by property type
        st.markdown("<h3>Average Days on Market by Property Type</h3>", unsafe_allow_html=True)
        
        property_types = ['Apartment', 'Semi-detached', 'Detached', 'Terraced', 'Bungalow']
        days = [35, 42, 56, 38, 50]
        
        dom_data = pd.DataFrame({
            'Property Type': property_types,
            'Average Days on Market': days
        })
        
        fig = px.bar(dom_data, x='Property Type', y='Average Days on Market',
                   color_discrete_sequence=['#ff6b35'])
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Market trends and insights
    st.markdown("""
    <div class="card">
        <h3>Latest Market Insights</h3>
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px;">
            <div style="border: 1px solid #ddd; border-radius: 5px; padding: 15px;">
                <h4>Price Trend</h4>
                <p style="font-size: 2rem; font-weight: 700; color: #28a745; margin: 10px 0;">+7.2%</p>
                <p>Average price increase in Dublin over the past 12 months.</p>
            </div>
            <div style="border: 1px solid #ddd; border-radius: 5px; padding: 15px;">
                <h4>Supply vs Demand</h4>
                <p style="font-size: 2rem; font-weight: 700; color: #dc3545; margin: 10px 0;">-12%</p>
                <p>Decrease in available properties compared to same period last year.</p>
            </div>
            <div style="border: 1px solid #ddd; border-radius: 5px; padding: 15px;">
                <h4>Offer Success Rate</h4>
                <p style="font-size: 2rem; font-weight: 700; color: #17a2b8; margin: 10px 0;">68%</p>
                <p>Percentage of properties sold at or above asking price.</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Recent blog posts / market reports
    st.markdown("<h3>Latest Market Reports</h3>", unsafe_allow_html=True)
    
    cols = st.columns(3)
    
    reports = [
        {"title": "Dublin Property Market Q2 2025", "date": "May 15, 2025", "snippet": "Analysis of the latest trends and data from the Dublin property market in Q2 2025.", "image": "1588880331179"},
        {"title": "First-Time Buyers' Guide 2025", "date": "May 8, 2025", "snippet": "Everything first-time buyers need to know about navigating the Irish property market in 2025.", "image": "1560518883-ce09059eeffa"},
        {"title": "Investment Property ROI Analysis", "date": "April 28, 2025", "snippet": "Detailed analysis of return on investment for different property types across Ireland.", "image": "1582142435826"}
    ]
    
    for i, report in enumerate(reports):
        with cols[i]:
            st.markdown(f"""
            <div style="border: 1px solid #ddd; border-radius: 5px; overflow: hidden;">
                <img src="https://images.unsplash.com/photo-{report["image"]}?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80" style="width: 100%; height: 150px; object-fit: cover;">
                <div style="padding: 15px;">
                    <h4 style="margin-top: 0;">{report["title"]}</h4>
                    <p style="font-size: 0.8rem; color: #6c757d;">{report["date"]}</p>
                    <p>{report["snippet"]}</p>
                    <button class="custom-button-secondary" style="width: 100%;">Read More</button>
                </div>
            </div>
            """, unsafe_allow_html=True)

# Main app function
def main():
    # Website header
    col1, col2, col3 = st.columns([1, 3, 1])
    
    with col2:
        st.markdown("""
        <div style="text-align: center; padding: 20px 0 10px 0;">
            <h1 style="color: #006648; font-size: 2.5rem; margin: 0;">RealEstateIreland.ie</h1>
            <p style="font-size: 1.2rem; margin: 5px 0 0 0;">The smarter way to sell your property</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Navigation bar
    create_nav()
    
    # Hero section
    create_hero()
    
    # USP Section
    display_usp()
    
    # How it works
    how_it_works()
    
    # Features
    features_section()
    
    # Pricing
    pricing_section()
    
    # Savings calculator
    savings_calculator()
    
    # Testimonials
    testimonials_section()
    
    # Demo sections
    st.markdown("<h2 class='sub-header'>Experience the Platform</h2>", unsafe_allow_html=True)
    
    demo_tabs = st.tabs(["Seller Dashboard", "Buyer Dashboard", "AI Valuation Tool", "Market Insights"])
    
    with demo_tabs[0]:
        seller_dashboard()
    
    with demo_tabs[1]:
        buyer_dashboard()
    
    with demo_tabs[2]:
        ai_valuation_demo()
    
    with demo_tabs[3]:
        market_insights()
    
    # About section
    about_section()
    
    # Contact form
    contact_form()
    
    # Footer
    create_footer()

if __name__ == "__main__":
    main()background-color: {status_color}; color: white; padding: 3px 8px; border-radius: 12px; font-size: 0.8rem;">{viewing["status"]}</span>
                    </div>
                    <p style="margin: 5px 0 0 0;"><strong>Viewer:</strong> {viewing["name"]}</p>
                    <div style="display: flex; gap: 5px; margin-top: 10px;">
                        <button class="custom-button-secondary" style="padding: 5px 10px; font-size: 0.8rem;">Reschedule</button>
                        <button class="custom-button-secondary" style="padding: 5px 10px; font-size: 0.8rem;">Cancel</button>
                        <button class="custom-button-secondary" style="padding: 5px 10px; font-size: 0.8rem;">Send Reminder</button>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("""
            <button class="custom-button" style="width: 100%; margin-top: 15px;">+ Schedule New Viewing</button>
            """, unsafe_allow_html=True)
    
    with tabs[3]:
        # Offers management
        st.markdown("<h3>Current Offers</h3>", unsafe_allow_html=True)
        
        # Sample offers data
        offers = [
            {"date": "2025-05-19", "amount": "€590,000", "buyer": "David & Lisa Thompson", "status": "Active", "note": "Cash buyer, no chain, flexible on closing date"},
            {"date": "2025-05-18", "amount": "€580,000", "buyer": "James Wilson", "status": "Active", "note": "Pre-approved mortgage, needs 60-day closing period"},
            {"date": "2025-05-16", "amount": "€575,000", "buyer": "Sarah O'Brien", "status": "Active", "note": "First-time buyer with AIP, can move quickly"},
            {"date": "2025-05-15", "amount": "€560,000", "buyer": "Michael & Emma Davis", "status": "Rejected", "note": "Conditional on selling their current property"},
        ]
        
        # Display offers in a table-like format
        for i, offer in enumerate(offers):
            status_color = "#28a745" if offer["status"] == "Active" else "#dc3545"
            bg_color = "#f8f9fa" if i % 2 == 0 else "white"
            
            st.markdown(f"""
            <div style="border: 1px solid #ddd; border-radius: 5px; padding: 15px; margin-bottom: 15px; background-color: {bg_color};">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                    <div>
                        <h4 style="margin: 0; color: #006648;">{offer["amount"]}</h4>
                        <p style="margin: 5px 0 0 0; font-size: 0.9rem;">Received: {offer["date"]}</p>
                    </div>
                    <span style="background-color: {status_color}; color: white; padding: 3px 10px; border-radius: 12px;">{offer["status"]}</span>
                </div>
                
                <p><strong>Buyer:</strong> {offer["buyer"]}</p>
                <p><strong>Note:</strong> {offer["note"]}</p>
                
                <div style="display: flex; gap: 10px; margin-top: 15px;">
                    <button class="custom-button" style="padding: 8px 15px;">Accept</button>
                    <button class="custom-button-secondary" style="padding: 8px 15px;">Counter</button>
                    <button class="custom-button-secondary" style="padding: 8px 15px;">Reject</button>
                    <button class="custom-button-secondary" style="padding: 8px 15px;">View Details</button>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Offer comparison chart
        st.markdown("<h3>Offer Comparison</h3>", unsafe_allow_html=True)
        
        # Create offer comparison chart
        offer_data = {
            'Buyer': [offer["buyer"] for offer in offers if offer["status"] == "Active"],
            'Amount': [int(re.sub(r'[^0-9]', '', offer["amount"])) for offer in offers if offer["status"] == "Active"]
        }
        
        offer_df = pd.DataFrame(offer_data)
        offer_df['Asking Price'] = 575000
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=offer_df['Buyer'],
            y=offer_df['Amount'],
            name='Offer Amount',
            marker_color='#006648'
        ))
        
        fig.add_trace(go.Scatter(
            x=offer_df['Buyer'],
            y=offer_df['Asking Price'],
            mode='lines',
            name='Asking Price',
            line=dict(color='red', width=2, dash='dash')
        ))
        
        fig.update_layout(
            title='Active Offers vs. Asking Price',
            xaxis_title='Buyer',
            yaxis_title='Amount (€)',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            yaxis=dict(tickformat='€,.0f'),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with tabs[4]:
        # Legal progress tracker
        st.markdown("<h3>Legal Progress Tracker</h3>", unsafe_allow_html=True)
        
        progress = 65  # Example progress percentage
        
        # Overall progress bar
        st.markdown(f"""
        <div style="background-color: #f8f9fa; border-radius: 5px; padding: 20px; margin-bottom: 20px;">
            <h4>Overall Sale Progress: {progress}%</h4>
            <div style="background-color: #e9ecef; border-radius: 10px; height: 20px; margin-top: 10px;">
                <div style="background-color: #006648; width: {progress}%; height: 20px; border-radius: 10px;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Process steps
        steps = [
            {"title": "Seller Verification", "status": "Completed", "date": "2025-05-13", "note": "Identity and property ownership verified."},
            {"title": "Property Documentation", "status": "Completed", "date": "2025-05-14", "note": "All required documents uploaded and verified."},
            {"title": "Offer Acceptance", "status": "Completed", "date": "2025-05-19", "note": "Offer of €590,000 from David & Lisa Thompson accepted."},
            {"title": "Deposit Payment", "status": "Completed", "date": "2025-05-20", "note": "10% deposit (€59,000) received in escrow."},
            {"title": "Contract Drafting", "status": "In Progress", "date": "", "note": "Sale contract being prepared by partner law firm."},
            {"title": "Buyer Survey", "status": "Pending", "date": "", "note": "Buyer to arrange property survey."},
            {"title": "Mortgage Approval", "status": "Not Required", "date": "", "note": "Cash buyer - no mortgage required."},
            {"title": "Contract Exchange", "status": "Pending", "date": "", "note": ""},
            {"title": "Completion", "status": "Pending", "date": "", "note": "Scheduled for June 20, 2025."}
        ]
        
        # Display steps in a timeline view
        for i, step in enumerate(steps):
            # Determine status colors and icons
            if step["status"] == "Completed":
                status_color = "#28a745"
                status_icon = "✓"
                bar_class = "completed"
            elif step["status"] == "In Progress":
                status_color = "#17a2b8"
                status_icon = "⟳"
                bar_class = "in-progress"
            elif step["status"] == "Not Required":
                status_color = "#6c757d"
                status_icon = "–"
                bar_class = "completed"
            else:
                status_color = "#6c757d"
                status_icon = "○"
                bar_class = "pending"
            
            # Calculate if the step is the last one
            is_last = i == len(steps) - 1
            
            # Timeline entry
            st.markdown(f"""
            <div style="display: flex; margin-bottom: {0 if is_last else 10}px;">
                <div style="display: flex; flex-direction: column; align-items: center; margin-right: 15px;">
                    <div style="width: 30px; height: 30px; background-color: {status_color}; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; z-index: 2;">
                        {status_icon}
                    </div>
                    {'' if is_last else f'<div style="width: 2px; height: 100%; background-color: #e9ecef; margin-top: 5px;"></div>'}
                </div>
                <div style="flex: 1; background-color: white; border-radius: 5px; padding: 15px; border: 1px solid #ddd;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <h4 style="margin: 0;">{step["title"]}</h4>
                        <span style="background-color: {status_color}; color: white; padding: 3px 10px; border-radius: 12px; font-size: 0.8rem;">{step["status"]}</span>
                    </div>
                    {f'<p style="margin: 5px 0 0 0; font-size: 0.9rem;">Completed: {step["date"]}</p>' if step["date"] else ''}
                    {f'<p style="margin: 5px 0 0 0;">{step["note"]}</p>' if step["note"] else ''}
                </div>
            </div>
            """, unsafe_allow_html=True)

# Function to create a buyer dashboard
def buyer_dashboard():
    st.markdown("<h2 class='sub-header'>Buyer Dashboard Demo</h2>", unsafe_allow_html=True)
    
    tabs = st.tabs(["Saved Properties", "My Offers", "Transaction Progress"])
    
    with tabs[0]:
        # Saved properties
        st.markdown("<h3>Your Saved Properties</h3>", unsafe_allow_html=True)
        
        # Sample saved properties
        saved_properties = [
            {"address": "24 Pembroke Road, Dublin 4", "price": "€575,000", "beds": 4, "baths": 3, "size": "185 sq.m", "saved_date": "2025-05-15", "status": "Active"},
            {"address": "8 Westmoreland Park, Ranelagh", "price": "€625,000", "beds": 3, "baths": 2, "size": "160 sq.m", "saved_date": "2025-05-17", "status": "Active"},
            {"address": "42 Sandymount Avenue, Dublin 4", "price": "€795,000", "beds": 5, "baths": 3, "size": "210 sq.m", "saved_date": "2025-05-18", "status": "Viewing Scheduled"},
        ]
        
        # Display saved properties in a grid
        cols = st.columns(3)
        
        for i, property in enumerate(saved_properties):
            with cols[i % 3]:
                status_color = "#28a745" if property["status"] == "Viewing Scheduled" else "#17a2b8"
                
                st.markdown(f"""
                <div style="border: 1px solid #ddd; border-radius: 5px; overflow: hidden; margin-bottom: 20px;">
                    <img src="https://images.unsplash.com/photo-{1588880331179 + i * 100}-5e548efb85a0?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80" style="width: 100%; height: 150px; object-fit: cover;">
                    <div style="padding: 15px;">
                        <h4 style="margin-top: 0; margin-bottom: 10px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">{property["address"]}</h4>
                        <p style="font-size: 1.2rem; font-weight: 600; color: #006648; margin: 5px 0;">{property["price"]}</p>
                        <div style="display: flex; justify-content: space-between; margin: 10px 0;">
                            <span>{property["beds"]} Beds</span>
                            <span>{property["baths"]} Baths</span>
                            <span>{property["size"]}</span>
                        </div>
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 10px;">
                            <span style="font-size: 0.8rem;">Saved: {property["saved_date"]}</span>
                            <span style="background-color: {status_color}; color: white; padding: 3px 8px; border-radius: 12px; font-size: 0.8rem;">{property["status"]}</span>
                        </div>
                        <div style="display: flex; gap: 5px; margin-top: 15px;">
                            <button class="custom-button" style="flex: 1;">View</button>
                            <button class="custom-button-secondary" style="flex: 1;">Make Offer</button>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    with tabs[1]:
        # My offers
        st.markdown("<h3>Your Active Offers</h3>", unsafe_allow_html=True)
        
        # Sample offers
        my_offers = [
            {"address": "24 Pembroke Road, Dublin 4", "asking": "€575,000", "offer": "€590,000", "date": "2025-05-19", "status": "Accepted", "notes": "Deposit of €59,000 paid to escrow."},
            {"address": "42 Sandymount Avenue, Dublin 4", "asking": "€795,000", "offer": "€780,000", "date": "2025-05-20", "status": "Pending", "notes": "Waiting for seller response."},
        ]
        
        # Display offers
        for offer in my_offers:
            status_color = "#28a745" if offer["status"] == "Accepted" else "#ffc107"
            
            st.markdown(f"""
            <div style="border: 1px solid #ddd; border-radius: 5px; padding: 15px; margin-bottom: 15px; background-color: white;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                    <h4 style="margin: 0;">{offer["address"]}</h4>
                    <span style="background-color: {status_color}; color: white; padding: 3px 10px; border-radius: 12px;">{offer["status"]}</span>
                </div>
                
                <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                    <div>
                        <p style="margin: 0;"><strong>Asking Price:</strong> {offer["asking"]}</p>
                        <p style="margin: 5px 0 0 0;"><strong>Your Offer:</strong> <span style="color: #006648; font-weight: 600;">{offer["offer"]}</span></p>
                    </div>
                    <div>
                        <p style="margin: 0;"><strong>Offer Date:</strong> {offer["date"]}</p>
                        <p style="margin: 5px 0 0 0;"><strong>Difference:</strong> {f'€{int(re.sub(r"[^0-9]", "", offer["offer"])) - int(re.sub(r"[^0-9]", "", offer["asking"])):,}'}</p>
                    </div>
                </div>
                
                <p><strong>Notes:</strong> {offer["notes"]}</p>
                
                <div style="display: flex; gap: 10px; margin-top: 15px;">
                    <button class="custom-button" style="padding: 8px 15px;">View Details</button>
                    {"<button class='custom-button-secondary' style='padding: 8px 15px;'>Withdraw Offer</button>" if offer["status"] == "Pending" else "<button class='custom-button-secondary' style='padding: 8px 15px;'>View Contract</button>"}
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with tabs[2]:
        # Transaction progress
        if len(my_offers) > 0 and my_offers[0]["status"] == "Accepted":
            st.markdown("<h3>Your Active Transaction</h3>", unsafe_allow_html=True)
            
            progress = 45  # Example progress percentage
            
            # Overall progress bar
            st.markdown(f"""
            <div style="background-color: #f8f9fa; border-radius: 5px; padding: 20px; margin-bottom: 20px;">
                <h4>Property: {my_offers[0]["address"]}</h4>
                <p><strong>Offer Amount:</strong> {my_offers[0]["offer"]}</p>
                <p><strong>Overall Progress:</strong> {progress}%</p>
                <div style="background-color: #e9ecef; border-radius: 10px; height: 20px; margin-top: 10px;">
                    <div style="background-color: #006648; width: {progress}%; height: 20px; border-radius: 10px;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Next steps
            st.markdown("""
            <div class="card">
                <h4>Next Steps</h4>
                <ul>
                    <li><strong>Book Property Survey</strong> - Due by May 25, 2025</li>
                    <li><strong>Review Draft Contract</strong> - Expected by May 27, 2025</li>
                </ul>
                <button class="custom-button" style="margin-top: 15px;">Book Survey Now</button>
            </div>
            """, unsafe_allow_html=True)
            
            # Document checklist
            st.markdown("""
            <div class="card">
                <h4>Document Checklist</h4>
                <div style="display: flex; align-items: center; margin-bottom: 10px;">
                    <span style="background-color: #28a745; color: white; width: 20px; height: 20px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin-right: 10px;">✓</span>
                    <span>ID Verification</span>
                </div>
                <div style="display: flex; align-items: center; margin-bottom: 10px;">
                    <span style="background-color: #28a745; color: white; width: 20px; height: 20px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin-right: 10px;">✓</span>
                    <span>Proof of Funds</span>
                </div>
                <div style="display: flex; align-items: center; margin-bottom: 10px;">
                    <span style="background-color: #28a745; color: white; width: 20px; height: 20px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin-right: 10px;">✓</span>
                    <span>Deposit Payment</span>
                </div>
                <div style="display: flex; align-items: center; margin-bottom: 10px;">
                    <span style="
