from typing import Any

from hypothesis import given, settings
from hypothesis import strategies as st

from src.observers.notification_observer import NotificationObserver
from src.services.notification_service import NotificationService


class _FailObserver(NotificationObserver):
    def notify(self, event: str, order_data: dict[str, Any]) -> None:
        raise ValueError("boom")


class _CountObserver(NotificationObserver):
    count = 0

    def notify(self, event: str, order_data: dict[str, Any]) -> None:
        _CountObserver.count += 1


@given(n=st.integers(min_value=1, max_value=5))
@settings(max_examples=20)
def test_observer_fault_tolerance(n):
    """Falha em um observer nao impede os demais."""
    service = NotificationService()
    _CountObserver.count = 0
    for _ in range(n):
        service.add_observer(_FailObserver())
    service.add_observer(_CountObserver())
    service.notify_all("evt", {"cli": "A", "tp": "normal", "tot": 1, "id": 1, "st": "x"})
    assert _CountObserver.count == 1


def test_observer_add_remove():
    """Observer removido deixa de ser notificado."""
    service = NotificationService()
    observer = _CountObserver()
    _CountObserver.count = 0
    service.add_observer(observer)
    service.notify_all("evt", {"cli": "A", "tp": "normal", "tot": 1, "id": 1, "st": "x"})
    assert _CountObserver.count == 1
    service.remove_observer(observer)
    service.notify_all("evt", {"cli": "A", "tp": "normal", "tot": 1, "id": 1, "st": "x"})
    assert _CountObserver.count == 1
