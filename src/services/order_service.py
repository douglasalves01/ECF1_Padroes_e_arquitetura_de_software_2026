from datetime import datetime

from src.models.order import Order
from src.models.order_item import OrderItem
from src.observers.special_order_observer import SpecialOrderObserver
from src.repositories.interfaces import OrderRepositoryInterface
from src.services.notification_service import NotificationService
from src.services.order_factory import OrderFactory
from src.strategies.item_discount_resolver import calculate_special_subtotal

_VALID_TRANSITIONS: dict[str, set[str]] = {
    "pendente": {"aprovado", "cancelado"},
    "aprovado": {"enviado", "cancelado"},
    "enviado": {"entregue", "cancelado"},
    "entregue": set(),
    "cancelado": set(),
}


class OrderService:
    def __init__(
        self,
        repository: OrderRepositoryInterface,
        factory: OrderFactory,
        notification_service: NotificationService,
        *,
        special: bool = False,
    ) -> None:
        self._repository = repository
        self._factory = factory
        self._notifications = notification_service
        self._special = special

    def create_order(
        self,
        customer_name: str,
        items: list[OrderItem],
        customer_type: str,
    ) -> int:
        if self._special:
            order = self._create_special_order(customer_name, items, customer_type)
            self._notifications.clear_observers()
            self._notifications.add_observer(SpecialOrderObserver())
            event = "pedido_recebido"
        else:
            order = self._factory.create_order(customer_name, items, customer_type)
            self._notifications.clear_observers()
            for observer in self._factory.get_configuration(customer_type).observers:
                self._notifications.add_observer(observer)
            event = "pedido_recebido"

        order_id = self._repository.save(order)
        order.id = order_id
        self._notifications.notify_all(event, order.to_legacy_dict())
        return order_id

    def get_order(self, order_id: int) -> Order | None:
        return self._repository.find_by_id(order_id)

    def update_status(
        self,
        order_id: int,
        new_status: str,
        *,
        enforce_transitions: bool = False,
    ) -> bool:
        order = self._repository.find_by_id(order_id)
        if order is None:
            return False

        invalid = enforce_transitions and not self._is_valid_transition(
            order.status, new_status
        )
        if invalid:
            return False

        self._repository.update_status(order_id, new_status)
        order.status = new_status
        order_data = order.to_legacy_dict()

        if self._special:
            self._notifications.clear_observers()
            self._notifications.add_observer(SpecialOrderObserver())
            self._notifications.notify_all("status_atualizado", order_data)
            return True

        self._configure_observers(order.customer_type)
        if new_status in {"aprovado", "enviado", "entregue"}:
            self._notifications.notify_all(new_status, order_data)
        return True

    def _configure_observers(self, customer_type: str) -> None:
        self._notifications.clear_observers()
        for observer in self._factory.get_configuration(customer_type).observers:
            self._notifications.add_observer(observer)

    def cancel_order(self, order_id: int) -> bool:
        order = self._repository.find_by_id(order_id)
        if order is None:
            return False
        self._repository.update_status(order_id, "cancelado")
        print(f"Pedido {order_id} cancelado")
        return True

    def get_customer_total(self, customer_name: str) -> float:
        orders = self._repository.find_by_customer(customer_name)
        return sum(order.total for order in orders)

    def generate_report(self, report_type: str) -> None:
        if report_type == "vendas":
            self._generate_sales_report()
        elif report_type == "clientes":
            self._generate_clients_report()

    def _create_special_order(
        self,
        customer_name: str,
        items: list[OrderItem],
        customer_type: str,
    ) -> Order:
        total = calculate_special_subtotal(items)
        return Order(
            customer_name=customer_name,
            items=items,
            total=total,
            status="pendente",
            created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            customer_type=customer_type,
            loyalty_multiplier=1.0,
        )

    @staticmethod
    def _is_valid_transition(current: str, new_status: str) -> bool:
        if new_status == "cancelado":
            return True
        allowed = _VALID_TRANSITIONS.get(current, set())
        return new_status in allowed

    def _generate_sales_report(self) -> None:
        orders = self._repository.find_all()
        print("=== RELATORIO DE VENDAS ===")
        total_geral = 0.0
        for order in orders:
            print(
                f"Pedido #{order.id} - Cliente: {order.customer_name} - "
                f"Total: R${order.total:.2f} - Status: {order.status}"
            )
            total_geral += order.total
        print(f"Total Geral: R${total_geral:.2f}")
        with open("rel_vendas.txt", "w") as file:
            file.write(f"Total de vendas: {total_geral}")

    def _generate_clients_report(self) -> None:
        clients = self._repository.find_distinct_customers()
        print("=== RELATORIO DE CLIENTES ===")
        for name, client_type in clients:
            total = self.get_customer_total(name)
            print(f"Cliente: {name} ({client_type}) - Total gasto: R${total:.2f}")
        with open("rel_clientes.txt", "w") as file:
            for name, client_type in clients:
                file.write(f"{name},{client_type}\n")
