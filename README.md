# IKW Store - Shopping Web Application

A Flask-based shopping web application developed for observational case study on AI-assisted software development.

## Features

- **Home Page**: Shop information with logo and contact details
- **Product List**: 20 computer accessory products with grid display
- **Search Functionality**: Case-insensitive product search
- **Star Rating**: Rate products from 1-5 stars
- **Shopping Cart**: Add, remove, and update product quantities
- **Enquiry Form**: Contact form with validation
- **Responsive Design**: Mobile-friendly interface

## Technology Stack

- Python 3.11+
- Flask 2.x
- Jinja2 templating
- CSS3 for styling

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python app.py
```

3. Open your browser and navigate to:
```
http://localhost:5000
```

## Shop Information

- **Shop Name**: IKW store
- **Contact Name**: Waichi Ikeda
- **Email**: W.Ikeda@liverpool.ac.uk
- **Phone**: +81 00-000-0000

## Project Structure

```
/workspace/
??? app.py                  # Main Flask application
??? requirements.txt        # Python dependencies
??? templates/              # HTML templates
?   ??? base.html          # Base template with navigation
?   ??? home.html          # Home page
?   ??? products.html      # Product list
?   ??? cart.html          # Shopping cart
?   ??? checkout.html      # Checkout page
?   ??? enquiry.html       # Contact form
?   ??? confirmation.html  # Form confirmation
??? static/                # Static assets
    ??? css/
    ?   ??? style.css      # Application styles
    ??? images/
        ??? IKWStoreLogo.png

```

## Notes

- Checkout is for demonstration only (no payment processing)
- Enquiry form does not send emails (demonstration mode)
- Session-based cart and rating storage
