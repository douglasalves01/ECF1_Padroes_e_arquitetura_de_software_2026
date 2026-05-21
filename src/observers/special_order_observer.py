from typing import Any

from src.observers.notification_observer import NotificationObserver


class SpecialOrderObserver(NotificationObserver):
    def notify(self, event: str, order_data: dict[str, Any]) -> None:
        if event == "pedido_recebido":
            client = order_data["cli"]
            print(f"Email especial enviado para {client}: Pedido especial recebido!")
        elif event == "status_atualizado":
            order_id = order_data["id"]
            status = order_data["st"]
            print(f"Pedido especial {order_id} -> {status}")
