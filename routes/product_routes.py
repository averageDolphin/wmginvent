from flask import Blueprint, request, jsonify
from models.product import Product

product_routes = Blueprint("product_routes", __name__)


@product_routes.route("/api/products", methods=["GET"])
def get_all_products():
    """Fetch all products."""
    return jsonify(Product.load_products())


@product_routes.route("/api/products/<product_id>", methods=["GET"])
def get_product(product_id):
    """Fetch a single product by ID."""
    product = Product.get_product(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    return jsonify(product)


@product_routes.route("/api/products", methods=["POST"])
def create_product():
    """Create a new product."""
    data = request.json
    required_fields = ["product_id", "name", "brand", "price",
                       "stock", "threshold", "discontinued", "image_url"]

    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400

    try:
        product = Product.create_product(data)
        return jsonify({"message": "Product added successfully", "product": product}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@product_routes.route("/api/products/<product_id>", methods=["PUT"])
def update_product(product_id):
    """Update an existing product."""
    updates = request.json
    updated_product = Product.update_product(product_id, updates)

    if not updated_product:
        return jsonify({"error": "Product not found"}), 404

    return jsonify({"message": "Product updated successfully", "product": updated_product})


@product_routes.route("/api/products/<product_id>", methods=["DELETE"])
def delete_product(product_id):
    """Delete a product."""
    success = Product.delete_product(product_id)

    if not success:
        return jsonify({"error": "Product not found"}), 404

    return jsonify({"message": "Product deleted successfully"})
