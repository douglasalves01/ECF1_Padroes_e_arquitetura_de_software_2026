import pytest

from src.strategies.payment_implementations import (
    BoletoPaymentStrategy,
    CardPaymentStrategy,
    PixPaymentStrategy,
)


def test_card_approves_on_sufficient_amount() -> None:
    """Cartao aprova com valor suficiente."""
    result = CardPaymentStrategy().process(100, 100)
    assert result.success is True
    assert result.approves_order is True


def test_pix_rejects_insufficient() -> None:
    """PIX rejeita valor insuficiente."""
    result = PixPaymentStrategy().process(100, 50)
    assert result.success is False


def test_boleto_does_not_approve() -> None:
    """Boleto nao altera status do pedido."""
    result = BoletoPaymentStrategy().process(100, 100)
    assert result.success is True
    assert result.approves_order is False
