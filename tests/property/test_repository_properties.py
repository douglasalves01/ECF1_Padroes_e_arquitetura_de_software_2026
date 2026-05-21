import tempfile
from datetime import datetime
from pathlib import Path

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from src.models.order import Order
from src.models.order_item import OrderItem
from src.repositories.sqlite_repository import SqliteOrderRepository


def _order_strategy():
    return st.builds(
        Order,
        customer_name=st.text(min_size=1, max_size=30, alphabet=st.characters(blacklist_categories=["Cs"])),
        items=st.lists(
            st.builds(
                OrderItem,
                name=st.text(min_size=1, max_size=20, alphabet=st.characters(blacklist_categories=["Cs"])),
                price=st.floats(min_value=0.01, max_value=1000, allow_nan=False, allow_infinity=False),
                quantity=st.integers(min_value=1, max_value=10),
                discount_type=st.sampled_from(["normal", "desc10", "desc20", "frete_gratis"]),
            ),
            min_size=1,
            max_size=5,
        ),
        total=st.floats(min_value=0.01, max_value=10000, allow_nan=False, allow_infinity=False),
        status=st.just("pendente"),
        created_at=st.just(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        customer_type=st.sampled_from(["normal", "vip", "corporativo"]),
        id=st.none(),
        loyalty_multiplier=st.floats(min_value=1.0, max_value=2.0),
    )


@given(order=_order_strategy())
@settings(max_examples=50)
def test_repository_round_trip(order):
    """Salvar e buscar pedido preserva os dados."""
    with tempfile.TemporaryDirectory() as tmp:
        db_path = str(Path(tmp) / "test.db")
        repo = SqliteOrderRepository(db_path)
        try:
            order_id = repo.save(order)
            found = repo.find_by_id(order_id)
            assert found is not None
            assert found.customer_name == order.customer_name
            assert found.total == pytest.approx(order.total)
            assert found.status == order.status
            assert found.customer_type == order.customer_type
            assert len(found.items) == len(order.items)
        finally:
            repo.close()
