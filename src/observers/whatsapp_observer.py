from typing import Any
from src.observers.notification_observer import NotificationObserver

_WHATSAPP_EVENTS: frozenset[str] = frozenset(
    {"pedido_recebido", "aprovado", "enviado", "entregue"}
)

_MESSAGES: dict[str, str] = {
    "pedido_recebido": "Pedido recebido com sucesso!",
    "aprovado": "Seu pedido foi aprovado!",
    "enviado": "Seu pedido foi enviado!",
    "entregue": "Seu pedido foi entregue!",
}


class WhatsAppObserver(NotificationObserver):

    def notify(self, event: str, order_data: dict[str, Any]) -> None:
        if event not in _WHATSAPP_EVENTS:
            return
        client = order_data["cli"]
        message = _MESSAGES.get(event, f"Atualizacao do pedido: {event}")
        print(f"WhatsApp enviado para {client}: {message}")