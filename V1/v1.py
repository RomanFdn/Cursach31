import json

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


class Order:
    def __init__(self, oid, items, contact):
        self.id = oid
        self.items = items  # list of (product_id, count)
        self.contact = contact

    def to_dict(self):
        return {"id": self.id, "items": self.items, "contact": self.contact}

    @staticmethod
    def from_dict(d):
        return Order(d["id"], d["items"], d["contact"])


class Store:
    def __init__(self):
        self.products = []
        self.orders = []
        self.load()

    def load(self):
        try:
            with open("products.json", "r", encoding="utf-8") as f:
                self.products = [Product.from_dict(p) for p in json.load(f)]
        except: self.products = []
        try:
            with open("orders.json", "r", encoding="utf-8") as f:
                self.orders = [Order.from_dict(o) for o in json.load(f)]
        except: self.orders = []

    def save(self):
        with open("products.json", "w", encoding="utf-8") as f:
            json.dump([p.to_dict() for p in self.products], f, ensure_ascii=False, indent=2)
        with open("orders.json", "w", encoding="utf-8") as f:
            json.dump([o.to_dict() for o in self.orders], f, ensure_ascii=False, indent=2)

    def add_product(self, name, price, qty):
        pid = max([p.id for p in self.products], default=0) + 1
        self.products.append(Product(pid, name, price, qty))
        self.save()

    def edit_product(self, pid, name, price, qty):
        for p in self.products:
            if p.id == pid:
                p.name, p.price, p.qty = name, price, qty
        self.save()

    def remove_product(self, pid):
        self.products = [p for p in self.products if p.id != pid]
        self.save()

    def new_order(self, items, contact):
        oid = max([o.id for o in self.orders], default=0) + 1
        for pid, count in items:
            for p in self.products:
                if p.id == pid and p.qty >= count:
                    p.qty -= count
        self.orders.append(Order(oid, items, contact))
        self.save()

    def process_order(self, oid):
        self.orders = [o for o in self.orders if o.id != oid]
        self.save()


store = Store()

while True:
    print('\n1. Додати товар\n2. Редагувати товар\n3. Видалити товар\n4. Каталог\n5. Заявка\n6. Перегляд замовлень\n0. Вихід')
    cmd = input('Оберіть дію: ')
    if cmd == "1":
        n = input("Назва: ")
        p = float(input("Ціна: "))
        q = int(input("Кількість: "))
        store.add_product(n, p, q)
    if cmd == "2":
        pid = int(input("ID: "))
        n = input("Назва: ")
        p = float(input("Ціна: "))
        q = int(input("Кількість: "))
        store.edit_product(pid, n, p, q)
    if cmd == "3":
        pid = int(input("ID: "))
        store.remove_product(pid)
    if cmd == "4":
        for p in store.products:
            print(f"ID={p.id} | {p.name} | {p.price} грн | {p.qty} шт")
    if cmd == "5":
        basket = []
        while True:
            pid = int(input("ID товару (0 - все): "))
            if pid == 0: break
            qty = int(input("Кількість: "))
            basket.append((pid, qty))
        contact = input("Контакти: ")
        store.new_order(basket, contact)
    if cmd == "6":
        for o in store.orders:
            print(f"Order ID: {o.id}, {o.items}, Контакт: {o.contact}")
        oid = int(input("ID замовлення для обробки (0 = Пропустити): "))
        if oid != 0:
            store.process_order(oid)
    if cmd == "0":
        break
