import json
import os
import time
import re
from models.product import Product


class Order:
    def __init__(self, order_id, customer_name, email, items, status="pending"):
        self.order_id = order_id
        self.customer_name = customer_name
        self.email = email
        self.items = items
        """List of purchased items"""
        self.status = status  # "pending", "shipped", "completed"
        """"pending", "shipped", "completed\""""

    def to_dict(self):
        """Convert order object to dictionary."""
        return self.__dict__

    @staticmethod
    def load_order(order_id):
        """Load an order from a specific file."""
        file_path = f"data/orders/{order_id}.json"

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Order {order_id} not found.")

        with open(file_path, "r") as file:
            return json.load(file)

    @staticmethod
    def save_order(order_id, order_data):
        """Save an order to a separate JSON file."""
        file_path = f"data/orders/{order_id}.json"

        with open(file_path, "w") as file:
            json.dump(order_data, file, indent=4)

    @staticmethod
    def is_valid_email(email):
        """Validate email format."""
        email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(email_regex, email) is not None

    @staticmethod
    def validate_items(items):
        """Ensure all items exist in the product catalog and have enough stock."""
        products = Product.load_products()

        for item in items:
            product_id = item["product_id"]
            quantity = item["quantity"]

            if product_id not in products:
                return False, f"Product ID {product_id} does not exist."

            if quantity > products[product_id]["stock"]:
                return False, f"Not enough stock for {product_id}. Available: {products[product_id]['stock']}."

        return True, None  # Validation passed

    @staticmethod
    def create_order(customer_name, email, items):
        """Creates a new order with input validation and stock deduction."""
        if not customer_name.strip():
            raise ValueError("Customer name cannot be empty.")

        if not Order.is_valid_email(email):
            raise ValueError("Invalid email format.")

        is_valid, error_message = Order.validate_items(items)
        if not is_valid:
            raise ValueError(error_message)

        # Deduct stock for each ordered product
        products = Product.load_products()
        for item in items:
            product_id = item["product_id"]
            quantity = item["quantity"]
            products[product_id]["stock"] -= quantity

        Product.save_products(products)

        order_id = f"ORD{int(time.time())}"
        new_order = Order(order_id, customer_name, email, items)

        Order.save_order(order_id, new_order.to_dict())
        return new_order.to_dict()

    @staticmethod
    def load_all_orders():
        """Load all orders from the orders directory."""
        orders_dir = "data/orders/"
        if not os.path.exists(orders_dir):
            return {}

        orders = {}
        for order_file in os.listdir(orders_dir):
            with open(os.path.join(orders_dir, order_file), "r") as file:
                order_data = json.load(file)
                orders[order_data["order_id"]] = order_data

        return orders

    @staticmethod
    def update_order(order_id, updates):
        """Update an existing order's details."""
        try:
            order = Order.load_order(order_id)
        except FileNotFoundError:
            return None

        order.update(updates)
        Order.save_order(order_id, order)
        return order

    @staticmethod
    def delete_order(order_id):
        """Delete an order by ID."""
        file_path = f"data/orders/{order_id}.json"

        if os.path.exists(file_path):
            os.remove(file_path)
            return True
        return False
