from src.strategies.discount_strategy import ItemDiscountStrategy
from src.strategies.item_discount_resolver import resolve_item_discount

VOLUME_THRESHOLD: int = 3
VOLUME_DISCOUNT_RATE: float = 0.15


class VolumeDiscountStrategy(ItemDiscountStrategy):
    def __init__(self, base_discount_type: str) -> None:
        self._base_strategy: ItemDiscountStrategy = resolve_item_discount(
            base_discount_type
        )

    def calculate(self, price: float, quantity: int) -> float:
        base_subtotal = self._base_strategy.calculate(price, quantity)
        if quantity >= VOLUME_THRESHOLD:
            return base_subtotal * (1.0 - VOLUME_DISCOUNT_RATE)
        return base_subtotal


def calculate_subtotal_with_volume_discount(
    items: list[dict[str, object]],
) -> float:
    total = 0.0
    for item in items:
        price = float(str(item["p"]))
        quantity = int(str(item["q"]))
        discount_type = str(item["tipo"])
        strategy = VolumeDiscountStrategy(discount_type)
        total += strategy.calculate(price, quantity)
    return total