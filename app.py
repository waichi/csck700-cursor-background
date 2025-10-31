from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.utils import escape
import secrets
import re

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# Product data - 20 computer accessory products
PRODUCTS = [
    {"id": 1, "name": "Wireless Mouse", "description": "Ergonomic wireless mouse with 6 buttons", "price": 3500, "image": "mouse.jpg"},
    {"id": 2, "name": "Mechanical Keyboard", "description": "RGB backlit mechanical gaming keyboard", "price": 12000, "image": "keyboard.jpg"},
    {"id": 3, "name": "USB-C Hub", "description": "7-in-1 USB-C hub with HDMI and SD card reader", "price": 5500, "image": "hub.jpg"},
    {"id": 4, "name": "Laptop Stand", "description": "Adjustable aluminum laptop stand", "price": 4200, "image": "stand.jpg"},
    {"id": 5, "name": "Webcam HD", "description": "1080p HD webcam with built-in microphone", "price": 7800, "image": "webcam.jpg"},
    {"id": 6, "name": "External SSD 1TB", "description": "Portable 1TB solid state drive", "price": 15000, "image": "ssd.jpg"},
    {"id": 7, "name": "Monitor 24 inch", "description": "Full HD IPS monitor with thin bezels", "price": 14500, "image": "monitor.jpg"},
    {"id": 8, "name": "Headset with Mic", "description": "Noise-canceling headset with boom microphone", "price": 6500, "image": "headset.jpg"},
    {"id": 9, "name": "HDMI Cable 2m", "description": "High-speed HDMI 2.1 cable", "price": 1500, "image": "hdmi.jpg"},
    {"id": 10, "name": "USB Flash Drive 64GB", "description": "High-speed USB 3.0 flash drive", "price": 1200, "image": "usb.jpg"},
    {"id": 11, "name": "Mousepad XL", "description": "Extra-large gaming mousepad with non-slip base", "price": 2500, "image": "mousepad.jpg"},
    {"id": 12, "name": "Laptop Cooling Pad", "description": "Cooling pad with adjustable fans", "price": 3800, "image": "cooling.jpg"},
    {"id": 13, "name": "Cable Organizer", "description": "Desktop cable management system", "price": 1000, "image": "organizer.jpg"},
    {"id": 14, "name": "Screen Cleaner Kit", "description": "Professional screen cleaning kit", "price": 1800, "image": "cleaner.jpg"},
    {"id": 15, "name": "Wireless Charger", "description": "Fast wireless charging pad", "price": 3200, "image": "charger.jpg"},
    {"id": 16, "name": "Bluetooth Speaker", "description": "Portable Bluetooth speaker with bass boost", "price": 5800, "image": "speaker.jpg"},
    {"id": 17, "name": "Graphics Tablet", "description": "Digital drawing tablet with stylus", "price": 8900, "image": "tablet.jpg"},
    {"id": 18, "name": "Document Scanner", "description": "Portable document scanner", "price": 11000, "image": "scanner.jpg"},
    {"id": 19, "name": "Ergonomic Wrist Rest", "description": "Memory foam wrist rest for keyboard", "price": 2200, "image": "wrist.jpg"},
    {"id": 20, "name": "LED Desk Lamp", "description": "Adjustable LED desk lamp with USB port", "price": 4500, "image": "lamp.jpg"}
]

# Shop information
SHOP_INFO = {
    "name": "IKW store",
    "contact_name": "Waichi Ikeda",
    "email": "W.Ikeda@liverpool.ac.uk",
    "phone": "+81 00-000-0000"
}

def init_session():
    """Initialize session variables if not present"""
    if 'cart' not in session:
        session['cart'] = {}
    if 'ratings' not in session:
        session['ratings'] = {}

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def sanitize_input(text):
    """Sanitize user input to prevent injection attacks"""
    return escape(text)

@app.route('/')
def home():
    """Home page route"""
    init_session()
    return render_template('home.html', shop=SHOP_INFO)

@app.route('/products')
def products():
    """Product list page with search functionality"""
    init_session()
    search_query = request.args.get('search', '').strip()
    
    if search_query:
        # Case-insensitive search
        filtered_products = [p for p in PRODUCTS if search_query.lower() in p['name'].lower()]
    else:
        filtered_products = PRODUCTS
    
    return render_template('products.html', products=filtered_products, search_query=search_query, shop=SHOP_INFO, ratings=session.get('ratings', {}))

@app.route('/rate/<int:product_id>/<int:rating>')
def rate_product(product_id, rating):
    """Rate a product"""
    init_session()
    if 1 <= rating <= 5:
        ratings = session.get('ratings', {})
        ratings[str(product_id)] = rating
        session['ratings'] = ratings
        session.modified = True
    return redirect(url_for('products'))

@app.route('/cart')
def cart():
    """Shopping cart page"""
    init_session()
    cart_items = []
    total = 0
    
    for product_id, quantity in session['cart'].items():
        product = next((p for p in PRODUCTS if p['id'] == int(product_id)), None)
        if product:
            subtotal = product['price'] * quantity
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'subtotal': subtotal
            })
            total += subtotal
    
    return render_template('cart.html', cart_items=cart_items, total=total, shop=SHOP_INFO)

@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    """Add product to cart"""
    init_session()
    cart = session.get('cart', {})
    product_id_str = str(product_id)
    
    if product_id_str in cart:
        cart[product_id_str] += 1
    else:
        cart[product_id_str] = 1
    
    session['cart'] = cart
    session.modified = True
    return redirect(url_for('products'))

@app.route('/update_cart/<int:product_id>/<int:quantity>')
def update_cart(product_id, quantity):
    """Update quantity of product in cart"""
    init_session()
    cart = session.get('cart', {})
    product_id_str = str(product_id)
    
    if quantity > 0:
        cart[product_id_str] = quantity
    elif product_id_str in cart:
        del cart[product_id_str]
    
    session['cart'] = cart
    session.modified = True
    return redirect(url_for('cart'))

@app.route('/remove_from_cart/<int:product_id>')
def remove_from_cart(product_id):
    """Remove product from cart"""
    init_session()
    cart = session.get('cart', {})
    product_id_str = str(product_id)
    
    if product_id_str in cart:
        del cart[product_id_str]
    
    session['cart'] = cart
    session.modified = True
    return redirect(url_for('cart'))

@app.route('/checkout')
def checkout():
    """Checkout page (demonstration only)"""
    init_session()
    cart_items = []
    total = 0
    
    for product_id, quantity in session['cart'].items():
        product = next((p for p in PRODUCTS if p['id'] == int(product_id)), None)
        if product:
            subtotal = product['price'] * quantity
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'subtotal': subtotal
            })
            total += subtotal
    
    return render_template('checkout.html', cart_items=cart_items, total=total, shop=SHOP_INFO)

@app.route('/enquiry', methods=['GET', 'POST'])
def enquiry():
    """Enquiry form page"""
    init_session()
    if request.method == 'POST':
        # Get form data
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        subject = request.form.get('subject', '').strip()
        message = request.form.get('message', '').strip()
        
        # Validation
        errors = []
        if not name:
            errors.append('Name is required')
        if not email:
            errors.append('Email is required')
        elif not validate_email(email):
            errors.append('Invalid email format')
        if not subject:
            errors.append('Subject is required')
        if not message:
            errors.append('Message is required')
        
        if errors:
            for error in errors:
                flash(error, 'error')
            return render_template('enquiry.html', shop=SHOP_INFO, name=name, email=email, subject=subject, message=message)
        
        # Sanitize inputs
        safe_name = sanitize_input(name)
        safe_email = sanitize_input(email)
        safe_subject = sanitize_input(subject)
        safe_message = sanitize_input(message)
        
        return render_template('confirmation.html', shop=SHOP_INFO, 
                             name=safe_name, email=safe_email, 
                             subject=safe_subject, message=safe_message)
    
    return render_template('enquiry.html', shop=SHOP_INFO)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
