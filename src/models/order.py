from dataclasses import dataclass
from typing import Any

from src.models.order_item import OrderItem


@dataclass
class Order:
    customer_name: str
    items: list[OrderItem]
    total: float
    status: str
    created_at: str
    customer_type: str
    id: int | None = None
    loyalty_multiplier: float = 1.0

    def to_legacy_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "cli": self.customer_name,
            "itens": [item.to_legacy_dict() for item in self.items],
            "tot": self.total,
            "st": self.status,
            "dt": self.created_at,
            "tp": self.customer_type,
        }
