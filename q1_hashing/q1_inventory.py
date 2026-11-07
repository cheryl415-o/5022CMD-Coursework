"""Q1 - Pharmacy Inventory System (hash table vs one-dimensional array)."""

import random
import time

from hash_table import HashTable
from product import Product

TABLE_SIZE = 101   # prime number -> spreads keys evenly with modulo hashing

SEED_DATA = [
    (1001, "Panadol 500mg", 8.50, 200, "Medicine"),
    (1002, "Amoxicillin 250mg", 15.90, 80, "Medicine"),
    (1003, "Ibuprofen 400mg", 12.30, 150, "Medicine"),
    (1004, "Vitamin C 1000mg", 24.00, 60, "Supplement"),
    (1005, "Cough Syrup 100ml", 9.80, 90, "Medicine"),
    (1006, "Digital Thermometer", 29.90, 25, "Equipment"),
    (1042, "Paracetamol 500mg", 5.90, 120, "Medicine"),
    (1101, "Loratadine 10mg", 11.20, 70, "Medicine"),
    (1150, "Plaster Box (100pcs)", 7.50, 300, "Equipment"),
    (1203, "Omeprazole 20mg", 18.60, 55, "Medicine"),
]


class PharmacyInventory:
    """Holds the hash table (fast lookup) and a plain list (for comparison)."""

    def __init__(self, table_size: int = TABLE_SIZE) -> None:
        self.table = HashTable(table_size)
        self.array: list[Product] = []

    def insert(self, product: Product) -> int:
        # ask the hash table first (O(1) on average): a new product only needs an
        # append to the array; scanning the array is needed only to replace a record
        existing = self.table.search(product.product_id)
        slot = self.table.insert(product.product_id, product)
        if existing is None:
            self.array.append(product)
        else:
            self.array[self.array.index(existing)] = product
        return slot

    def search_hash(self, product_id: int):
        return self.table.search(product_id)

    def search_array(self, product_id: int):
        for p in self.array:             # linear search O(n)
            if p.product_id == product_id:
                return p
        return None

    def edit(self, product_id: int, price=None, stock=None) -> bool:
        p = self.table.search(product_id)
        if p is None:
            return False
        if price is not None:
            p.price = price
        if stock is not None:
            p.stock = stock
        return True                       # same object is shared by the array

    def delete(self, product_id: int) -> bool:
        if not self.table.delete(product_id):
            return False
        self.array = [p for p in self.array if p.product_id != product_id]
        return True


def load_seed(inv: PharmacyInventory) -> None:
    for pid, name, price, stock, cat in SEED_DATA:
        inv.insert(Product(pid, name, price, stock, cat))


# ---------------------------------------------------------------- UI helpers
def read_int(prompt: str) -> int:
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("  Please enter a whole number.")


def read_float(prompt: str) -> float:
    while True:
        try:
            value = float(input(prompt))
            if value < 0:
                raise ValueError
            return value
        except ValueError:
            print("  Please enter a valid non-negative number.")


def do_insert(inv: PharmacyInventory) -> None:
    pid = read_int("Enter Product ID: ")
    existed = inv.search_hash(pid) is not None
    name = input("Enter Product Name: ").strip()
    price = read_float("Enter Price: ")
    stock = read_int("Enter Stock Quantity: ")
    try:
        slot = inv.insert(Product(pid, name, price, stock))
        if existed:
            print(f"Product ID already existed - record updated in slot [{slot}]")
        else:
            print(f"Product inserted successfully into slot [{slot}]")
    except OverflowError:
        print("Error: hash table is full.")


def do_search(inv: PharmacyInventory) -> None:
    pid = read_int("Enter Product ID to search: ")

    t0 = time.perf_counter_ns()
    found = inv.search_hash(pid)
    t_hash = time.perf_counter_ns() - t0

    t0 = time.perf_counter_ns()
    inv.search_array(pid)
    t_arr = time.perf_counter_ns() - t0

    if found:
        print("Product Found!")
        print(found)
    else:
        print("Product not found.")
    print(f"Search completed in {t_hash / 1e9:.6f} seconds (Hash Table)")
    print(f"Search completed in {t_arr / 1e9:.6f} seconds (Array - same record)")


def do_edit(inv: PharmacyInventory) -> None:
    pid = read_int("Enter Product ID to edit: ")
    if inv.search_hash(pid) is None:
        print("Product not found.")
        return
    price = read_float("Enter new price: ")
    stock = read_int("Enter new stock quantity: ")
    inv.edit(pid, price, stock)
    print("Product updated.")


def do_delete(inv: PharmacyInventory) -> None:
    pid = read_int("Enter Product ID to delete: ")
    print("Product deleted." if inv.delete(pid) else "Product not found.")


def do_list(inv: PharmacyInventory) -> None:
    print(f"{len(inv.table)} product(s) (load factor "
          f"{inv.table.load_factor():.2f}):")
    for p in inv.table.values():
        print("  ", p)


def menu() -> None:
    inv = PharmacyInventory()
    load_seed(inv)
    actions = {"1": do_insert, "2": do_search, "3": do_edit,
               "4": do_delete, "5": do_list}
    while True:
        print("\n==== Pharmacy Inventory System ====")
        print("1. Insert Product")
        print("2. Search Product")
        print("3. Edit Product")
        print("4. Delete Product")
        print("5. List All Products")
        print("6. Run Performance Benchmark")
        print("7. Exit")
        choice = input("Enter choice: ").strip()
        if choice == "7":
            print("Exiting Inventory System. Goodbye!")
            break
        if choice == "6":
            import benchmark
            benchmark.run()
        elif choice in actions:
            actions[choice](inv)
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    menu()
