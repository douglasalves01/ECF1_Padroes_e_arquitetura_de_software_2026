import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

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


@given(
    price=st.floats(min_value=0.01, max_value=10000, allow_nan=False, allow_infinity=False),
    quantity=st.integers(min_value=1, max_value=1000),
    discount_type=st.sampled_from(["normal", "desc10", "desc20", "frete_gratis"]),
)
@settings(max_examples=100)
def test_item_discount_formula(price, quantity, discount_type):
    """Valida formula de desconto por tipo de item."""
    factors = {
        "normal": 1.0,
        "frete_gratis": 1.0,
        "desc10": 0.9,
        "desc20": 0.8,
    }
    strategies = {
        "normal": NoDiscountStrategy(),
        "frete_gratis": NoDiscountStrategy(),
        "desc10": Discount10Strategy(),
        "desc20": Discount20Strategy(),
    }
    expected = price * quantity * factors[discount_type]
    assert strategies[discount_type].calculate(price, quantity) == pytest.approx(expected)


@given(
    subtotal=st.floats(min_value=0.01, max_value=10000, allow_nan=False, allow_infinity=False),
    client_type=st.sampled_from(["normal", "vip", "corporativo"]),
)
@settings(max_examples=100)
def test_client_discount_factor(subtotal, client_type):
    """Valida desconto global por tipo de cliente."""
    factors = {"normal": 1.0, "vip": 0.95, "corporativo": 0.90}
    strategies = {
        "normal": NoClientDiscount(),
        "vip": VipClientDiscount(),
        "corporativo": CorporateClientDiscount(),
    }
    assert strategies[client_type].apply(subtotal) == pytest.approx(subtotal * factors[client_type])
