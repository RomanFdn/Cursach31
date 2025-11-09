import json
from product import Product

class Store:
    def __init__(self):
        self.products = []
        self._load()

    def _load(self):
        try:
            with open("products.json", "r", encoding="utf-8") as f:
                self.products = [Product.from_dict(p) for p in json.load(f)]
        except:
            self.products = []

    def _save(self):
        with open("products.json", "w", encoding="utf-8") as f:
            json.dump([p.to_dict() for p in self.products], f, ensure_ascii=False, indent=2)

    def add_product(self, name, price, qty):
        pid = max([p.id for p in self.products], default=0) + 1
        self.products.append(Product(pid, name, price, qty))
        self._save()

    def edit_product(self, pid, name, price, qty):
        for p in self.products:
            if p.id == pid:
                p.name = name
                p.price = price
                p.qty = qty
        self._save()

    def remove_product(self, pid):
        self.products = [p for p in self.products if p.id != pid]
        self._save()

    def find_product(self, pid):
        for p in self.products:
            if p.id == pid:
                return p
        return None