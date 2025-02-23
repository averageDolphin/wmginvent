from models.product import Product


class TVProduct(Product):
    def __init__(self, product_id, name, brand, price, stock, threshold, discontinued, image_url, resolution, panel_type):
        super().__init__(product_id, name, brand, price,
                         stock, threshold, discontinued, image_url)
        self.resolution = resolution
        self.panel_type = panel_type

    def to_dict(self):
        """Converts TV product object to dictionary format."""
        product_dict = super().to_dict()  # Inherit base attributes
        product_dict.update({
            "resolution": self.resolution,
            "panel_type": self.panel_type
        })
        return product_dict

    @staticmethod
    def create_tv(data):
        """Create a new TV product and save it."""
        products = Product.load_products()
        if data["product_id"] in products:
            raise ValueError("Product ID already exists.")

        new_tv = TVProduct(**data)
        products[new_tv.product_id] = new_tv.to_dict()
        Product.save_products(products)
        return new_tv.to_dict()
