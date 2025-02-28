from flask import Blueprint, jsonify, request
from models.report import Report
import os
import json
from datetime import datetime

report_routes = Blueprint("report_routes", __name__)


@report_routes.route("/api/reports/sales", methods=["GET"])
def get_sales_report():
    """Fetch sales report."""
    report = Report.generate_sales_report()
    return jsonify(report)


@report_routes.route("/api/reports/stock", methods=["GET"])
def get_stock_report():
    """Fetch stock report."""
    report = Report.generate_stock_report()
    return jsonify(report)


ORDERS_FOLDER = "data/orders"
PRODUCTS_FILE = "data/products.json"

@report_routes.route("/api/reports/sales", methods=["GET"])
def sales_report():
    """Generate sales report"""
    if not os.path.exists(ORDERS_FOLDER):
        return jsonify({"error": "No orders found"}), 404

    # Load product prices
    products = {}
    if os.path.exists(PRODUCTS_FILE):
        with open(PRODUCTS_FILE, "r") as file:
            products = json.load(file)

    sales = {}
    total_orders = 0

    for filename in os.listdir(ORDERS_FOLDER):
        if filename.endswith(".json"):
            filepath = os.path.join(ORDERS_FOLDER, filename)
            try:
                with open(filepath, "r") as file:
                    order = json.load(file)
                    total_orders += 1  # Count orders

                    for item in order["items"]:
                        product_id = item.get("product_id")
                        quantity = item.get("quantity", 0)
                        price = products.get(product_id, {}).get("price", 0)

                        if product_id not in sales:
                            sales[product_id] = {"units_sold": 0, "total_revenue": 0}

                        sales[product_id]["units_sold"] += quantity
                        sales[product_id]["total_revenue"] += price * quantity

            except json.JSONDecodeError:
                print(f"Skipping invalid JSON file: {filename}")

    return jsonify({"product_sales": sales, "total_orders": total_orders})

@report_routes.route("/api/reports/stock", methods=["GET"])
def stock_report():
    """Generate low-stock report"""
    if not os.path.exists(PRODUCTS_FILE):
        return jsonify({"error": "Products file not found"}), 404

    with open(PRODUCTS_FILE, "r") as file:
        products = json.load(file)

    low_stock = {
        pid: {"name": p["name"], "stock": p["stock"]}
        for pid, p in products.items() if p["stock"] <= p.get("threshold", 5)
    }

    return jsonify({"low_stock_products": low_stock})
