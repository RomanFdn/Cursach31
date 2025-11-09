from store import Store
from cart import Cart

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