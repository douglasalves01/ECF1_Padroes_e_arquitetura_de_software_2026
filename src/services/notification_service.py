from typing import Any

from src.observers.notification_observer import NotificationObserver


class NotificationService:
    def __init__(self) -> None:
        self._observers: list[NotificationObserver] = []

    def add_observer(self, observer: NotificationObserver) -> None:
        self._observers.append(observer)

    def remove_observer(self, observer: NotificationObserver) -> None:
        self._observers.remove(observer)

    def notify_all(self, event: str, order_data: dict[str, Any]) -> None:
        for observer in list(self._observers):
            try:
                observer.notify(event, order_data)
            except Exception:
                continue

    def clear_observers(self) -> None:
        self._observers.clear()
