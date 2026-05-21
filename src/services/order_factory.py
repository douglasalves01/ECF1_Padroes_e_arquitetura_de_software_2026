from abc import ABC, abstractmethod
from dataclasses import dataclass

from src.models.order import Order
from src.models.order_item import OrderItem
from src.observers.notification_observer import NotificationObserver
from src.strategies.discount_strategy import ClientDiscountStrategy


@dataclass
class OrderConfiguration:
    client_discount: ClientDiscountStrategy
    observers: list[NotificationObserver]
    loyalty_multiplier: float


class OrderFactory(ABC):
    @abstractmethod
    def create_order(
        self,
        customer_name: str,
        items: list[OrderItem],
        customer_type: str,
    ) -> Order:
        ...

    @abstractmethod
    def get_configuration(self, customer_type: str) -> OrderConfiguration:
        ...
