from hypothesis import given, settings
from hypothesis import strategies as st
from src.strategies.payment_implementations import (
    BoletoPaymentStrategy,
    CardPaymentStrategy,
    PixPaymentStrategy,
)


@given(
    total=st.floats(
        min_value=0.01,
        max_value=5000,
        allow_nan=False,
        allow_infinity=False
    ),
    paid=st.floats(
        min_value=0.01,
        max_value=5000,
        allow_nan=False,
        allow_infinity=False
    ),
)
@settings(max_examples=100)
def test_approving_payment_methods(total, paid):
    """Cartao e PIX aprovam com valor suficiente."""
    if paid < total:
        return
    for strategy in (CardPaymentStrategy(), PixPaymentStrategy()):
        result = strategy.process(total, paid)
        assert result.success is True
        assert result.approves_order is True


@given(
    total=st.floats(
        min_value=0.01,
        max_value=5000,
        allow_nan=False,
        allow_infinity=False
    ),
    paid=st.floats(
        min_value=0.0,
        max_value=5000,
        allow_nan=False,
        allow_infinity=False
    ),
)
@settings(max_examples=100)
def test_insufficient_payment_rejected(total, paid):
    """Pagamento insuficiente sempre e rejeitado."""
    if paid >= total:
        return
    for strategy in (
        CardPaymentStrategy(),
        PixPaymentStrategy(),
        BoletoPaymentStrategy(),
    ):
        result = strategy.process(total, paid)
        assert result.success is False
