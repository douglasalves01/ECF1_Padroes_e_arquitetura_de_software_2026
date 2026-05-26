import pytest
from src.models.order_item import OrderItem
from src.services.concrete_order_factory import ConcreteOrderFactory


def test_factory_normal_order() -> None:
    """Factory cria pedido normal sem desconto global."""
    factory = ConcreteOrderFactory()
    items = [OrderItem("p1", 100, 1, "normal")]
    order = factory.create_order("Joao", items, "normal")
    assert order.total == pytest.approx(100)
    assert order.loyalty_multiplier == 1.0


def test_factory_vip_order() -> None:
    """Factory aplica desconto VIP de 5%."""
    factory = ConcreteOrderFactory()
    items = [OrderItem("p1", 100, 1, "normal")]
    order = factory.create_order("Maria", items, "vip")
    assert order.total == pytest.approx(95)


def test_factory_corporate_order() -> None:
    """Factory aplica desconto corporativo de 10%."""
    factory = ConcreteOrderFactory()
    items = [OrderItem("p1", 200, 1, "desc20")]
    order = factory.create_order("Corp", items, "corporativo")
    assert order.total == pytest.approx(144)


def test_factory_invalid_type() -> None:
    """Tipo de cliente invalido gera erro."""
    factory = ConcreteOrderFactory()
    with pytest.raises(ValueError):
        factory.get_configuration("premium")
