# Ecom

Ecom is a Django-based ecommerce web application that allows users to browse products, manage a shopping cart, and place orders. The project is structured with dedicated folders for the main Django configuration, store logic, static assets, and uploaded media.

## Project structure

The repository currently contains the following main files and folders:

- `manage.py` – Django management entry point
- `cartecom/` – Main Django project configuration
- `store/` – App for product and shopping-related functionality
- `static/` – Static files such as CSS, JavaScript, and images
- `media/` – Uploaded media files
- `db.sqlite3` – SQLite database for local development

## Features

This project is designed to support core ecommerce functionality such as:

- Product listing and browsing
- Shopping cart management
- Django admin support
- Static and media file handling
- Store app integration within a Django project structure

> Update this section further if your project includes login, checkout, payment, order history, or category filtering.

## Requirements

Make sure the following are installed:

- Python 3.x
- pip
- virtualenv (optional but recommended)

## Installation

1. Clone the repository:

```bash
git clone https://github.com/adithyasagarmk-coder/ecom.git
cd ecom
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
```

For Windows:

```bash
venv\Scripts\activate
```

For Linux/macOS:

```bash
source venv/bin/activate
```

3. Install dependencies:

```bash
pip install django
```

If you create a `requirements.txt` file, use:

```bash
pip install -r requirements.txt
```

## Apply migrations

Run the following command to apply database migrations:

```bash
python manage.py migrate
```

## Run the server

Start the development server with:

```bash
python manage.py runserver
```

Then open:

`http://127.0.0.1:8000/`

## Admin access

To create an admin user:

```bash
python manage.py createsuperuser
```

Then log in through the Django admin panel, usually available at:

`http://127.0.0.1:8000/admin/`

## Static and media files

- Static files are stored in the `static/` folder
- Uploaded files are stored in the `media/` folder

Make sure your Django `settings.py` is configured correctly for static and media handling during development.

## Database

This project currently uses SQLite for development through the `db.sqlite3` file. For production, it is better to switch to PostgreSQL or MySQL.

## Future improvements

Possible enhancements for this project include:

- User authentication and registration
- Product categories and search
- Checkout and billing flow
- Order history
- Payment gateway integration
- Deployment configuration

## License

This project is for learning and development purposes. Add a license here if needed.
