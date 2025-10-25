import json
from dataclasses import dataclass, asdict
from typing import Dict, Optional

# --- 1. Покращені Моделі (Dataclasses) ---

@dataclass
class Product:
    """Модель продукту з використанням dataclass для лаконічності."""
    id: int
    name: str
    price: float
    qty: int

    def to_dict(self) -> dict:
        """Серіалізує об'єкт у словник."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> 'Product':
        """Десеріалізує об'єкт зі словника."""
        # Використання **data дозволяє автоматично
        # розпакувати словник у аргументи __init__
        return cls(**data)

@dataclass
class CartItem:
    """Модель позиції у кошику. Використовує Композицію (містить Product)."""
    product: Product
    quantity: int

    @property
    def total_price(self) -> float:
        """Обчислювана властивість для вартості позиції."""
        return self.product.price * self.quantity

# --- 2. Покращені Класи Бізнес-Логіки ---

class Cart:
    """
    Клас Кошика. Тепер повністю інкапсулює логіку роботи з позиціями.
    Використовує словник для швидкого доступу до позицій за ID товару.
    """
    def __init__(self):
        # {product_id: CartItem}
        self.items: Dict[int, CartItem] = {}

    def add_item(self, product: Product, qty: int):
        """Додає товар або оновлює кількість існуючого."""
        if qty <= 0:
            print("Кількість має бути позитивною.")
            return

        # Перевірка, чи достатньо товару НА СКЛАДІ
        if product.qty < qty:
            print(f"Недостатньо на складі. Доступно: {product.qty}")
            return

        pid = product.id
        if pid in self.items:
            # Перевірка загальної кількості (вже в кошику + нова)
            new_qty = self.items[pid].quantity + qty
            if product.qty < new_qty:
                print(f"Недостатньо на складі. Доступно: {product.qty}, у кошику вже: {self.items[pid].quantity}")
            else:
                self.items[pid].quantity += qty
                print(f"Додано ще {qty} шт. товару '{product.name}'.")
        else:
            self.items[pid] = CartItem(product=product, quantity=qty)
            print(f"Товар '{product.name}' додано до кошика.")

    def edit_item(self, pid: int, new_qty: int):
        """Змінює кількість товару або видаляє його, якщо кількість <= 0."""
        if pid not in self.items:
            print("Такого товару немає у кошику.")
            return

        if new_qty > 0:
            # Перевірка наявності на складі
            available = self.items[pid].product.qty
            if new_qty > available:
                print(f"Неможливо встановити кількість {new_qty}. Доступно на складі: {available}")
            else:
                self.items[pid].quantity = new_qty
                print("Кількість оновлено.")
        else:
            # Видаляємо, якщо нова кількість 0 або менше
            self.remove_item(pid)

    def remove_item(self, pid: int):
        """Видаляє позицію з кошика за ID товару."""
        if pid in self.items:
            del self.items[pid]
            print("Товар видалено з кошика.")
        else:
            print("Такого товару немає у кошику.")

    def view(self):
        """
        Відображає вміст кошика.
        Зверніть увагу: 'store' більше не потрібен як аргумент!
        """
        if self.is_empty():
            print("\nВаш кошик порожній.")
            return

        print("\n--- Ваш кошик ---")
        total = 0.0
        for item in self.items.values():
            print(f"ID={item.product.id} | {item.product.name} | {item.product.price} грн | {item.quantity} шт. | Сума: {item.total_price:.2f} грн")
            total += item.total_price
        print("--------------------")
        print(f"Загальна вартість: {total:.2f} грн")

    def is_empty(self) -> bool:
        return not self.items

    def clear(self):
        """Очищує кошик (наприклад, після замовлення)."""
        self.items.clear()


class Store:
    """
    Клас Складу (Репозиторій).
    Відповідає за CRUD операції з товарами та їх збереження у файл.
    Використовує словник для миттєвого доступу до товарів за ID.
    """
    def __init__(self, filename: str = "products.json"):
        self.filename = filename
        # {product_id: Product} - значно ефективніше за list
        self.products: Dict[int, Product] = {}
        self._load()

    def _load(self):
        """Завантажує товари зі JSON-файлу."""
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                products_list = json.load(f)
                # Конвертуємо список словників у словник об'єктів
                for p_data in products_list:
                    product = Product.from_dict(p_data)
                    self.products[product.id] = product
        except (FileNotFoundError, json.JSONDecodeError):
            # Якщо файл не знайдено або він порожній/пошкоджений
            self.products = {}

    def _save(self):
        """Зберігає поточний стан товарів у JSON-файл."""
        with open(self.filename, "w", encoding="utf-8") as f:
            # Конвертуємо словник об'єктів назад у список словників
            products_list = [p.to_dict() for p in self.products.values()]
            json.dump(products_list, f, ensure_ascii=False, indent=2)

    def add_product(self, name: str, price: float, qty: int) -> Product:
        """Створює, додає та повертає новий об'єкт Product."""
        # Визначення нового ID стало простішим
        pid = max(self.products.keys(), default=0) + 1
        product = Product(pid, name, price, qty)
        self.products[pid] = product
        self._save()
        return product

    def edit_product(self, pid: int, name: str, price: float, qty: int) -> bool:
        """Оновлює дані товару за ID."""
        product = self.find_product(pid)
        if product:
            product.name = name
            product.price = price
            product.qty = qty
            self._save()
            return True
        return False

    def remove_product(self, pid: int) -> bool:
        """Видаляє товар за ID. Миттєва операція завдяки словнику."""
        if pid in self.products:
            del self.products[pid]
            self._save()
            return True
        return False

    def find_product(self, pid: int) -> Optional[Product]:
        """Знаходить товар за ID. Миттєва операція завдяки словнику."""
        return self.products.get(pid)

    def get_all_products(self) -> list[Product]:
        """Повертає список всіх товарів."""
        return list(self.products.values())

    def process_order(self, cart: Cart) -> bool:
        """
        Обробляє замовлення. Це ключова бізнес-логіка.
        Перевіряє наявність *всіх* товарів перед списанням.
        """
        # 1. Валідація (чи всі товари ще є на складі у потрібній кількості)
        for item in cart.items.values():
            # self.find_product(item.product.id) - це той самий об'єкт,
            # але краще перевіряти "свіжі" дані зі сховища
            prod_in_store = self.find_product(item.product.id)
            if not prod_in_store or prod_in_store.qty < item.quantity:
                print(f"Помилка: Недостатньо товару '{item.product.name}'. Замовлення скасовано.")
                return False

        # 2. Списання (якщо валідація пройшла)
        for item in cart.items.values():
            # Змінюємо кількість товару на складі
            self.products[item.product.id].qty -= item.quantity
        
        self._save()
        return True


# --- 3. Класи Відображення/Контролери (Розділення відповідальності) ---

class AdminConsole:
    """Клас, що відповідає *лише* за адмін-меню та взаємодію."""
    def __init__(self, store: Store):
        self.store = store

    def run(self):
        """Головний цикл адмін-панелі."""
        while True:
            print('\n--- Адмін-панель ---')
            print('1. Додати товар')
            print('2. Редагувати товар')
            print('3. Видалити товар')
            print('4. Переглянути каталог')
            print('0. Вийти з адмін-панелі')
            cmd = input('=> ')
            
            if cmd == "1": self._handle_add()
            elif cmd == "2": self._handle_edit()
            elif cmd == "3": self._handle_remove()
            elif cmd == "4": self._view_catalog()
            elif cmd == "0": break
            else: print("Невідома команда.")

    def _view_catalog(self):
        print("\n--- Каталог товарів (Склад) ---")
        products = self.store.get_all_products()
        if not products:
            print("Склад порожній.")
            return
        for p in products:
            print(f"ID={p.id} | {p.name} | {p.price:.2f} грн | {p.qty} шт.")

    def _handle_add(self):
        try:
            name = input("Назва: ")
            price = float(input("Ціна: "))
            qty = int(input("Кількість: "))
            self.store.add_product(name, price, qty)
            print("Товар додано.")
        except ValueError:
            print("Помилка: Ціна та кількість мають бути числами.")

    def _handle_edit(self):
        try:
            pid = int(input("ID для редагування: "))
            if not self.store.find_product(pid):
                print("Товар з таким ID не знайдено.")
                return
                
            name = input("Нова назва: ")
            price = float(input("Нова ціна: "))
            qty = int(input("Нова кількість: "))
            if self.store.edit_product(pid, name, price, qty):
                print("Товар змінено.")
        except ValueError:
            print("Помилка: ID, ціна та кількість мають бути числами.")

    def _handle_remove(self):
        try:
            pid = int(input("ID для видалення: "))
            if self.store.remove_product(pid):
                print("Товар видалено.")
            else:
                print("Товар з таким ID не знайдено.")
        except ValueError:
            print("Помилка: ID має бути числом.")


class BuyerConsole:
    """Клас, що відповідає *лише* за меню покупця та взаємодію."""
    def __init__(self, store: Store):
        self.store = store
        self.cart = Cart()

    def run(self):
        """Головний цикл меню покупця."""
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

            if cmd == "1": self._view_catalog()
            elif cmd == "2": self._handle_add_to_cart()
            elif cmd == "3": self.cart.view()
            elif cmd == "4": self._handle_edit_cart()
            elif cmd == "5": self._handle_remove_from_cart()
            elif cmd == "6": self._handle_checkout()
            elif cmd == "0": break
            else: print("Невідома команда.")

    def _view_catalog(self):
        print("\n--- Каталог товарів ---")
        products = self.store.get_all_products()
        if not products:
            print("На жаль, товари закінчились.")
            return
        # Показуємо лише товари, які є в наявності
        available_products = [p for p in products if p.qty > 0]
        if not available_products:
            print("На жаль, товари закінчились.")
            return

        for p in available_products:
            print(f"ID={p.id} | {p.name} | {p.price:.2f} грн | (Доступно: {p.qty} шт.)")

    def _handle_add_to_cart(self):
        try:
            pid = int(input("ID товару: "))
            product = self.store.find_product(pid)
            if not product:
                print("Товар не знайдено.")
                return
            if product.qty <= 0:
                print("Цього товару немає в наявності.")
                return

            qty = int(input(f"Кількість (доступно {product.qty}): "))
            self.cart.add_item(product, qty)
            
        except ValueError:
            print("Помилка: ID та кількість мають бути числами.")

    def _handle_edit_cart(self):
        try:
            pid = int(input("ID товару у кошику: "))
            qty = int(input("Нова кількість (0 для видалення): "))
            self.cart.edit_item(pid, qty)
        except ValueError:
            print("Помилка: ID та кількість мають бути числами.")

    def _handle_remove_from_cart(self):
        try:
            pid = int(input("ID для видалення з кошика: "))
            self.cart.remove_item(pid)
        except ValueError:
            print("Помилка: ID має бути числом.")

    def _handle_checkout(self):
        if self.cart.is_empty():
            print("Кошик порожній. Нічого оформлювати.")
            return
        
        self.cart.view()
        name = input("Введіть ваші контактні дані (ПІБ, телефон): ")
        if not name:
            print("Контактні дані не можуть бути порожніми. Замовлення скасовано.")
            return

        # Уся складна логіка списання інкапсульована тут:
        if self.store.process_order(self.cart):
            print(f"\nДякуємо, {name}! Ваше замовлення успішно оформлено.")
            self.cart.clear() # Очищуємо кошик
        else:
            print("\nНе вдалося оформити замовлення. Перевірте кошик (можливо, товар закінчився).")


# --- 4. Головний клас-запускач ---

class App:
    """Головний клас застосунку, який керує меню ролей."""
    def __init__(self, db_path: str):
        self.store = Store(db_path)
        self.admin_console = AdminConsole(self.store)
        # BuyerConsole створюється щоразу нова, щоб кошик був порожнім
        # Або можна передавати store і створювати її тут:
        # self.buyer_console = BuyerConsole(self.store)

    def run(self):
        while True:
            print('\n--- Головне меню ---')
            print('1. Я Адміністратор')
            print('2. Я Покупець')
            print('0. Вихід')
            role = input('=> ')
            
            if role == "1":
                # Запускаємо консоль адміна
                self.admin_console.run()
            elif role == "2":
                # Створюємо нову сесію покупця з новим кошиком
                buyer_console = BuyerConsole(self.store)
                buyer_console.run()
            elif role == "0":
                print('До побачення!')
                break


# --- Точка входу ---
if __name__ == "__main__":
    app = App(db_path="products.json")
    app.run()