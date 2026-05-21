import pytest

from src.models.order_item import OrderItem
from src.strategies.client_discount_implementations import (
    CorporateClientDiscount,
    NoClientDiscount,
    VipClientDiscount,
)
from src.strategies.discount_implementations import (
    Discount10Strategy,
    Discount20Strategy,
    NoDiscountStrategy,
)
from src.strategies.item_discount_resolver import calculate_items_subtotal


def test_no_discount_strategy() -> None:
    """Item normal sem desconto."""
    assert NoDiscountStrategy().calculate(100, 2) == pytest.approx(200)


def test_discount10_strategy() -> None:
    """Item com 10% de desconto."""
    assert Discount10Strategy().calculate(100, 1) == pytest.approx(90)


def test_discount20_strategy() -> None:
    """Item com 20% de desconto."""
    assert Discount20Strategy().calculate(100, 1) == pytest.approx(80)


def test_vip_client_discount() -> None:
    """Desconto de 5% para cliente VIP."""
    assert VipClientDiscount().apply(100) == pytest.approx(95)


def test_corporate_client_discount() -> None:
    """Desconto de 10% para cliente corporativo."""
    assert CorporateClientDiscount().apply(100) == pytest.approx(90)


def test_no_client_discount() -> None:
    """Cliente normal sem desconto global."""
    assert NoClientDiscount().apply(100) == pytest.approx(100)


def test_calculate_items_subtotal_mixed() -> None:
    """Soma subtotal com varios tipos de item."""
    items = [
        OrderItem("a", 100, 1, "normal"),
        OrderItem("b", 100, 1, "desc10"),
        OrderItem("c", 100, 1, "desc20"),
        OrderItem("d", 100, 1, "frete_gratis"),
    ]
    assert calculate_items_subtotal(items) == pytest.approx(370)
