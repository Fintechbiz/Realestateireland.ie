<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Real Estate Ireland | Sell Your Property Directly</title>
    <style>
        :root {
            --primary: #34a853;
            --secondary: #1e3a8a;
            --dark: #1f2937;
            --light: #f9fafb;
            --accent: #f59e0b;
            --danger: #ef4444;
            --success: #10b981;
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        
        body {
            background-color: var(--light);
            color: var(--dark);
            line-height: 1.6;
        }
        
        header {
            background-color: white;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            position: sticky;
            top: 0;
            z-index: 100;
        }
        
        .container {
            width: 90%;
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 15px;
        }
        
        .navbar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 1.5rem 0;
        }
        
        .logo {
            font-size: 1.5rem;
            font-weight: 700;
            color: var(--secondary);
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        
        .logo span {
            color: var(--primary);
        }
        
        .nav-links {
            display: flex;
            gap: 2rem;
        }
        
        .nav-links a {
            text-decoration: none;
            color: var(--dark);
            font-weight: 500;
            transition: color 0.3s;
        }
        
        .nav-links a:hover {
            color: var(--primary);
        }
        
        .btn {
            display: inline-block;
            padding: 0.75rem 1.5rem;
            border-radius: 4px;
            text-decoration: none;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
        }
        
        .btn-primary {
            background-color: var(--primary);
            color: white;
        }
        
        .btn-primary:hover {
            background-color: #2d9249;
        }
        
        .btn-outline {
            border: 2px solid var(--primary);
            color: var(--primary);
            background: transparent;
        }
        
        .btn-outline:hover {
            background-color: var(--primary);
            color: white;
        }
        
        .hero {
            padding: 5rem 0;
            background: linear-gradient(135deg, #f6f9fc 0%, #ecf4fe 100%);
        }
        
        .hero-content {
            display: flex;
            align-items: center;
            gap: 3rem;
        }
        
        .hero-text {
            flex: 1;
        }
        
        .hero-image {
            flex: 1;
            text-align: center;
        }
        
        .hero-image img {
            max-width: 100%;
            height: auto;
            border-radius: 8px;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
        }
        
        h1 {
            font-size: 2.5rem;
            margin-bottom: 1.5rem;
            color: var(--secondary);
            line-height: 1.3;
        }
        
        h2 {
            font-size: 2rem;
            margin-bottom: 1rem;
            color: var(--secondary);
        }
        
        h3 {
            font-size: 1.5rem;
            margin-bottom: 1rem;
            color: var(--dark);
        }
        
        p {
            margin-bottom: 1.5rem;
        }
        
        .savings-calculator {
            background-color: white;
            padding: 2rem;
            border-radius: 8px;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05);
            margin-top: 2rem;
        }
        
        .input-group {
            margin-bottom: 1.5rem;
        }
        
        label {
            display: block;
            margin-bottom: 0.5rem;
            font-weight: 500;
        }
        
        input {
            width: 100%;
            padding: 0.75rem;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-size: 1rem;
        }
        
        .result {
            background-color: #f8fafc;
            padding: 1.5rem;
            border-radius: 4px;
            margin-top: 1rem;
            display: none;
        }
        
        .result.active {
            display: block;
        }
        
        .features {
            padding: 5rem 0;
        }
        
        .section-header {
            text-align: center;
            margin-bottom: 3rem;
        }
        
        .features-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 2rem;
        }
        
        .feature-card {
            background-color: white;
            padding: 2rem;
            border-radius: 8px;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05);
            transition: transform 0.3s;
        }
        
        .feature-card:hover {
            transform: translateY(-5px);
        }
        
        .feature-icon {
            font-size: 2.5rem;
            color: var(--primary);
            margin-bottom: 1rem;
        }
        
        .how-it-works {
            padding: 5rem 0;
            background-color: #f8fafc;
        }
        
        .steps {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 2rem;
            margin-top: 2rem;
        }
        
        .step {
            text-align: center;
            padding: 2rem;
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05);
        }
        
        .step-number {
            display: inline-flex;
            justify-content: center;
            align-items: center;
            width: 50px;
            height: 50px;
            background-color: var(--primary);
            color: white;
            border-radius: 50%;
            font-size: 1.5rem;
            font-weight: 600;
            margin-bottom: 1rem;
        }
        
        .testimonials {
            padding: 5rem 0;
        }
        
        .testimonial-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 2rem;
        }
        
        .testimonial-card {
            background-color: white;
            padding: 2rem;
            border-radius: 8px;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05);
        }
        
        .testimonial-text {
            font-style: italic;
            margin-bottom: 1.5rem;
        }
        
        .testimonial-author {
            display: flex;
            align-items: center;
            gap: 1rem;
        }
        
        .author-image {
            width: 50px;
            height: 50px;
            border-radius: 50%;
            overflow: hidden;
            background-color: #ddd;
        }
        
        .author-info h4 {
            font-weight: 600;
        }
        
        .author-info p {
            color: #6b7280;
            font-size: 0.875rem;
            margin-bottom: 0;
        }
        
        .cta {
            padding: 5rem 0;
            background-color: var(--secondary);
            color: white;
            text-align: center;
        }
        
        .cta h2 {
            color: white;
        }
        
        .cta-buttons {
            display: flex;
            justify-content: center;
            gap: 1rem;
            margin-top: 2rem;
        }
        
        footer {
            padding: 3rem 0;
            background-color: var(--dark);
            color: white;
        }
        
        .footer-content {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 2rem;
        }
        
        .footer-logo {
            font-size: 1.5rem;
            font-weight: 700;
            margin-bottom: 1rem;
            color: white;
        }
        
        .footer-logo span {
            color: var(--primary);
        }
        
        .footer-links h3 {
            color: white;
            font-size: 1.2rem;
            margin-bottom: 1.5rem;
        }
        
        .footer-links ul {
            list-style: none;
        }
        
        .footer-links ul li {
            margin-bottom: 0.75rem;
        }
        
        .footer-links ul li a {
            text-decoration: none;
            color: #d1d5db;
            transition: color 0.3s;
        }
        
        .footer-links ul li a:hover {
            color: var(--primary);
        }
        
        .copyright {
            text-align: center;
            padding-top: 2rem;
            margin-top: 2rem;
            border-top: 1px solid #374151;
            color: #9ca3af;
        }
        
        @media (max-width: 768px) {
            .hero-content {
                flex-direction: column;
            }
            
            .navbar {
                flex-direction: column;
                gap: 1rem;
            }
            
            .nav-links {
                flex-wrap: wrap;
                justify-content: center;
            }
            
            h1 {
                font-size: 2rem;
            }
        }
    </style>
    <script>
        function calculateSavings() {
            const propertyValue = parseFloat(document.getElementById('propertyValue').value);
            if (!propertyValue || isNaN(propertyValue)) {
                alert('Please enter a valid property value');
                return;
            }
            
            const traditionalFee = propertyValue * 0.015; // 1.5% + VAT
            const ourFee = 1500; // €1,500 flat fee
            const savings = traditionalFee - ourFee;
            
            const resultElement = document.getElementById('calculationResult');
            resultElement.innerHTML = `
                <p><strong>Traditional Agent Fee (1.5%):</strong> €${traditionalFee.toLocaleString('en-IE', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</p>
                <p><strong>Our Flat Fee:</strong> €${ourFee.toLocaleString('en-IE')}</p>
                <p class="savings"><strong>Your Savings:</strong> €${savings.toLocaleString('en-IE', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</p>
            `;
            
            resultElement.classList.add('active');
            resultElement.style.display = 'block';
            
            // Add styling to the savings line
            const savingsLine = resultElement.querySelector('.savings');
            savingsLine.style.color = '#34a853';
            savingsLine.style.fontWeight = 'bold';
            savingsLine.style.fontSize = '1.2rem';
        }
    </script>
</head>
<body>
    <header>
        <div class="container">
            <nav class="navbar">
                <div class="logo">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M3 9L12 2L21 9V20C21 20.5304 20.7893 21.0391 20.4142 21.4142C20.0391 21.7893 19.5304 22 19 22H5C4.46957 22 3.96086 21.7893 3.58579 21.4142C3.21071 21.0391 3 20.5304 3 20V9Z" stroke="#34a853" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                        <path d="M9 22V12H15V22" stroke="#34a853" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                    <span>Real<span>Estate</span>Ireland</span>
                </div>
                <div class="nav-links">
                    <a href="#features">Features</a>
                    <a href="#how-it-works">How It Works</a>
                    <a href="#testimonials">Testimonials</a>
                    <a href="#contact">Contact</a>
                </div>
                <div>
                    <a href="#" class="btn btn-outline">Log In</a>
                    <a href="#" class="btn btn-primary">List Your Property</a>
                </div>
            </nav>
        </div>
    </header>
    
    <section class="hero">
        <div class="container">
            <div class="hero-content">
                <div class="hero-text">
                    <h1>Sell Your Home for a Flat Fee of €1,500 and Save Thousands</h1>
                    <p>Say goodbye to high estate agent commissions. Our platform lets you sell your property directly with legal security, transparent bidding, and full control of the process.</p>
                    <a href="#" class="btn btn-primary">Start Selling Now</a>
                    
                    <div class="savings-calculator">
                        <h3>See How Much You Could Save</h3>
                        <div class="input-group">
                            <label for="propertyValue">Enter Your Estimated Property Value (€)</label>
                            <input type="number" id="propertyValue" placeholder="e.g. 500000">
                        </div>
                        <button class="btn btn-primary" onclick="calculateSavings()">Calculate Savings</button>
                        <div class="result" id="calculationResult"></div>
                    </div>
                </div>
                <div class="hero-image">
                    <img src="/api/placeholder/600/400" alt="Modern home illustration">
                </div>
            </div>
        </div>
    </section>
    
    <section class="features" id="features">
        <div class="container">
            <div class="section-header">
                <h2>Why Choose Real Estate Ireland?</h2>
                <p>Our platform offers unique benefits over traditional estate agents</p>
            </div>
            <div class="features-grid">
                <div class="feature-card">
                    <div class="feature-icon">💰</div>
                    <h3>Flat Fee Pricing</h3>
                    <p>Pay just €1,500 instead of 1-2% commission. On a €600,000 property, you could save up to €12,000!</p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">🔒</div>
                    <h3>Legally Secure Process</h3>
                    <p>We partner with reputable law firms to handle the legal transfer process efficiently and securely.</p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">🏦</div>
                    <h3>Escrow-Backed Deposits</h3>
                    <p>Buyers place deposits in secure escrow wallets, showing serious intent and deterring frivolous offers.</p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">👁️</div>
                    <h3>Transparent Bidding</h3>
                    <p>Optional open bidding system prevents under-the-table offers and creates a fairer environment.</p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">📊</div>
                    <h3>Digital Timeline Tracker</h3>
                    <p>Track legal progress (survey, valuation, solicitor steps) in real time throughout the sale process.</p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">✅</div>
                    <h3>Verified Buyers</h3>
                    <p>Our system verifies buyer identity and financing readiness, so you don't waste time with unqualified leads.</p>
                </div>
            </div>
        </div>
    </section>
    
    <section class="how-it-works" id="how-it-works">
        <div class="container">
            <div class="section-header">
                <h2>How It Works</h2>
                <p>Selling your property with us is simple and straightforward</p>
            </div>
            <div class="steps">
                <div class="step">
                    <div class="step-number">1</div>
                    <h3>List Your Property</h3>
                    <p>Create an account and upload your property details, photos, and documents. Our AI system helps determine optimal pricing.</p>
                </div>
                <div class="step">
                    <div class="step-number">2</div>
                    <h3>Receive & Review Offers</h3>
                    <p>Verified buyers submit offers through our platform. You can accept, decline, or negotiate directly.</p>
                </div>
                <div class="step">
                    <div class="step-number">3</div>
                    <h3>Secure the Sale</h3>
                    <p>Once you accept an offer, buyers sign a legally-binding agreement and place a deposit in our secure escrow system.</p>
                </div>
                <div class="step">
                    <div class="step-number">4</div>
                    <h3>Complete Legal Transfer</h3>
                    <p>Our partner law firm handles the legal process efficiently, with progress tracked digitally every step of the way.</p>
                </div>
            </div>
        </div>
    </section>
    
    <section class="testimonials" id="testimonials">
        <div class="container">
            <div class="section-header">
                <h2>What Our Customers Say</h2>
                <p>See how sellers across Ireland have saved thousands with our platform</p>
            </div>
            <div class="testimonial-grid">
                <div class="testimonial-card">
                    <div class="testimonial-text">
                        "I saved over €9,000 selling my Dublin home through RealEstateIreland. The process was incredibly straightforward, and the legal support gave me complete peace of mind."
                    </div>
                    <div class="testimonial-author">
                        <div class="author-image">
                            <!-- Placeholder for author image -->
                        </div>
                        <div class="author-info">
                            <h4>Sarah O'Connor</h4>
                            <p>Dublin</p>
                        </div>
                    </div>
                </div>
                <div class="testimonial-card">
                    <div class="testimonial-text">
                        "As a first-time seller, I was worried about handling the sale myself. But the platform made it so easy, and the transparency of the bidding process actually got me a better price than I expected."
                    </div>
                    <div class="testimonial-author">
                        <div class="author-image">
                            <!-- Placeholder for author image -->
                        </div>
                        <div class="author-info">
                            <h4>Michael Byrne</h4>
                            <p>Cork</p>
                        </div>
                    </div>
                </div>
                <div class="testimonial-card">
                    <div class="testimonial-text">
                        "The digital timeline tracker was brilliant - I could see exactly what was happening with my sale at every stage. No chasing solicitors for updates. And the flat fee saved me thousands!"
                    </div>
                    <div class="testimonial-author">
                        <div class="author-image">
                            <!-- Placeholder for author image -->
                        </div>
                        <div class="author-info">
                            <h4>Emma Fitzgerald</h4>
                            <p>Galway</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>
    
    <section class="cta">
        <div class="container">
            <h2>Ready to Save Thousands on Your Property Sale?</h2>
            <p>Join thousands of Irish homeowners who have chosen a better way to sell.</p>
            <div class="cta-buttons">
                <a href="#" class="btn btn-primary">List Your Property</a>
                <a href="#" class="btn btn-outline" style="border-color: white; color: white;">Learn More</a>
            </div>
        </div>
    </section>
    
    <footer id="contact">
        <div class="container">
            <div class="footer-content">
                <div>
                    <div class="footer-logo">Real<span>Estate</span>Ireland</div>
                    <p>The smarter way to sell your property in Ireland. Save thousands with our flat-fee model and secure, transparent process.</p>
                </div>
                <div class="footer-links">
                    <h3>Quick Links</h3>
                    <ul>
                        <li><a href="#">Home</a></li>
                        <li><a href="#features">Features</a></li>
                        <li><a href="#how-it-works">How It Works</a></li>
                        <li><a href="#testimonials">Testimonials</a></li>
                    </ul>
                </div>
                <div class="footer-links">
                    <h3>Resources</h3>
                    <ul>
                        <li><a href="#">Seller Guide</a></li>
                        <li><a href="#">Legal Process</a></li>
                        <li><a href="#">Pricing Calculator</a></li>
                        <li><a href="#">FAQs</a></li>
                    </ul>
                </div>
                <div class="footer-links">
                    <h3>Contact Us</h3>
                    <ul>
                        <li><a href="mailto:info@realestateireland.ie">info@realestateireland.ie</a></li>
                        <li><a href="tel:+35312345678">+353 1 234 5678</a></li>
                        <li>Trinity Business School, Dublin</li>
                    </ul>
                </div>
            </div>
            <div class="copyright">
                <p>&copy; 2025 RealEstateIreland. All rights reserved.</p>
            </div>
        </div>
    </footer>
</body>
</html>
