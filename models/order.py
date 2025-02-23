import json
import os


class Order:
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
