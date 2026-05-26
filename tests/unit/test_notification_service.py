from typing import Any

from src.observers.notification_observer import NotificationObserver
from src.services.notification_service import NotificationService


class _FailingObserver(NotificationObserver):
    def notify(self, event: str, order_data: dict[str, Any]) -> None:
        raise RuntimeError("fail")


class _RecordingObserver(NotificationObserver):
    def __init__(self) -> None:
        self.events: list[str] = []

    def notify(self, event: str, order_data: dict[str, Any]) -> None:
        self.events.append(event)

def test_add_remove_observer() -> None:
    """Adiciona e remove observer da lista."""
    service = NotificationService()
    observer = _RecordingObserver()
    service.add_observer(observer)
    service.notify_all(
        "teste",
        {
            "cli": "A",
            "tp": "normal",
            "tot": 1,
            "id": 1,
            "st": "x",
        },
    )
    assert observer.events == ["teste"]
    service.remove_observer(observer)
    service.notify_all(
        "teste",
        {
            "cli": "A",
            "tp": "normal",
            "tot": 1,
            "id": 1,
            "st": "x",
        },
    )
    assert observer.events == ["teste"]


def test_fault_tolerance() -> None:
    """Continua notificando se um observer falhar."""
    service = NotificationService()
    ok = _RecordingObserver()
    service.add_observer(_FailingObserver())
    service.add_observer(ok)
    service.notify_all(
        "evt",
        {
            "cli": "A",
            "tp": "normal",
            "tot": 1,
            "id": 1,
            "st": "x"
        }
    )
    assert ok.events == ["evt"]
