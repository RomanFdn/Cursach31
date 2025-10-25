import json
from dataclasses import dataclass, asdict
from typing import Dict, Optional

# --- 1. Моделі (коротко і сучасно) ---

@dataclass
class Product:
    """Використання dataclass значно скорочує код."""
    id: int
    name: str
    price: float
    qty: int

    def to_dict(self) -> dict:
        return asdict(self)

    @staticmethod
    def from_dict(d: dict) -> 'Product':
        return Product(**d)

# --- 2. Основні Класи (оптимізовані зі словниками) ---

class Store:
    """Використовує словник (dict) для миттєвого доступу O(1) до товарів."""
    def __init__(self, filename="products.json"):
        self.filename = filename
        # {pid: Product} - значно ефективніше за список
        self.products: Dict[int, Product] = {}
        self._load()

    def _load(self):
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                products_list = json.load(f)
                for p_data in products_list:
                    product = Product.from_dict(p_data)
                    self.products[product.id] = product
        except (FileNotFoundError, json.JSONDecodeError):
            self.products = {}

    def _save(self):
        with open(self.filename, "w", encoding="utf-8") as f:
            # Конвертуємо значення словника назад у список
            json.dump([p.to_dict() for p in self.products.values()], f, ensure_ascii=False, indent=2)

    def add_product(self, name: str, price: float, qty: int):
        pid = max(self.products.keys(), default=0) + 1
        product = Product(pid, name, price, qty)
        self.products[pid] = product
        self._save()

    def edit_product(self, pid: int, name: str, price: float, qty: int):
        if product := self.find_product(pid):  # := (walrus operator, Python 3.8+)
            product.name = name
            product.price = price
            product.qty = qty
            self._save()

    def remove_product(self, pid: int):
        if pid in self.products:
            del self.products[pid]
            self._save()

    def find_product(self, pid: int) -> Optional[Product]:
        """Миттєвий пошук завдяки словнику."""
        return self.products.get(pid)

    def process_order(self, cart: 'Cart') -> bool:
        """Транзакційна обробка замовлення."""
        # 1. Перевірка, чи всі товари є в наявності
        for pid, qty in cart.items.items():
            prod = self.find_product(pid)
            if not prod or prod.qty < qty:
                print(f"Помилка: Недостатньо товару '{prod.name if prod else f'ID {pid}'}'.")
                return False
        
        # 2. Списання товарів
        for pid, qty in cart.items.items():
            self.products[pid].qty -= qty
        
        self._save()
        return True

class Cart:
    """Використовує словник (dict) {pid: qty} для простоти."""
    def __init__(self):
        self.items: Dict[int, int] = {} # {pid: qty}

    def add_item(self, pid: int, qty: int):
        """Значно коротший 'add' завдяки dict.get()"""
        self.items[pid] = self.items.get(pid, 0) + qty

    def edit_item(self, pid: int, new_qty: int):
        if new_qty > 0:
            self.items[pid] = new_qty
        elif pid in self.items:
            del self.items[pid]

    def remove_item(self, pid: int):
        if pid in self.items:
            del self.items[pid]

    def view(self, store: Store):
        """Перегляд кошика. Знову потребує 'store' для отримання деталей."""
        if self.is_empty():
            print("\nВаш кошик порожній.")
            return
            
        print("\n--- Ваш кошик ---")
        total = 0.0
        for pid, qty in self.items.items():
            prod = store.find_product(pid)
            if prod:
                item_total = prod.price * qty
                print(f"ID={prod.id} | {prod.name} | {prod.price} грн | {qty} шт. | Сума: {item_total:.2f} грн")
                total += item_total
        print(f"--------------------\nЗагальна вартість: {total:.2f} грн")

    def is_empty(self) -> bool:
        return not self.items

    def clear(self):
        self.items.clear()

# --- 3. Функції-меню (як у вашому оригіналі) ---

def admin_menu(store: Store):
    while True:
        print('\n--- Адмін-панель ---')
        print('1. Додати товар\n2. Редагувати товар\n3. Видалити товар\n4. Переглянути каталог\n0. Вийти')
        cmd = input('=> ')
        try:
            if cmd == "1":
                name = input("Назва: ")
                price = float(input("Ціна: "))
                qty = int(input("Кількість: "))
                store.add_product(name, price, qty)
                print("Товар додано.")
            elif cmd == "2":
                pid = int(input("ID для редагування: "))
                if not store.find_product(pid):
                    print("Товар не знайдено.")
                    continue
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
                print("\n--- Каталог товарів ---")
                if not store.products:
                    print("Склад порожній.")
                for p in store.products.values(): # .values() для ітерації по словнику
                    print(f"ID={p.id} | {p.name} | {p.price:.2f} грн | {p.qty} шт.")
            elif cmd == "0":
                break
        except ValueError:
            print("Помилка: Некоректний ввід. ID та кількість мають бути числами.")

def buyer_menu(store: Store):
    cart = Cart()
    while True:
        print('\n--- Меню покупця ---')
        print('1. Каталог товарів\n2. Додати у кошик\n3. Переглянути кошик')
        print('4. Змінити кількість\n5. Видалити з кошика\n6. Оформити замовлення\n0. Вийти')
        cmd = input('=> ')
        try:
            if cmd == "1":
                print("\n--- Каталог товарів ---")
                available = False
                for p in store.products.values():
                    if p.qty > 0:
                        print(f"ID={p.id} | {p.name} | {p.price:.2f} грн | (Доступно: {p.qty} шт.)")
                        available = True
                if not available:
                    print("На жаль, товари закінчились.")
            elif cmd == "2":
                pid = int(input("ID товару: "))
                prod = store.find_product(pid)
                if not prod:
                    print("Товар не знайдено.")
                    continue
                
                qty = int(input(f"Кількість (доступно {prod.qty}): "))
                if qty <= 0:
                    print("Кількість має бути позитивною.")
                elif prod.qty < qty:
                    print(f"Недостатньо на складі. Доступно: {prod.qty}")
                else:
                    cart.add_item(pid, qty)
                    print("Товар у кошику.")
            elif cmd == "3":
                cart.view(store)
            elif cmd == "4":
                pid = int(input("ID у кошику: "))
                if pid not in cart.items:
                    print("Товару немає у кошику.")
                    continue
                
                prod = store.find_product(pid) # Потрібно для перевірки наявності
                new_qty = int(input(f"Нова кількість (доступно {prod.qty}, 0 - видалити): "))
                
                if new_qty > prod.qty:
                    print(f"Недостатньо на складі. Доступно: {prod.qty}")
                else:
                    cart.edit_item(pid, new_qty)
                    print("Кількість оновлено.")
            elif cmd == "5":
                pid = int(input("ID для видалення з кошика: "))
                cart.remove_item(pid)
                print("Видалено з кошика.")
            elif cmd == "6":
                if cart.is_empty():
                    print("Кошик порожній.")
                    continue
                
                name = input("Контактні дані (ПІБ): ")
                if not name:
                    print("Контактні дані обов'язкові.")
                    continue

                if store.process_order(cart):
                    print(f"Замовлення успішно оформлено на ім'я: {name}")
                    cart.clear()
                else:
                    print("Не вдалося оформити замовлення (товару не вистачило на складі).")
            elif cmd == "0":
                break
        except ValueError:
            print("Помилка: Некоректний ввід. ID та кількість мають бути числами.")

# --- 4. Точка входу ---

if __name__ == "__main__":
    store = Store()
    while True:
        print('\n--- Головне меню ---')
        print('1. Адміністратор\n2. Покупець\n0. Вихід')
        role = input('=> ')
        if role == "1":
            admin_menu(store)
        elif role == "2":
            buyer_menu(store)
        elif role == "0":
            print('До побачення!')
            break