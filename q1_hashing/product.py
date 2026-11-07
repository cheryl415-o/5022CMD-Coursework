"""Entity class for a pharmacy product."""


class Product:
    """A product sold by the pharmacy (medicine, supplement, equipment ...)."""

    def __init__(self, product_id: int, name: str, price: float,
                 stock: int, category: str = "Medicine") -> None:
        self.product_id = product_id   # int   - unique key, fast to hash/compare
        self.name = name               # str   - e.g. "Paracetamol 500mg"
        self.price = price             # float - price in RM
        self.stock = stock             # int   - units on hand
        self.category = category       # str   - Medicine / Supplement / ...

    def __str__(self) -> str:
        return (f"ID: {self.product_id} | Name: {self.name} | "
                f"Price: RM{self.price:.2f} | Stock: {self.stock} | "
                f"Category: {self.category}")
