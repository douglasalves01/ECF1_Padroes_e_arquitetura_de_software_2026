from typing import Any

from src.observers.notification_observer import NotificationObserver


class SmsObserver(NotificationObserver):
    def notify(self, event: str, order_data: dict[str, Any]) -> None:
        if order_data["tp"] != "vip":
            return
        client = order_data["cli"]
        if event == "pedido_recebido":
            print(f"SMS enviado para {client}: Pedido VIP recebido!")
        elif event == "aprovado":
            print(f"SMS enviado para {client}: Pedido aprovado!")
