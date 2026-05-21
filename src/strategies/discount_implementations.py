from src.strategies.discount_strategy import ItemDiscountStrategy


class NoDiscountStrategy(ItemDiscountStrategy):
    def calculate(self, price: float, quantity: int) -> float:
        return price * quantity * 1.0


class Discount10Strategy(ItemDiscountStrategy):
    def calculate(self, price: float, quantity: int) -> float:
        return price * quantity * 0.9


class Discount20Strategy(ItemDiscountStrategy):
    def calculate(self, price: float, quantity: int) -> float:
        return price * quantity * 0.8
