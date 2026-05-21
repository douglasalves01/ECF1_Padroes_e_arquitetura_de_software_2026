from abc import ABC, abstractmethod
from typing import Any


class InventoryServiceInterface(ABC):
    @abstractmethod
    def validate(self, items: list[dict[str, Any]]) -> bool:
        ...
