from flask import Blueprint, request, jsonify
from models.fridge_product import FridgeProduct
from models.product import Product

fridge_routes = Blueprint("fridge_routes", __name__)


@fridge_routes.route("/api/fridges", methods=["GET"])
def get_fridges():
    """Fetch only Fridge products from the product list."""
    products = Product.load_products()
    # Ensure it's a Fridge
    fridges = {k: v for k, v in products.items() if "capacity_l" in v}
    return jsonify(fridges)


@fridge_routes.route("/api/fridges", methods=["POST"])
def add_fridge():
    """Add a new Fridge product to products.json."""
    data = request.json
    required_fields = ["product_id", "name", "brand", "price", "stock",
                       "threshold", "discontinued", "image_url", "capacity_l", "energy_rating"]

    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400

    try:
        product = FridgeProduct.create_fridge(data)
        return jsonify({"message": "Fridge Product added successfully", "product": product}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
