import pytest
from src.observers.whatsapp_observer import WhatsAppObserver


@pytest.fixture
def observer() -> WhatsAppObserver:
    return WhatsAppObserver()

_ORDER_DATA: dict[str, object] = {
    "id": 1,
    "cli": "Jorge",
    "tp": "normal",
    "tot": 100.0,
    "st": "pendente",
    "dt": "2026-05-26 10:00:00",
    "itens": [],
}

class TestWhatsAppObserver:

    def test_notifica_pedido_recebido(
        self, observer: WhatsAppObserver, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Verifica mensagem WhatsApp ao receber pedido."""
        observer.notify("pedido_recebido", _ORDER_DATA)
        captured = capsys.readouterr()
        assert "WhatsApp" in captured.out
        assert "Jorge" in captured.out

    def test_notifica_aprovado(
        self, observer: WhatsAppObserver, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Verifica mensagem WhatsApp para pedido aprovado."""
        observer.notify("aprovado", _ORDER_DATA)
        captured = capsys.readouterr()
        assert "WhatsApp" in captured.out
        assert "aprovado" in captured.out.lower()

    def test_notifica_enviado(
        self, observer: WhatsAppObserver, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Verifica mensagem WhatsApp para pedido enviado."""
        observer.notify("enviado", _ORDER_DATA)
        captured = capsys.readouterr()
        assert "WhatsApp" in captured.out

    def test_notifica_entregue(
        self, observer: WhatsAppObserver, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Verifica mensagem WhatsApp para pedido entregue."""
        observer.notify("entregue", _ORDER_DATA)
        captured = capsys.readouterr()
        assert "WhatsApp" in captured.out

    def test_ignora_evento_desconhecido(
        self, observer: WhatsAppObserver, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Verifica que eventos desconhecidos não geram saída."""
        observer.notify("evento_inexistente", _ORDER_DATA)
        captured = capsys.readouterr()
        assert captured.out == ""

    @pytest.mark.parametrize("customer_type", ["normal", "vip", "corporativo"])
    def test_notifica_todos_tipos_de_cliente(
        self,
        observer: WhatsAppObserver,
        capsys: pytest.CaptureFixture[str],
        customer_type: str,
    ) -> None:
        """Verifica notificação para todos os tipos de cliente."""
        data = {**_ORDER_DATA, "tp": customer_type}
        observer.notify("pedido_recebido", data)
        captured = capsys.readouterr()
        assert "WhatsApp" in captured.out

    def test_integracao_com_notification_service(
        self, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Verifica integração com NotificationService."""
        from src.services.notification_service import NotificationService

        service = NotificationService()
        service.add_observer(WhatsAppObserver())
        service.notify_all("pedido_recebido", _ORDER_DATA)
        captured = capsys.readouterr()
        assert "WhatsApp" in captured.out

    def test_integracao_com_concrete_factory_via_configuracao(
        self, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Verifica integração dinâmica via ConcreteOrderFactory."""
        import os
        import tempfile

        from src.models.order_item import OrderItem
        from src.repositories.sqlite_repository import SqliteOrderRepository
        from src.services.concrete_order_factory import ConcreteOrderFactory
        from src.services.notification_service import NotificationService
        from src.services.order_service import OrderService

        with tempfile.TemporaryDirectory() as tmp:
            db_path = os.path.join(tmp, "test.db")
            repo = SqliteOrderRepository(db_path)
            notif = NotificationService()
            factory = ConcreteOrderFactory()
            order_service = OrderService(repo, factory, notif)

            items = [
                OrderItem(
                    name="p1",
                    price=100.0,
                    quantity=1,
                    discount_type="normal"
                )
            ]
            order_id = order_service.create_order("Jorge", items, "normal")

            notif.add_observer(WhatsAppObserver())
            order = repo.find_by_id(order_id)
            assert order is not None
            notif.notify_all("aprovado", order.to_legacy_dict())

            captured = capsys.readouterr()
            assert "WhatsApp" in captured.out
            repo.close()
