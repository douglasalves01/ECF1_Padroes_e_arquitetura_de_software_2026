from src.models.order_item import OrderItem
from src.strategies.discount_implementations import (
    Discount10Strategy,
    Discount20Strategy,
    NoDiscountStrategy,
)
from src.strategies.discount_strategy import ItemDiscountStrategy


def resolve_item_discount(discount_type: str) -> ItemDiscountStrategy:
    if discount_type in ("normal", "frete_gratis"):
        return NoDiscountStrategy()
    if discount_type == "desc10":
        return Discount10Strategy()
    if discount_type == "desc20":
        return Discount20Strategy()
    return NoDiscountStrategy()


def calculate_items_subtotal(
    items: list[OrderItem],
    *,
    include_free_shipping: bool = True,
) -> float:
    total = 0.0
    for item in items:
        if item.discount_type == "frete_gratis" and not include_free_shipping:
            continue
        strategy = resolve_item_discount(item.discount_type)
        total += strategy.calculate(item.price, item.quantity)
    return total


def calculate_special_subtotal(items: list[OrderItem]) -> float:
    subtotal = calculate_items_subtotal(items, include_free_shipping=False)
    return subtotal * 1.15
