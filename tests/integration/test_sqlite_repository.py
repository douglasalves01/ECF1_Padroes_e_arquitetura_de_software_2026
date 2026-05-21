import pytest

from src.models.order import Order
from src.models.order_item import OrderItem
from src.repositories.sqlite_repository import SqliteOrderRepository


@pytest.fixture
def repo(tmp_path, monkeypatch):
    """Repository com sqlite em diretorio temporario."""
    monkeypatch.chdir(tmp_path)
    repository = SqliteOrderRepository("test.db")
    yield repository
    repository.close()


def _sample_order() -> Order:
    return Order(
        customer_name="Joao",
        items=[OrderItem("p1", 100, 1, "normal")],
        total=100.0,
        status="pendente",
        created_at="2026-05-20 10:00:00",
        customer_type="normal",
    )


def test_save_and_find_by_id(repo) -> None:
    """Salva pedido e busca pelo id."""
    order_id = repo.save(_sample_order())
    found = repo.find_by_id(order_id)
    assert found is not None
    assert found.customer_name == "Joao"
    assert found.total == pytest.approx(100)


def test_find_by_customer(repo) -> None:
    """Retorna pedidos apenas do cliente informado."""
    repo.save(_sample_order())
    repo.save(
        Order(
            customer_name="Maria",
            items=[OrderItem("p2", 50, 1, "normal")],
            total=50.0,
            status="pendente",
            created_at="2026-05-20 11:00:00",
            customer_type="vip",
        )
    )
    joao_orders = repo.find_by_customer("Joao")
    assert len(joao_orders) == 1
    assert repo.find_by_customer("Inexistente") == []


def test_update_status(repo) -> None:
    """Atualiza status de pedido existente."""
    order_id = repo.save(_sample_order())
    assert repo.update_status(order_id, "aprovado") is True
    assert repo.update_status(999, "aprovado") is False


def test_find_all(repo) -> None:
    """Lista todos os pedidos persistidos."""
    repo.save(_sample_order())
    repo.save(_sample_order())
    assert len(repo.find_all()) == 2
