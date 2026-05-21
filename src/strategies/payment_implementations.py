from src.strategies.payment_strategy import PaymentResult, PaymentStrategy


class _ApprovingPayment(PaymentStrategy):
    def __init__(self, first_message: str, second_message: str) -> None:
        self._first_message = first_message
        self._second_message = second_message

    def process(self, order_total: float, amount_paid: float) -> PaymentResult:
        if amount_paid < order_total:
            return PaymentResult(False, False, "Valor insuficiente!")
        print(self._first_message)
        print(self._second_message)
        return PaymentResult(True, True, "ok")


class CardPaymentStrategy(_ApprovingPayment):
    def __init__(self) -> None:
        super().__init__(
            "Processando pagamento com cartao...",
            "Cartao validado!",
        )


class PixPaymentStrategy(_ApprovingPayment):
    def __init__(self) -> None:
        super().__init__(
            "Gerando QR Code PIX...",
            "PIX recebido!",
        )


class BoletoPaymentStrategy(PaymentStrategy):
    def process(self, order_total: float, amount_paid: float) -> PaymentResult:
        if amount_paid < order_total:
            return PaymentResult(False, False, "Valor insuficiente!")
        print("Gerando boleto...")
        print("Boleto gerado!")
        return PaymentResult(True, False, "ok")
