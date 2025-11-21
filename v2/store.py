import json

class Product:
    """Клас для представлення товару"""
    def __init__(self, id, name, price, qty):
        self.id = id
        self.name = name
        self.price = price
        self.qty = qty

class Store:
    """Клас для управління магазином"""
    def __init__(self):
        self.products = []
        self._load()
    
    def _load(self):
        try:
            with open("products.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                self.products = [Product(p['id'], p['name'], p['price'], p['qty']) for p in data]
        except:
            self.products = []
    
    def _save(self):
        data = [{'id': p.id, 'name': p.name, 'price': p.price, 'qty': p.qty} for p in self.products]
        with open("products.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def add_product(self, name, price, qty):
        pid = max([p.id for p in self.products], default=0) + 1
        self.products.append(Product(pid, name, price, qty))
        self._save()
    
    def find_product(self, pid):
        for p in self.products:
            if p.id == pid:
                return p
        return None
    
    def edit_product(self, pid, name, price, qty):
        prod = self.find_product(pid)
        if prod:
            prod.name = name
            prod.price = price
            prod.qty = qty
            self._save()
    
    def remove_product(self, pid):
        self.products = [p for p in self.products if p.id != pid]
        self._save()