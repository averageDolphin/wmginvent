from models.product import Product


class FridgeProduct(Product):
    def __init__(self, product_id, name, brand, price, stock, threshold, discontinued, image_url, capacity_l, energy_rating):
        super().__init__(product_id, name, brand, price,
                         stock, threshold, discontinued, image_url)
        self.capacity_l = capacity_l
        self.energy_rating = energy_rating

    def to_dict(self):
        """Converts Fridge product object to dictionary format."""
        product_dict = super().to_dict()  # Inherit base attributes
        product_dict.update({
            "capacity_l": self.capacity_l,
            "energy_rating": self.energy_rating
        })
        return product_dict

    @staticmethod
    def create_fridge(data):
        """Create a new Fridge product and save it."""
        products = Product.load_products()
        if data["product_id"] in products:
            raise ValueError("Product ID already exists.")

        new_fridge = FridgeProduct(**data)
        products[new_fridge.product_id] = new_fridge.to_dict()
        Product.save_products(products)
        return new_fridge.to_dict()
