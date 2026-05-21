from dataclasses import dataclass

from src.repositories.interfaces import OrderRepositoryInterface
from src.repositories.sqlite_repository import SqliteOrderRepository
from src.services.concrete_order_factory import ConcreteOrderFactory
from src.services.inventory_interface import InventoryServiceInterface
from src.services.inventory_service import InMemoryInventoryService
from src.services.notification_service import NotificationService
from src.services.order_service import OrderService
from src.services.payment_service import PaymentService
from src.strategies.payment_implementations import (
    BoletoPaymentStrategy,
    CardPaymentStrategy,
    PixPaymentStrategy,
)
from src.strategies.payment_strategy import PaymentStrategy


@dataclass
class ApplicationContext:
    repository: OrderRepositoryInterface
    order_service: OrderService
    payment_service: PaymentService
    inventory: InventoryServiceInterface
    notification_service: NotificationService


def create_application(*, special: bool = False) -> ApplicationContext:
    repository = SqliteOrderRepository()
    notifications = NotificationService()
    factory = ConcreteOrderFactory()
    order_service = OrderService(
        repository,
        factory,
        notifications,
        special=special,
    )
    strategies: dict[str, PaymentStrategy] = {
        "cartao": CardPaymentStrategy(),
        "pix": PixPaymentStrategy(),
        "boleto": BoletoPaymentStrategy(),
    }
    payment_service = PaymentService(repository, strategies, order_service)
    inventory: InventoryServiceInterface = InMemoryInventoryService()
    return ApplicationContext(
        repository=repository,
        order_service=order_service,
        payment_service=payment_service,
        inventory=inventory,
        notification_service=notifications,
    )
