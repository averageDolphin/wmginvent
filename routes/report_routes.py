from flask import Blueprint, jsonify
from models.report import Report

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
