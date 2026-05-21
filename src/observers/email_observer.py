from typing import Any

from src.observers.notification_observer import NotificationObserver


class EmailObserver(NotificationObserver):
    def notify(self, event: str, order_data: dict[str, Any]) -> None:
        client = order_data["cli"]
        if event == "pedido_recebido":
            print(f"Email enviado para {client}: Pedido recebido!")
        elif event == "aprovado":
            print(f"Email enviado para {client}: Pedido aprovado!")
        elif event == "enviado":
            print(f"Email enviado para {client}: Pedido enviado!")
        elif event == "entregue":
            print(f"Email enviado para {client}: Pedido entregue!")
            self._print_loyalty(order_data)

    @staticmethod
    def _print_loyalty(order_data: dict[str, Any]) -> None:
        total = order_data["tot"]
        client_type = order_data["tp"]
        if client_type == "vip":
            pts = int(total * 2)
            print(f"Cliente VIP ganhou {pts} pontos!")
        elif client_type == "corporativo":
            pts = int(total * 1.5)
            print(f"Cliente corporativo ganhou {pts} pontos!")
        else:
            pts = int(total)
            print(f"Cliente ganhou {pts} pontos!")
