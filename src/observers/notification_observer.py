from abc import ABC, abstractmethod
from typing import Any


class NotificationObserver(ABC):
    @abstractmethod
    def notify(self, event: str, order_data: dict[str, Any]) -> None:
        ...
