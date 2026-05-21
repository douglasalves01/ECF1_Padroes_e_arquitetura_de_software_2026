from src.application import create_application


def run_demo() -> None:
    ctx = create_application(special=False)
    order_service = ctx.order_service
    payment_service = ctx.payment_service
    inventory = ctx.inventory

    items1 = [
        {"nome": "produto1", "p": 100, "q": 2, "tipo": "normal"},
        {"nome": "produto2", "p": 50, "q": 1, "tipo": "desc10"},
    ]
    if inventory.validate(items1):
        from src.models.order_item import OrderItem

        order_items = [OrderItem.from_legacy_dict(i) for i in items1]
        order_id = order_service.create_order("Joao Silva", order_items, "normal")
        print(f"Pedido {order_id} criado!")
        payment_service.process_payment(order_id, "cartao", 250)
        order_service.update_status(order_id, "enviado", enforce_transitions=False)
        order_service.update_status(order_id, "entregue", enforce_transitions=False)

    ctx.repository.close()


if __name__ == "__main__":
    run_demo()
