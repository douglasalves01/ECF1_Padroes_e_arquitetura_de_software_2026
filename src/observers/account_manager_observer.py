from typing import Any

from src.observers.notification_observer import NotificationObserver


class AccountManagerObserver(NotificationObserver):
    def notify(self, event: str, order_data: dict[str, Any]) -> None:
        if event != "pedido_recebido" or order_data["tp"] != "corporativo":
            return
        client = order_data["cli"]
        print(f"Notificacao enviada ao gerente de conta de {client}")
