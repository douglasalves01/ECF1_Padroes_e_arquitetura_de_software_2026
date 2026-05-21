from typing import Any

from src.services.inventory_interface import InventoryServiceInterface


class InMemoryInventoryService(InventoryServiceInterface):
    def __init__(self) -> None:
        self._stock: dict[str, int] = {
            "produto1": 100,
            "produto2": 50,
            "produto3": 75,
        }

    def validate(self, items: list[dict[str, Any]]) -> bool:
        for item in items:
            name = item["nome"]
            if name not in self._stock:
                print(f"Produto {name} nao encontrado!")
                return False
            if self._stock[name] < item["q"]:
                print(f"Estoque insuficiente para {name}!")
                return False
        return True
