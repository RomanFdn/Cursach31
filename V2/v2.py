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

class Cart:
    def __init__(self):
        self.items = []  # (pid, qty)

    def add_item(self, pid, qty):
        for i, (p, q) in enumerate(self.items):
            if p == pid:
                self.items[i] = (p, q + qty)
                return
        self.items.append((pid, qty))

    def edit_item(self, pid, new_qty):
        for i, (p, q) in enumerate(self.items):
            if p == pid:
                if new_qty > 0:
                    self.items[i] = (p, new_qty)
                else:
                    self.items.pop(i)
                return

    def remove_item(self, pid):
        self.items = [item for item in self.items if item[0] != pid]

    def view(self, store):
        print("\nВаш кошик:")
        for pid, qty in self.items:
            prod = store.find_product(pid)
            if prod:
                print(f"ID={prod.id} | {prod.name} | {prod.price} грн | {qty} шт.")

    def is_empty(self):
        return len(self.items) == 0

def admin_menu(store):
    while True:
        print('\n--- Адмін-панель ---')
        print('1. Додати товар')
        print('2. Редагувати товар')
        print('3. Видалити товар')
        print('4. Переглянути каталог')
        print('0. Вийти з адмін-панелі')
        cmd = input('=> ')
        if cmd == "1":
            name = input("Назва: ")
            price = float(input("Ціна: "))
            qty = int(input("Кількість: "))
            store.add_product(name, price, qty)
            print("Товар додано.")
        elif cmd == "2":
            pid = int(input("ID для редагування: "))
            name = input("Нова назва: ")
            price = float(input("Нова ціна: "))
            qty = int(input("Нова кількість: "))
            store.edit_product(pid, name, price, qty)
            print("Товар змінено.")
        elif cmd == "3":
            pid = int(input("ID для видалення: "))
            store.remove_product(pid)
            print("Товар видалено.")
        elif cmd == "4":
            for p in store.products:
                print(f"ID={p.id} | {p.name} | {p.price} грн | {p.qty} шт.")
        elif cmd == "0":
            break

def buyer_menu(store):
    cart = Cart()
    while True:
        print('\n--- Меню покупця ---')
        print('1. Каталог товарів')
        print('2. Додати товар у кошик')
        print('3. Переглянути кошик')
        print('4. Змінити кількість у кошику')
        print('5. Видалити товар з кошика')
        print('6. Оформити замовлення')
        print('0. Вийти в головне меню')
        cmd = input('=> ')
        if cmd == "1":
            for p in store.products:
                print(f"ID={p.id} | {p.name} | {p.price} грн | {p.qty} шт.")
        elif cmd == "2":
            pid = int(input("ID товару: "))
            qty = int(input("Кількість: "))
            prod = store.find_product(pid)
            if not prod:
                print("Товар не знайдено")
                continue
            if prod.qty < qty:
                print("Недостатньо на складі")
                continue
            cart.add_item(pid, qty)
            print("Товар у кошику")
        elif cmd == "3":
            cart.view(store)
        elif cmd == "4":
            pid = int(input("ID у кошику: "))
            qty = int(input("Нова кількість: "))
            cart.edit_item(pid, qty)
            print("Кількість оновлено")
        elif cmd == "5":
            pid = int(input("ID для видалення з кошика: "))
            cart.remove_item(pid)
            print("Видалено з кошика")
        elif cmd == "6":
            if cart.is_empty():
                print("Кошик порожній.")
                continue
            name = input("Контактні дані: ")
            # зменшуємо залишок на складі
            for pid, qty in cart.items:
                prod = store.find_product(pid)
                if prod and prod.qty >= qty:
                    prod.qty -= qty
            store._save()
            print("Замовлення оформлено на ім'я:", name)
            cart = Cart()
        elif cmd == "0":
            break

store = Store()
while True:
    print('\n--- Головне меню ---')
    print('1. Адміністратор')
    print('2. Покупець')
    print('0. Вихід')
    role = input('=> ')
    if role == "1":
        admin_menu(store)
    elif role == "2":
        buyer_menu(store)
    elif role == "0":
        print('До побачення!')
        break
