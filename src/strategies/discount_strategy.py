from abc import ABC, abstractmethod


class ItemDiscountStrategy(ABC):
    @abstractmethod
    def calculate(self, price: float, quantity: int) -> float:
        ...


class ClientDiscountStrategy(ABC):
    @abstractmethod
    def apply(self, subtotal: float) -> float:
        ...
