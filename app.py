from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime
import os
import uuid

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev_key_for_testing')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///realestate.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static', 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize database
db = SQLAlchemy(app)

# Initialize Login Manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Define models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    properties = db.relationship('Property', backref='owner', lazy=True)
    offers_made = db.relationship('Offer', backref='buyer', lazy=True, foreign_keys='Offer.buyer_id')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
        
    def __repr__(self):
        return f'<User {self.email}>'

class Property(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    address = db.Column(db.String(200), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    county = db.Column(db.String(100), nullable=False)
    eircode = db.Column(db.String(10))
    bedrooms = db.Column(db.Integer)
    bathrooms = db.Column(db.Integer)
    size_sqm = db.Column(db.Float)
    property_type = db.Column(db.String(50))  # apartment, house, commercial, etc.
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='active')  # active, pending, sold, withdrawn
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    photos = db.relationship('PropertyPhoto', backref='property', lazy=True, cascade="all, delete-orphan")
    offers = db.relationship('Offer', backref='property', lazy=True, cascade="all, delete-orphan")
    
    def __repr__(self):
        return f'<Property {self.title}>'

class PropertyPhoto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100), nullable=False)
    property_id = db.Column(db.Integer, db.ForeignKey('property.id'), nullable=False)
    is_primary = db.Column(db.Boolean, default=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<PropertyPhoto {self.filename}>'

class Offer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, accepted, declined, withdrawn
    message = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    property_id = db.Column(db.Integer, db.ForeignKey('property.id'), nullable=False)
    buyer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    escrow_deposit = db.Column(db.Boolean, default=False)
    legal_agreement = db.Column(db.Boolean, default=False)
    
    def __repr__(self):
        return f'<Offer {self.amount} on {self.property_id}>'

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    property_id = db.Column(db.Integer, db.ForeignKey('property.id'), nullable=False)
    seller_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    buyer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    fee = db.Column(db.Float, nullable=False, default=1500.00)  # Flat fee
    status = db.Column(db.String(20), default='pending')  # pending, completed, cancelled
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    
    property = db.relationship('Property', backref='transaction', uselist=False)
    seller = db.relationship('User', foreign_keys=[seller_id])
    buyer = db.relationship('User', foreign_keys=[buyer_id])
    
    def __repr__(self):
        return f'<Transaction {self.amount} for property {self.property_id}>'

class TransactionStep(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    transaction_id = db.Column(db.Integer, db.ForeignKey('transaction.id'), nullable=False)
    step_name = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, completed, skipped
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    notes = db.Column(db.Text)
    
    transaction = db.relationship('Transaction', backref='steps')
    
    def __repr__(self):
        return f'<TransactionStep {self.step_name} for transaction {self.transaction_id}>'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Helper functions
def save_photo(file):
    """Save uploaded photo with a unique filename"""
    if file:
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4().hex}_{filename}"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(file_path)
        return unique_filename
    return None

def calculate_savings(property_value):
    """Calculate savings compared to traditional agent fees"""
    traditional_fee = property_value * 0.015  # 1.5% commission
    our_fee = 1500  # €1,500 flat fee
    return traditional_fee - our_fee

# Routes
@app.route('/')
def index():
    """Homepage route"""
    featured_properties = Property.query.filter_by(status='active').order_by(Property.created_at.desc()).limit(6).all()
    return render_template('index.html', properties=featured_properties)

@app.route('/about')
def about():
    """About page route"""
    return render_template('about.html')

@app.route('/contact')
def contact():
    """Contact page route"""
    return render_template('contact.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration route"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
        
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        phone = request.form.get('phone')
        
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists. Please use a different email or login.')
            return redirect(url_for('register'))
        
        new_user = User(email=email, first_name=first_name, last_name=last_name, phone=phone)
        new_user.set_password(password)
        
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful! Please log in.')
        return redirect(url_for('login'))
        
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login route"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
        
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('dashboard'))
        else:
            flash('Invalid email or password.')
            
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    """User logout route"""
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    """User dashboard route"""
    # Get user's properties
    properties = Property.query.filter_by(owner_id=current_user.id).all()
    
    # Count active listings
    active_listings = Property.query.filter_by(owner_id=current_user.id, status='active').count()
    
    # Count total offers
    total_offers = sum(len(p.offers) for p in properties)
    
    # Calculate potential savings
    total_property_value = sum(p.price for p in properties)
    potential_savings = calculate_savings(total_property_value)
    
    # Count completed sales
    completed_sales = Property.query.filter_by(owner_id=current_user.id, status='sold').count()
    
    # Get recent offers
    recent_offers = Offer.query.join(Property).filter(Property.owner_id == current_user.id).order_by(Offer.created_at.desc()).limit(5).all()
    
    return render_template('dashboard.html', 
                          properties=properties, 
                          active_listings=active_listings,
                          total_offers=total_offers,
                          potential_savings=potential_savings,
                          completed_sales=completed_sales,
                          recent_offers=recent_offers)

@app.route('/properties/new', methods=['GET', 'POST'])
@login_required
def new_property():
    """Add new property route"""
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        price = float(request.form.get('price'))
        address = request.form.get('address')
        city = request.form.get('city')
        county = request.form.get('county')
        eircode = request.form.get('eircode')
        bedrooms = int(request.form.get('bedrooms'))
        bathrooms = int(request.form.get('bathrooms'))
        size_sqm = float(request.form.get('size_sqm'))
        property_type = request.form.get('property_type')
        
        new_property = Property(
            title=title,
            description=description,
            price=price,
            address=address,
            city=city,
            county=county,
            eircode=eircode,
            bedrooms=bedrooms,
            bathrooms=bathrooms,
            size_sqm=size_sqm,
            property_type=property_type,
            owner_id=current_user.id
        )
        
        db.session.add(new_property)
        db.session.commit()
        
        # Handle photo uploads
        photos = request.files.getlist('photos')
        is_primary = True  # First photo is primary
        
        for photo in photos:
            if photo.filename:
                filename = save_photo(photo)
                if filename:
                    property_photo = PropertyPhoto(
                        filename=filename,
                        property_id=new_property.id,
                        is_primary=is_primary
                    )
                    db.session.add(property_photo)
                    is_primary = False  # Only first photo is primary
        
        db.session.commit()
        flash('Property added successfully!')
        return redirect(url_for('dashboard'))
        
    return render_template('new_property.html')

@app.route('/properties/<int:property_id>')
def view_property(property_id):
    """View property details route"""
    property = Property.query.get_or_404(property_id)
    return render_template('property_details.html', property=property)

@app.route('/properties/<int:property_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_property(property_id):
    """Edit property route"""
    property = Property.query.get_or_404(property_id)
    
    # Make sure user owns this property
    if property.owner_id != current_user.id:
        flash('You do not have permission to edit this property.')
        return redirect(url_for('dashboard'))
        
    if request.method == 'POST':
        property.title = request.form.get('title')
        property.description = request.form.get('description')
        property.price = float(request.form.get('price'))
        property.address = request.form.get('address')
        property.city = request.form.get('city')
        property.county = request.form.get('county')
        property.eircode = request.form.get('eircode')
        property.bedrooms = int(request.form.get('bedrooms'))
        property.bathrooms = int(request.form.get('bathrooms'))
        property.size_sqm = float(request.form.get('size_sqm'))
        property.property_type = request.form.get('property_type')
        
        db.session.commit()
        
        # Handle photo uploads
        photos = request.files.getlist('photos')
        for photo in photos:
            if photo.filename:
                filename = save_photo(photo)
                if filename:
                    property_photo = PropertyPhoto(
                        filename=filename,
                        property_id=property.id,
                        is_primary=False
                    )
                    db.session.add(property_photo)
        
        db.session.commit()
        flash('Property updated successfully!')
        return redirect(url_for('view_property', property_id=property.id))
        
    return render_template('edit_property.html', property=property)

@app.route('/properties/<int:property_id>/delete', methods=['POST'])
@login_required
def delete_property(property_id):
    """Delete property route"""
    property = Property.query.get_or_404(property_id)
    
    # Make sure user owns this property
    if property.owner_id != current_user.id:
        flash('You do not have permission to delete this property.')
        return redirect(url_for('dashboard'))
        
    # Delete property photos from filesystem
    for photo in property.photos:
        try:
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], photo.filename))
        except:
            pass
    
    db.session.delete(property)
    db.session.commit()
    flash('Property deleted successfully!')
    return redirect(url_for('dashboard'))

@app.route('/properties/<int:property_id>/offer', methods=['GET', 'POST'])
@login_required
def make_offer(property_id):
    """Make an offer on a property route"""
    property = Property.query.get_or_404(property_id)
    
    # Make sure user doesn't own this property
    if property.owner_id == current_user.id:
        flash('You cannot make an offer on your own property.')
        return redirect(url_for('view_property', property_id=property.id))
        
    if request.method == 'POST':
        amount = float(request.form.get('amount'))
        message = request.form.get('message')
        legal_agreement = 'legal_agreement' in request.form
        escrow_deposit = 'escrow_deposit' in request.form
        
        # Validate the offer
        if amount <= 0:
            flash('Offer amount must be greater than zero.')
            return redirect(url_for('make_offer', property_id=property.id))
            
        if not legal_agreement or not escrow_deposit:
            flash('You must agree to the legal terms and escrow deposit to make an offer.')
            return redirect(url_for('make_offer', property_id=property.id))
        
        new_offer = Offer(
            amount=amount,
            message=message,
            property_id=property.id,
            buyer_id=current_user.id,
            legal_agreement=legal_agreement,
            escrow_deposit=escrow_deposit
        )
        
        db.session.add(new_offer)
        db.session.commit()
        flash('Your offer has been submitted successfully!')
        return redirect(url_for('view_property', property_id=property.id))
        
    return render_template('make_offer.html', property=property)

@app.route('/offers')
@login_required
def my_offers():
    """View user's offers route"""
    # Offers user has made on properties
    offers_made = Offer.query.filter_by(buyer_id=current_user.id).all()
    
    # Offers received on user's properties
    offers_received = Offer.query.join(Property).filter(Property.owner_id == current_user.id).all()
    
    return render_template('my_offers.html', offers_made=offers_made, offers_received=offers_received)

@app.route('/offers/<int:offer_id>/accept', methods=['POST'])
@login_required
def accept_offer(offer_id):
    """Accept an offer route"""
    offer = Offer.query.get_or_404(offer_id)
    property = Property.query.get(offer.property_id)
    
    # Make sure user owns this property
    if property.owner_id != current_user.id:
        flash('You do not have permission to accept offers on this property.')
        return redirect(url_for('dashboard'))
        
    # Update offer status
    offer.status = 'accepted'
    
    # Update property status
    property.status = 'pending'
    
    # Create transaction record
    transaction = Transaction(
        property_id=property.id,
        seller_id=current_user.id,
        buyer_id=offer.buyer_id,
        amount=offer.amount,
        fee=1500.00  # Flat fee
    )
    
    db.session.add(transaction)
    
    # Mark other offers as declined
    other_offers = Offer.query.filter(Offer.property_id == property.id, Offer.id != offer.id).all()
    for other_offer in other_offers:
        other_offer.status = 'declined'
    
    # Create initial transaction steps
    steps = [
        ('Offer Accepted', 'completed'),
        ('Legal Agreement Signed', 'pending'),
        ('Deposit Received', 'pending'),
        ('Survey Completed', 'pending'),
        ('Finance Approved', 'pending'),
        ('Legal Transfer', 'pending'),
        ('Final Payment', 'pending'),
        ('Transaction Complete', 'pending')
    ]
    
    for step_name, status in steps:
        step = TransactionStep(
            transaction_id=transaction.id,
            step_name=step_name,
            status=status,
            completed_at=datetime.utcnow() if status == 'completed' else None
        )
        db.session.add(step)
    
    db.session.commit()
    flash('Offer accepted successfully! The transaction process has begun.')
    return redirect(url_for('transaction_details', transaction_id=transaction.id))

@app.route('/offers/<int:offer_id>/decline', methods=['POST'])
@login_required
def decline_offer(offer_id):
    """Decline an offer route"""
    offer = Offer.query.get_or_404(offer_id)
    property = Property.query.get(offer.property_id)
    
    # Make sure user owns this property
    if property.owner_id != current_user.id:
        flash('You do not have permission to decline offers on this property.')
        return redirect(url_for('dashboard'))
        
    # Update offer status
    offer.status = 'declined'
    db.session.commit()
    
    flash('Offer declined successfully.')
    return redirect(url_for('view_property', property_id=property.id))

@app.route('/transactions')
@login_required
def my_transactions():
    """View user's transactions route"""
    # Transactions where user is seller
    selling_transactions = Transaction.query.filter_by(seller_id=current_user.id).all()
    
    # Transactions where user is buyer
    buying_transactions = Transaction.query.filter_by(buyer_id=current_user.id).all()
    
    return render_template('my_transactions.html', 
                          selling_transactions=selling_transactions, 
                          buying_transactions=buying_transactions)

@app.route('/transactions/<int:transaction_id>')
@login_required
def transaction_details(transaction_id):
    """View transaction details route"""
    transaction = Transaction.query.get_or_404(transaction_id)
    
    # Make sure user is either seller or buyer
    if transaction.seller_id != current_user.id and transaction.buyer_id != current_user.id:
        flash('You do not have permission to view this transaction.')
        return redirect(url_for('dashboard'))
        
    property = Property.query.get(transaction.property_id)
    steps = TransactionStep.query.filter_by(transaction_id=transaction.id).order_by(TransactionStep.id).all()
    
    return render_template('transaction_details.html', 
                          transaction=transaction, 
                          property=property, 
                          steps=steps)

@app.route('/transactions/<int:transaction_id>/step/<int:step_id>/complete', methods=['POST'])
@login_required
def complete_transaction_step(transaction_id, step_id):
    """Complete a transaction step route"""
    transaction = Transaction.query.get_or_404(transaction_id)
    step = TransactionStep.query.get_or_404(step_id)
    
    # Make sure user is either seller or buyer and step belongs to transaction
    if (transaction.seller_id != current_user.id and transaction.buyer_id != current_user.id) or step.transaction_id != transaction.id:
        flash('You do not have permission to update this transaction step.')
        return redirect(url_for('dashboard'))
        
    # Update step status
    step.status = 'completed'
    step.completed_at = datetime.utcnow()
    step.notes = request.form.get('notes', '')
    
    # Check if all steps are completed
    all_steps = TransactionStep.query.filter_by(transaction_id=transaction.id).all()
    all_completed = all(s.status == 'completed' for s in all_steps)
    
    # If all steps are completed, mark transaction as completed
    if all_completed:
        transaction.status = 'completed'
        transaction.completed_at = datetime.utcnow()
        
        # Update property status
        property = Property.query.get(transaction.property_id)
        property.status = 'sold'
    
    db.session.commit()
    flash('Transaction step marked as completed!')
    return redirect(url_for('transaction_details', transaction_id=transaction.id))

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """User profile route"""
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        phone = request.form.get('phone')
        
        current_user.first_name = first_name
        current_user.last_name = last_name
        current_user.phone = phone
        
        # Handle password change if provided
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        
        if current_password and new_password and confirm_password:
            if not current_user.check_password(current_password):
                flash('Current password is incorrect.')
                return redirect(url_for('profile'))
                
            if new_password != confirm_password:
                flash('New passwords do not match.')
                return redirect(url_for('profile'))
                
            current_user.set_password(new_password)
            flash('Password updated successfully.')
        
        db.session.commit()
        flash('Profile updated successfully!')
        return redirect(url_for('profile'))
        
    return render_template('profile.html')

@app.route('/search')
def search_properties():
    """Search properties route"""
    query = request.args.get('query', '')
    city = request.args.get('city', '')
    min_price = request.args.get('min_price', 0, type=float)
    max_price = request.args.get('max_price', 100000000, type=float)
    bedrooms = request.args.get('bedrooms', 0, type=int)
    property_type = request.args.get('property_type', '')
    
    # Build the query
    properties_query = Property.query.filter_by(status='active')
    
    if query:
        properties_query = properties_query.filter(
            (Property.title.contains(query)) |
            (Property.description.contains(query)) |
            (Property.address.contains(query))
        )
        
    if city:
        properties_query = properties_query.filter(Property.city == city)
        
    if min_price:
        properties_query = properties_query.filter(Property.price >= min_price)
        
    if max_price:
        properties_query = properties_query.filter(Property.price <= max_price)
        
    if bedrooms:
        properties_query = properties_query.filter(Property.bedrooms >= bedrooms)
        
    if property_type:
        properties_query = properties_query.filter(Property.property_type == property_type)
        
    properties = properties_query.order_by(Property.created_at.desc()).all()
    
    return render_template('search_results.html', 
                          properties=properties,
                          query=query,
                          city=city,
                          min_price=min_price,
                          max_price=max_price,
                          bedrooms=bedrooms,
                          property_type=property_type)

@app.route('/api/calculate-savings', methods=['POST'])
def api_calculate_savings():
    """API endpoint to calculate savings"""
    property_value = request.json.get('property_value', 0)
    savings = calculate_savings(float(property_value))
    
    return jsonify({
        'property_value': property_value,
        'traditional_fee': property_value * 0.015,
        'our_fee': 1500,
        'savings': savings
    })

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

# Create database tables if they don't exist
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
