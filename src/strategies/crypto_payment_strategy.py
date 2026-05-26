from src.strategies.payment_strategy import PaymentResult, PaymentStrategy

CRYPTO_FEE_RATE: float = 0.02

class CryptoPaymentStrategy(PaymentStrategy):
    def process(self, order_total: float, amount_paid: float) -> PaymentResult:
        fee = order_total * CRYPTO_FEE_RATE
        total_with_fee = order_total + fee

        if amount_paid < total_with_fee:
            print(
                f"Valor insuficiente para pagamento em cripto! "
                f"Total com taxa (2%): R${total_with_fee:.2f}"
            )
            return PaymentResult(False, False, "Valor insuficiente para cripto!")

        print("Processando pagamento em criptomoeda...")
        print(f"Taxa de servico (2%): R${fee:.2f}")
        print("Transacao cripto confirmada!")
        return PaymentResult(True, True, "ok")