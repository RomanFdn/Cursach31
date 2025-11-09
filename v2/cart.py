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