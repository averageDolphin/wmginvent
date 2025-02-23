import json
import os


class Report:
    @staticmethod
    def generate_sales_report():
        """Generates a sales report by aggregating data from all orders."""
        orders_dir = "data/orders/"
        total_revenue = 0
        total_orders = 0
        product_sales = {}

        for order_file in os.listdir(orders_dir):
            with open(os.path.join(orders_dir, order_file), "r") as file:
                order = json.load(file)
                total_orders += 1

                for item in order["items"]:
                    product_id = item["product_id"]
                    quantity = item["quantity"]
                    # Assume price is stored in each order item
                    price = item.get("price", 0)

                    total_revenue += price * quantity
                    product_sales[product_id] = product_sales.get(
                        product_id, 0) + quantity

        return {
            "total_revenue": total_revenue,
            "total_orders": total_orders,
            "product_sales": product_sales
        }

    @staticmethod
    def generate_stock_report():
        """Generates a stock report showing low-stock products."""
        with open("data/products.json", "r") as file:
            products = json.load(file)

        low_stock_products = {
            pid: p for pid, p in products.items() if p["stock"] < p["threshold"]}

        return {
            "low_stock_products": low_stock_products
        }
