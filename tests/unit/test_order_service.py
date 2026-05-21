import pytest

from src.application import create_application
from src.models.order_item import OrderItem


@pytest.fixture
def app(tmp_path, monkeypatch):
    """Monta aplicacao com banco temporario."""
    monkeypatch.chdir(tmp_path)
    ctx = create_application(special=False)
    yield ctx
    ctx.repository.close()


def test_create_order_normal(app) -> None:
    """Cria pedido normal com total correto."""
    items = [OrderItem("p1", 100, 1, "normal")]
    order_id = app.order_service.create_order("Joao", items, "normal")
    order = app.order_service.get_order(order_id)
    assert order is not None
    assert order.total == pytest.approx(100)
    assert order.status == "pendente"


def test_update_status_invalid_when_enforced(app) -> None:
    """Rejeita transicao invalida quando validacao ativa."""
    items = [OrderItem("p1", 100, 1, "normal")]
    order_id = app.order_service.create_order("Joao", items, "normal")
    result = app.order_service.update_status(order_id, "entregue", enforce_transitions=True)
    assert result is False


def test_cancel_order(app) -> None:
    """Cancela pedido e altera status."""
    items = [OrderItem("p1", 100, 1, "normal")]
    order_id = app.order_service.create_order("Joao", items, "normal")
    app.order_service.cancel_order(order_id)
    order = app.order_service.get_order(order_id)
    assert order is not None
    assert order.status == "cancelado"


def test_generate_reports(app, tmp_path) -> None:
    """Gera arquivos de relatorio de vendas e clientes."""
    items = [OrderItem("p1", 50, 2, "normal")]
    app.order_service.create_order("Joao", items, "normal")
    app.order_service.generate_report("vendas")
    app.order_service.generate_report("clientes")
    assert (tmp_path / "rel_vendas.txt").exists()
    assert (tmp_path / "rel_clientes.txt").exists()
