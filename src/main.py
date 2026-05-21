from src.application import create_application
from src.models.order_item import OrderItem


def run_demo() -> None:
    ctx = create_application(special=False)
    order_service = ctx.order_service
    payment_service = ctx.payment_service
    inventory = ctx.inventory

    its1 = [
        {"nome": "produto1", "p": 100, "q": 2, "tipo": "normal"},
        {"nome": "produto2", "p": 50, "q": 1, "tipo": "desc10"},
    ]
    if inventory.validate(its1):
        items1 = [OrderItem.from_legacy_dict(i) for i in its1]
        id1 = order_service.create_order("Joao Silva", items1, "normal")
        print(f"Pedido {id1} criado!")
        payment_service.process_payment(id1, "cartao", 250)
        order_service.update_status(id1, "enviado", enforce_transitions=False)
        order_service.update_status(id1, "entregue", enforce_transitions=False)

    its2 = [{"nome": "produto3", "p": 200, "q": 1, "tipo": "desc20"}]
    if inventory.validate(its2):
        items2 = [OrderItem.from_legacy_dict(i) for i in its2]
        id2 = order_service.create_order("Maria Santos", items2, "vip")
        payment_service.process_payment(id2, "pix", 160)

    its3 = [{"nome": "produto1", "p": 100, "q": 5, "tipo": "normal"}]
    if inventory.validate(its3):
        items3 = [OrderItem.from_legacy_dict(i) for i in its3]
        id3 = order_service.create_order("Empresa XYZ", items3, "corporativo")
        payment_service.process_payment(id3, "boleto", 500)

    order_service.generate_report("vendas")
    print()
    order_service.generate_report("clientes")
    ctx.repository.close()


if __name__ == "__main__":
    run_demo()
