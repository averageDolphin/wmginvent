from flask import Blueprint, request, jsonify
from models.order import Order
import time
import os

order_routes = Blueprint("order_routes", __name__)


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
    """Create a new order and save it as a separate JSON file."""
    data = request.json
    order_id = f"ORD{int(time.time())}"  # Generate a unique order ID
    Order.save_order(order_id, data)
    return jsonify({"message": "Order created successfully", "order_id": order_id}), 201


@order_routes.route("/api/orders/<order_id>", methods=["PUT"])
def update_order(order_id):
    """Update order details (e.g., status)."""
    data = request.json

    try:
        order = Order.load_order(order_id)
    except FileNotFoundError:
        return jsonify({"error": "Order not found"}), 404

    order.update(data)  # Update order details
    Order.save_order(order_id, order)

    return jsonify({"message": "Order updated successfully"}), 200


@order_routes.route("/api/orders/<order_id>", methods=["DELETE"])
def delete_order(order_id):
    """Delete an order."""
    file_path = f"data/orders/{order_id}.json"

    if not os.path.exists(file_path):
        return jsonify({"error": "Order not found"}), 404

    os.remove(file_path)  # Delete order file
    return jsonify({"message": "Order deleted successfully"}), 200
