from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class PaymentResult:
    success: bool
    approves_order: bool
    message: str


class PaymentStrategy(ABC):
    @abstractmethod
    def process(self, order_total: float, amount_paid: float) -> PaymentResult:
        ...
