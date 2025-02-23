import json
import os

PRODUCTS_FILE = "data/products.json"


class Product:
    def __init__(self, product_id, name, brand, price, stock, threshold, discontinued, image_url):
        self.product_id = product_id
        self.name = name
        self.brand = brand
        self.price = price
        self.stock = stock
        self.threshold = threshold
        self.discontinued = discontinued
        self.image_url = image_url

    def to_dict(self):
        """Convert product object to dictionary."""
        return self.__dict__

    @staticmethod
    def load_products():
        """Load all products from JSON file, or create an empty one if missing."""
        if not os.path.exists(PRODUCTS_FILE):
            return {}

        try:
            with open(PRODUCTS_FILE, "r") as file:
                return json.load(file) or {}
        except json.JSONDecodeError:
            raise ValueError("Error: products.json is corrupted.")

    @staticmethod
    def save_products(products):
        """Save updated products to JSON file."""
        with open(PRODUCTS_FILE, "w") as file:
            json.dump(products, file, indent=4)

    @staticmethod
    def get_product(product_id):
        """Fetch a single product by ID."""
        products = Product.load_products()
        return products.get(product_id, None)

    @staticmethod
    def create_product(data):
        """Create a new product and save it."""
        products = Product.load_products()
        if data["product_id"] in products:
            raise ValueError("Product ID already exists.")

        new_product = Product(**data)
        products[new_product.product_id] = new_product.to_dict()
        Product.save_products(products)
        return new_product.to_dict()

    @staticmethod
    def update_product(product_id, updates):
        """Update an existing product."""
        products = Product.load_products()
        if product_id not in products:
            return None

        products[product_id].update(updates)
        Product.save_products(products)
        return products[product_id]

    @staticmethod
    def delete_product(product_id):
        """Delete a product by ID."""
        products = Product.load_products()
        if product_id in products:
            del products[product_id]
            Product.save_products(products)
            return True
        return False
