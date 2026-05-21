from abc import ABC, abstractmethod

from src.models.order import Order


class OrderRepositoryInterface(ABC):
    @abstractmethod
    def save(self, order: Order) -> int:
        ...

    @abstractmethod
    def find_by_id(self, order_id: int) -> Order | None:
        ...

    @abstractmethod
    def find_by_customer(self, customer_name: str) -> list[Order]:
        ...

    @abstractmethod
    def update_status(self, order_id: int, status: str) -> bool:
        ...

    @abstractmethod
    def find_all(self) -> list[Order]:
        ...

    @abstractmethod
    def find_distinct_customers(self) -> list[tuple[str, str]]:
        ...

    @abstractmethod
    def close(self) -> None:
        ...
