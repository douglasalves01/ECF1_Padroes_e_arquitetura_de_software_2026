import pytest
from src.strategies.crypto_payment_strategy import (
    CRYPTO_FEE_RATE,
    CryptoPaymentStrategy,
)

@pytest.fixture
def strategy() -> CryptoPaymentStrategy:
    return CryptoPaymentStrategy()


class TestCryptoPaymentStrategy:

    def test_pagamento_exato_com_taxa_aprovado(self, strategy: CryptoPaymentStrategy) -> None:
        """Pagar exatamente total + 2% deve aprovar."""
        total = 100.0
        fee = total * CRYPTO_FEE_RATE
        result = strategy.process(total, total + fee)
        assert result.success is True
        assert result.approves_order is True

    def test_pagamento_acima_do_necessario_aprovado(self, strategy: CryptoPaymentStrategy) -> None:
        """Pagar acima de total + 2% deve aprovar."""
        result = strategy.process(100.0, 200.0)
        assert result.success is True
        assert result.approves_order is True

    def test_pagamento_sem_taxa_recusado(self, strategy: CryptoPaymentStrategy) -> None:
        """Pagar apenas o total sem incluir a taxa deve ser recusado."""
        result = strategy.process(100.0, 100.0)
        assert result.success is False
        assert result.approves_order is False

    def test_pagamento_insuficiente_recusado(self, strategy: CryptoPaymentStrategy) -> None:
        """Valor abaixo do total também deve ser recusado."""
        result = strategy.process(100.0, 50.0)
        assert result.success is False

    def test_taxa_calculada_corretamente(self, strategy: CryptoPaymentStrategy) -> None:
        """Taxa de 2% deve ser calculada sobre o total do pedido."""
        order_total = 200.0
        expected_fee = 4.0
        total_needed = order_total + expected_fee

        # Pagando exatamente o total com taxa deve passar
        result = strategy.process(order_total, total_needed)
        assert result.success is True

        # Pagando 1 centavo a menos deve falhar
        result_fail = strategy.process(order_total, total_needed - 0.01)
        assert result_fail.success is False

    def test_mensagem_de_erro_informativa(
        self, strategy: CryptoPaymentStrategy, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Mensagem de erro deve mencionar a taxa e o valor total."""
        strategy.process(100.0, 100.0)
        captured = capsys.readouterr()
        assert "102" in captured.out
        assert "2%" in captured.out

    def test_mensagem_de_sucesso(
        self, strategy: CryptoPaymentStrategy, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Pagamento aprovado deve imprimir confirmação."""
        strategy.process(100.0, 102.0)
        captured = capsys.readouterr()
        assert "cripto" in captured.out.lower()
        assert "confirmada" in captured.out.lower()

    def test_integracao_com_payment_service(self) -> None:
        """CryptoPaymentStrategy deve ser registrável no dicionário de strategies sem alterar PaymentService."""
        from src.services.notification_service import NotificationService
        from src.services.order_service import OrderService
        from src.services.concrete_order_factory import ConcreteOrderFactory
        from src.services.payment_service import PaymentService
        from src.repositories.sqlite_repository import SqliteOrderRepository
        from src.strategies.payment_implementations import CardPaymentStrategy
        from src.strategies.payment_strategy import PaymentStrategy
        import tempfile, os

        with tempfile.TemporaryDirectory() as tmp:
            db_path = os.path.join(tmp, "test.db")
            repo = SqliteOrderRepository(db_path)
            notif = NotificationService()
            factory = ConcreteOrderFactory()
            order_service = OrderService(repo, factory, notif)
            strategies: dict[str, PaymentStrategy] = {
                "cartao": CardPaymentStrategy(),
                "cripto": CryptoPaymentStrategy(),
            }
            payment_service = PaymentService(repo, strategies, order_service)

            from src.models.order_item import OrderItem
            items = [OrderItem(name="p1", price=100.0, quantity=1, discount_type="normal")]
            order_id = order_service.create_order("Jorge", items, "normal")

            result = payment_service.process_payment(order_id, "cripto", 102.0)
            assert result is True

            order = repo.find_by_id(order_id)
            assert order is not None
            assert order.status == "aprovado"
            repo.close()