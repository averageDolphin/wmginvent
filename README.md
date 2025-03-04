# WMGInvent Inventory Management System

WMGInvent is a web-based inventory management system built using Python and Flask. It offers a simple, intuitive interface for authorised users to manage TV products, track inventory levels, view order history, and generate basic reports.

## Features

- **User Authentication:** Secure login/logout using Flask-Login.
- **Product Management:** Add, edit, delete, and view TV product details.
- **Dynamic Search:** Real-time search for quick product lookup.
- **Dashboard:** Displays inventory statistics and sales overview.
- **Reporting:** Basic reporting of stock levels and sales trends.
- **RESTful API:** CRUD operations via API endpoints.

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/averageDolphin/wmginvent.git
   cd wmginvent
   ```

2. **Set up a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Run the application:**
    ```bash
    python app.py
    ```

Access the app at http://127.0.0.1:5000/dashboard

## Testing

To run the automated tests:

1. Ensure you have installed all dependencies via:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the tests with:
   ```bash
   pytest
   ```