from src.repositories.interfaces import OrderRepositoryInterface
from src.services.order_service import OrderService
from src.strategies.payment_strategy import PaymentStrategy


class PaymentService:
    def __init__(
        self,
        repository: OrderRepositoryInterface,
        strategies: dict[str, PaymentStrategy],
        order_service: OrderService,
    ) -> None:
        self._repository = repository
        self._strategies = strategies
        self._order_service = order_service

    def process_payment(self, order_id: int, method: str, amount: float) -> bool:
        order = self._repository.find_by_id(order_id)
        if order is None:
            return False
        if amount < order.total:
            print("Valor insuficiente!")
            return False

        strategy = self._strategies.get(method)
        if strategy is None:
            print("Metodo de pagamento invalido!")
            return False

        result = strategy.process(order.total, amount)
        if not result.success:
            return False
        if result.approves_order:
            self._order_service.update_status(order_id, "aprovado")
        return True
