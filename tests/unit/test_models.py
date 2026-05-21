from src.models.customer import Customer
from src.models.order import Order
from src.models.order_item import OrderItem


def test_order_item_from_legacy_dict() -> None:
    """Converte dicionario legado em OrderItem."""
    item = OrderItem.from_legacy_dict(
        {"nome": "p1", "p": 10.5, "q": 2, "tipo": "normal"}
    )
    assert item.name == "p1"
    assert item.price == 10.5
    assert item.quantity == 2


def test_order_to_legacy_dict() -> None:
    """Converte Order para formato legado."""
    order = Order(
        customer_name="Ana",
        items=[OrderItem("p1", 100.0, 1, "normal")],
        total=100.0,
        status="pendente",
        created_at="2026-01-01 10:00:00",
        customer_type="vip",
        id=1,
    )
    data = order.to_legacy_dict()
    assert data["cli"] == "Ana"
    assert data["tp"] == "vip"


def test_customer_creation() -> None:
    """Cria cliente com nome e tipo."""
    customer = Customer("Joao", "normal")
    assert customer.name == "Joao"
