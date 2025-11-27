from store import Store
from cart import Cart
from ui import AdminInterface, BuyerInterface, console_ui

def admin_logic(store):
    admin_ui = AdminInterface(store)
    while True:
        console_ui.admin_menu()
        cmd = input('=> ')
        if cmd == "1":
            admin_ui.add_product()
        elif cmd == "2":
            admin_ui.edit_product()
        elif cmd == "3":
            admin_ui.remove_product()
        elif cmd == "4":
            admin_ui.view_catalog()
        elif cmd == "0":
            break

def buyer_logic(store):
    cart = Cart()
    buyer_ui = BuyerInterface(store, cart)
    while True:
        console_ui.buyer_menu()
        cmd = input('=> ')
        if cmd == "1":
            buyer_ui.view_catalog()
        elif cmd == "2":
            buyer_ui.add_to_cart()
        elif cmd == "3":
            buyer_ui.view_cart()
        elif cmd == "4":
            buyer_ui.edit_cart_item()
        elif cmd == "5":
            buyer_ui.remove_from_cart()
        elif cmd == "6":
            buyer_ui.checkout()
            buyer_ui.cart = Cart()
        elif cmd == "0":
            break

store = Store()
while True:
    console_ui.main_menu()
    role = input('=> ')
    if role == "1":
        admin_logic(store)
    elif role == "2":
        buyer_logic(store)
    elif role == "0":
        print('До побачення!')
        break