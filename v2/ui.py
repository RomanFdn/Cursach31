from cart import Cart

class ConsoleUI:
    """Консольний UI — меню та відображення в методах."""
    def display_products(self, products):
        """Показати список товарів"""
        for p in products:
            print(f"ID={p.id} | {p.name} | {p.price} грн | {p.qty} шт.")

    def display_cart(self, cart, store):
        """Показати кошик"""
        print("\nВаш кошик:")
        for pid, qty in cart.items:
            prod = store.find_product(pid)
            if prod:
                print(f"ID={prod.id} | {prod.name} | {prod.price} грн | {qty} шт.")

    def admin_menu(self):
        """Меню адміністратора"""
        print('\n--- Адмін-панель ---')
        print('1. Додати товар')
        print('2. Редагувати товар')
        print('3. Видалити товар')
        print('4. Переглянути каталог')
        print('0. Вийти з адмін-панелі')

    def buyer_menu(self):
        """Меню покупця"""
        print('\n--- Меню покупця ---')
        print('1. Каталог товарів')
        print('2. Додати товар у кошик')
        print('3. Переглянути кошик')
        print('4. Змінити кількість у кошику')
        print('5. Видалити товар з кошика')
        print('6. Оформити замовлення')
        print('0. Вийти в головне меню')

    def main_menu(self):
        """Головне меню"""
        print('\n--- Головне меню ---')
        print('1. Адміністратор')
        print('2. Покупець')
        print('0. Вихід')

console_ui = ConsoleUI()

def display_products(products):
    return console_ui.display_products(products)

def display_cart(cart, store):
    return console_ui.display_cart(cart, store)

def admin_menu():
    return console_ui.admin_menu()

def buyer_menu():
    return console_ui.buyer_menu()

def main_menu():
    return console_ui.main_menu()

class AdminInterface:
    """Інтерфейс для адміністратора"""
    def __init__(self, store):
        self.store = store
    
    def add_product(self):
        name = input("Назва: ")
        price = float(input("Ціна: "))
        qty = int(input("Кількість: "))
        self.store.add_product(name, price, qty)
        print("Товар додано.")
    
    def edit_product(self):
        pid = int(input("ID для редагування: "))
        name = input("Нова назва: ")
        price = float(input("Нова ціна: "))
        qty = int(input("Нова кількість: "))
        self.store.edit_product(pid, name, price, qty)
        print("Товар змінено.")
    
    def remove_product(self):
        pid = int(input("ID для видалення: "))
        self.store.remove_product(pid)
        print("Товар видалено.")
    
    def view_catalog(self):
        console_ui.display_products(self.store.products)

class BuyerInterface:
    """Інтерфейс для покупця"""
    def __init__(self, store, cart):
        self.store = store
        self.cart = cart
    
    def view_catalog(self):
        console_ui.display_products(self.store.products)
    
    def add_to_cart(self):
        pid = int(input("ID товару: "))
        qty = int(input("Кількість: "))
        prod = self.store.find_product(pid)
        if not prod:
            print("Товар не знайдено")
            return
        if prod.qty < qty:
            print("Недостатньо на складі")
            return
        self.cart.add_item(pid, qty)
        print("Товар у кошику")
    
    def view_cart(self):
        console_ui.display_cart(self.cart, self.store)
    
    def edit_cart_item(self):
        pid = int(input("ID у кошику: "))
        qty = int(input("Нова кількість: "))
        self.cart.edit_item(pid, qty)
        print("Кількість оновлено")
    
    def remove_from_cart(self):
        pid = int(input("ID для видалення з кошика: "))
        self.cart.remove_item(pid)
        print("Видалено з кошика")
    
    def checkout(self):
        if self.cart.is_empty():
            print("Кошик порожній.")
            return
        name = input("Контактні дані: ")
        for pid, qty in self.cart.items:
            prod = self.store.find_product(pid)
            if prod and prod.qty >= qty:
                prod.qty -= qty
        self.store._save()
        print("Замовлення оформлено на ім'я:", name)
        self.cart.items = []
