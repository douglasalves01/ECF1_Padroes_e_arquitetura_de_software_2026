
from src.application import create_application
from src.models.order_item import OrderItem


def test_cancel_from_any_state(tmp_path, monkeypatch):
    """Cancela pedido em qualquer status."""
    monkeypatch.chdir(tmp_path)
    ctx = create_application()
    items = [OrderItem("p1", 100, 1, "normal")]
    order_id = ctx.order_service.create_order("Joao", items, "normal")
    ctx.payment_service.process_payment(order_id, "cartao", 100)
    ctx.order_service.update_status(order_id, "enviado", enforce_transitions=False)
    assert ctx.order_service.cancel_order(order_id) is True
    order = ctx.order_service.get_order(order_id)
    assert order is not None
    assert order.status == "cancelado"
    ctx.repository.close()


def test_state_transition_validation(tmp_path, monkeypatch):
    """Bloqueia transicao de status invalida."""
    monkeypatch.chdir(tmp_path)
    ctx = create_application()
    items = [OrderItem("p1", 100, 1, "normal")]
    order_id = ctx.order_service.create_order("Joao", items, "normal")
    assert ctx.order_service.update_status(
        order_id,
        "entregue",
        enforce_transitions=True
    ) is False
    assert ctx.order_service.get_order(order_id).status == "pendente"
    ctx.repository.close()


def test_loyalty_points_on_delivery(tmp_path, monkeypatch, capsys):
    """Calcula pontos de fidelidade na entrega."""
    monkeypatch.chdir(tmp_path)
    ctx = create_application()
    items = [OrderItem("p1", 100, 1, "normal")]
    order_id = ctx.order_service.create_order("Maria", items, "vip")
    order = ctx.order_service.get_order(order_id)
    assert order is not None
    ctx.payment_service.process_payment(order_id, "cartao", order.total)
    ctx.order_service.update_status(order_id, "enviado", enforce_transitions=False)
    ctx.order_service.update_status(order_id, "entregue", enforce_transitions=False)
    captured = capsys.readouterr()
    assert "Cliente VIP ganhou" in captured.out
    ctx.repository.close()
