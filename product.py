class Product:
    def __init__(self, pid, name, price, qty):
        self.id = pid
        self.name = name
        self.price = price
        self.qty = qty

    def to_dict(self):
        return {"id": self.id, "name": self.name, "price": self.price, "qty": self.qty}

    @staticmethod
    def from_dict(d):
        return Product(d["id"], d["name"], d["price"], d["qty"])