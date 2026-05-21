from src.strategies.discount_strategy import ClientDiscountStrategy


class NoClientDiscount(ClientDiscountStrategy):
    def apply(self, subtotal: float) -> float:
        return subtotal * 1.0


class VipClientDiscount(ClientDiscountStrategy):
    def apply(self, subtotal: float) -> float:
        return subtotal * 0.95


class CorporateClientDiscount(ClientDiscountStrategy):
    def apply(self, subtotal: float) -> float:
        return subtotal * 0.90
