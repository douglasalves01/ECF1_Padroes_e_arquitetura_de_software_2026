import tempfile
from pathlib import Path

from hypothesis import assume, given, settings
from hypothesis import strategies as st

from src.models.order import Order
from src.models.order_item import OrderItem
from src.repositories.sqlite_repository import SqliteOrderRepository


@given(
    customer=st.text(min_size=1, max_size=20, alphabet=st.characters(blacklist_categories=["Cs"])),
    other=st.text(min_size=1, max_size=20, alphabet=st.characters(blacklist_categories=["Cs"])),
)
@settings(max_examples=30)
def test_find_by_customer_returns_only_matching(customer, other):
    """Busca por cliente retorna apenas pedidos dele."""
    assume(customer != other)
    with tempfile.TemporaryDirectory() as tmp:
        repo = SqliteOrderRepository(str(Path(tmp) / "test.db"))
        try:
            order = Order(
                customer_name=customer,
                items=[OrderItem("p", 10.0, 1, "normal")],
                total=10.0,
                status="pendente",
                created_at="2026-05-20 10:00:00",
                customer_type="normal",
            )
            other_order = Order(
                customer_name=other,
                items=[OrderItem("p", 20.0, 1, "normal")],
                total=20.0,
                status="pendente",
                created_at="2026-05-20 10:00:00",
                customer_type="vip",
            )
            repo.save(order)
            repo.save(other_order)
            found = repo.find_by_customer(customer)
            assert len(found) == 1
            assert found[0].customer_name == customer
            assert repo.find_by_customer("sem_pedidos_xyz") == []
        finally:
            repo.close()
