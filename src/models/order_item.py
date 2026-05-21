from dataclasses import dataclass
from typing import Any


@dataclass
class OrderItem:
    name: str
    price: float
    quantity: int
    discount_type: str

    @classmethod
    def from_legacy_dict(cls, data: dict[str, Any]) -> "OrderItem":
        return cls(
            name=data["nome"],
            price=float(data["p"]),
            quantity=int(data["q"]),
            discount_type=data["tipo"],
        )

    def to_legacy_dict(self) -> dict[str, Any]:
        return {
            "nome": self.name,
            "p": self.price,
            "q": self.quantity,
            "tipo": self.discount_type,
        }
