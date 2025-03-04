from flask import Blueprint, request, jsonify
from models.tv_product import TVProduct
from models.product import Product

tv_routes = Blueprint("tv_routes", __name__)


@tv_routes.route("/api/tvs", methods=["GET"])
def get_tvs():
    """Fetch only TV products from the product list."""
    products = Product.load_products()
    # Ensure it's a TV
    tvs = {k: v for k, v in products.items() if "resolution" in v}
    return jsonify(tvs)


@tv_routes.route("/api/tvs", methods=["POST"])
def add_tv():
    """Add a new TV product to products.json."""
    data = request.json
    required_fields = ["product_id", "name", "brand", "price", "stock",
                       "threshold", "discontinued", "image_url", "resolution", "panel_type"]

    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400

    try:
        product = TVProduct.create_tv(data)
        return jsonify({"message": "TV Product added successfully", "product": product}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
