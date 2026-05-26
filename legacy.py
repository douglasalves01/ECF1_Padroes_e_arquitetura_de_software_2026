import sys
from pathlib import Path
from typing import Any

from src.application import ApplicationContext, create_application
from src.models.order_item import OrderItem
from src.repositories.sqlite_repository import SqliteOrderRepository

_ROOT = Path(__file__).resolve().parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

class Sis:
    def __init__(self) -> None:
        self._ctx: ApplicationContext = create_application(special=False)
        repo = self._ctx.repository
        if isinstance(repo, SqliteOrderRepository):
            self.db = repo._db
            self.c = repo._cursor

    def add_ped(self, n: str, its: list[dict[str, Any]], t: str) -> int:
        items = [OrderItem.from_legacy_dict(item) for item in its]
        return self._ctx.order_service.create_order(n, items, t)

    def get_ped(self, id: int) -> dict[str, Any] | None:
        order = self._ctx.order_service.get_order(id)
        if order is None:
            return None
        return order.to_legacy_dict()

    def upd_st(self, id: int, s: str) -> None:
        self._ctx.order_service.update_status(id, s, enforce_transitions=False)

    def calc_tot_cli(self, n: str) -> float:
        return self._ctx.order_service.get_customer_total(n)

    def gerar_rel(self, tipo: str) -> None:
        self._ctx.order_service.generate_report(tipo)

    def proc_pag(self, id: int, m: str, vl: float) -> bool:
        return self._ctx.payment_service.process_payment(id, m, vl)

    def validar_estoque(self, its: list[dict[str, Any]]) -> bool:
        return self._ctx.inventory.validate(its)

    def cancelar_pedido(self, id: int) -> None:
        self._ctx.order_service.cancel_order(id)

    def close(self) -> None:
        self._ctx.repository.close()


class PedEspecial:
    def __init__(self) -> None:
        self._ctx: ApplicationContext = create_application(special=True)
        repo = self._ctx.repository
        if isinstance(repo, SqliteOrderRepository):
            self.db = repo._db
            self.c = repo._cursor

    def add_ped(self, n: str, its: list[dict[str, Any]], t: str) -> int:
        items = [OrderItem.from_legacy_dict(item) for item in its]
        return self._ctx.order_service.create_order(n, items, t)

    def get_ped(self, id: int) -> dict[str, Any] | None:
        order = self._ctx.order_service.get_order(id)
        if order is None:
            return None
        return order.to_legacy_dict()

    def upd_st(self, id: int, s: str) -> None:
        self._ctx.order_service.update_status(id, s, enforce_transitions=False)

    def calc_tot_cli(self, n: str) -> float:
        return self._ctx.order_service.get_customer_total(n)

    def gerar_rel(self, tipo: str) -> None:
        self._ctx.order_service.generate_report(tipo)

    def proc_pag(self, id: int, m: str, vl: float) -> bool:
        return self._ctx.payment_service.process_payment(id, m, vl)

    def validar_estoque(self, its: list[dict[str, Any]]) -> bool:
        return self._ctx.inventory.validate(its)

    def cancelar_pedido(self, id: int) -> None:
        self._ctx.order_service.cancel_order(id)

    def close(self) -> None:
        self._ctx.repository.close()


def main() -> None:
    s = Sis()
    its1 = [
        {"nome": "produto1", "p": 100, "q": 2, "tipo": "normal"},
        {"nome": "produto2", "p": 50, "q": 1, "tipo": "desc10"},
    ]
    if s.validar_estoque(its1):
        id1 = s.add_ped("Joao Silva", its1, "normal")
        print(f"Pedido {id1} criado!")
        s.proc_pag(id1, "cartao", 250)
        s.upd_st(id1, "enviado")
        s.upd_st(id1, "entregue")

    its2 = [{"nome": "produto3", "p": 200, "q": 1, "tipo": "desc20"}]
    if s.validar_estoque(its2):
        id2 = s.add_ped("Maria Santos", its2, "vip")
        s.proc_pag(id2, "pix", 160)

    its3 = [{"nome": "produto1", "p": 100, "q": 5, "tipo": "normal"}]
    if s.validar_estoque(its3):
        id3 = s.add_ped("Empresa XYZ", its3, "corporativo")
        s.proc_pag(id3, "boleto", 500)

    s.gerar_rel("vendas")
    print()
    s.gerar_rel("clientes")
    s.close()


if __name__ == "__main__":
    main()
