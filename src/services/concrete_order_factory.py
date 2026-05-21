from datetime import datetime

from src.models.order import Order
from src.models.order_item import OrderItem
from src.observers.account_manager_observer import AccountManagerObserver
from src.observers.email_observer import EmailObserver
from src.observers.notification_observer import NotificationObserver
from src.observers.sms_observer import SmsObserver
from src.services.order_factory import OrderConfiguration, OrderFactory
from src.strategies.client_discount_implementations import (
    CorporateClientDiscount,
    NoClientDiscount,
    VipClientDiscount,
)
from src.strategies.item_discount_resolver import calculate_items_subtotal


class ConcreteOrderFactory(OrderFactory):
    def get_configuration(self, customer_type: str) -> OrderConfiguration:
        if customer_type == "vip":
            return OrderConfiguration(
                client_discount=VipClientDiscount(),
                observers=[EmailObserver(), SmsObserver()],
                loyalty_multiplier=2.0,
            )
        if customer_type == "corporativo":
            return OrderConfiguration(
                client_discount=CorporateClientDiscount(),
                observers=[EmailObserver(), AccountManagerObserver()],
                loyalty_multiplier=1.5,
            )
        if customer_type == "normal":
            return OrderConfiguration(
                client_discount=NoClientDiscount(),
                observers=[EmailObserver()],
                loyalty_multiplier=1.0,
            )
        raise ValueError(f"Tipo de cliente invalido: {customer_type}")

    def create_order(
        self,
        customer_name: str,
        items: list[OrderItem],
        customer_type: str,
    ) -> Order:
        config = self.get_configuration(customer_type)
        subtotal = calculate_items_subtotal(items)
        total = config.client_discount.apply(subtotal)
        return Order(
            customer_name=customer_name,
            items=items,
            total=total,
            status="pendente",
            created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            customer_type=customer_type,
            loyalty_multiplier=config.loyalty_multiplier,
        )

    def get_observers(self, customer_type: str) -> list[NotificationObserver]:
        return self.get_configuration(customer_type).observers
