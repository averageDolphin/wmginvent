from flask import Blueprint, request, jsonify
from models.order import Order

order_routes = Blueprint("order_routes", __name__)


@order_routes.route("/api/orders", methods=["GET"])
def get_all_orders():
    """Fetch all orders."""
    orders = Order.load_all_orders()
    return jsonify(orders)


@order_routes.route("/api/orders/<order_id>", methods=["GET"])
def get_order(order_id):
    """Fetch a specific order by ID."""
    try:
        order = Order.load_order(order_id)
        return jsonify(order)
    except FileNotFoundError:
        return jsonify({"error": "Order not found"}), 404


@order_routes.route("/api/orders", methods=["POST"])
def create_order():
    """Create a new order with input validation."""
    data = request.json
    required_fields = ["customer_name", "email", "items"]

    # Validate required fields
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400

    try:
        order = Order.create_order(
            data["customer_name"], data["email"], data["items"])
        return jsonify({"message": "Order created successfully", "order": order}), 201
    except ValueError as e:
        # Return validation error messages
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Something went wrong", "details": str(e)}), 500


@order_routes.route("/api/orders/<order_id>", methods=["PUT"])
def update_order(order_id):
    """Update an existing order (e.g., change status)."""
    updates = request.json

    updated_order = Order.update_order(order_id, updates)
    if not updated_order:
        return jsonify({"error": "Order not found"}), 404

    return jsonify({"message": "Order updated successfully", "order": updated_order})


@order_routes.route("/api/orders/<order_id>", methods=["DELETE"])
def delete_order(order_id):
    """Delete an order."""
    success = Order.delete_order(order_id)

    if not success:
        return jsonify({"error": "Order not found"}), 404

    return jsonify({"message": "Order deleted successfully"})
