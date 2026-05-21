import json
import sqlite3

from src.models.order import Order
from src.models.order_item import OrderItem
from src.repositories.interfaces import OrderRepositoryInterface


class SqliteOrderRepository(OrderRepositoryInterface):
    def __init__(self, db_path: str = "loja.db") -> None:
        self._db = sqlite3.connect(db_path)
        self._cursor = self._db.cursor()
        self._initialize_schema()

    def _initialize_schema(self) -> None:
        self._cursor.execute(
            """CREATE TABLE IF NOT EXISTS ped (
            id INTEGER PRIMARY KEY, cli TEXT, itens TEXT,
            tot REAL, st TEXT, dt TEXT, tp TEXT)"""
        )
        self._db.commit()

    def save(self, order: Order) -> int:
        items_json = json.dumps([item.to_legacy_dict() for item in order.items])
        self._cursor.execute(
            "INSERT INTO ped (cli, itens, tot, st, dt, tp) VALUES (?, ?, ?, ?, ?, ?)",
            (
                order.customer_name,
                items_json,
                order.total,
                order.status,
                order.created_at,
                order.customer_type,
            ),
        )
        self._db.commit()
        row_id = self._cursor.lastrowid
        assert row_id is not None
        return int(row_id)

    def find_by_id(self, order_id: int) -> Order | None:
        self._cursor.execute("SELECT * FROM ped WHERE id=?", (order_id,))
        row = self._cursor.fetchone()
        if row is None:
            return None
        return self._row_to_order(self._cast_row(row))

    def find_by_customer(self, customer_name: str) -> list[Order]:
        self._cursor.execute("SELECT * FROM ped WHERE cli=?", (customer_name,))
        rows = self._cursor.fetchall()
        return [self._row_to_order(self._cast_row(row)) for row in rows]

    def update_status(self, order_id: int, status: str) -> bool:
        if self.find_by_id(order_id) is None:
            return False
        self._cursor.execute("UPDATE ped SET st=? WHERE id=?", (status, order_id))
        self._db.commit()
        return True

    def find_all(self) -> list[Order]:
        self._cursor.execute("SELECT * FROM ped")
        rows = self._cursor.fetchall()
        return [self._row_to_order(self._cast_row(row)) for row in rows]

    def find_distinct_customers(self) -> list[tuple[str, str]]:
        self._cursor.execute("SELECT DISTINCT cli, tp FROM ped")
        return [(row[0], row[1]) for row in self._cursor.fetchall()]

    def close(self) -> None:
        self._db.close()

    @staticmethod
    def _cast_row(
        row: tuple[object, ...],
    ) -> tuple[int, str, str, float, str, str, str]:
        order_id = int(str(row[0]))
        customer = str(row[1])
        items_json = str(row[2])
        total = float(str(row[3]))
        status = str(row[4])
        created_at = str(row[5])
        customer_type = str(row[6])
        return (
            order_id,
            customer,
            items_json,
            total,
            status,
            created_at,
            customer_type,
        )

    @staticmethod
    def _row_to_order(row: tuple[int, str, str, float, str, str, str]) -> Order:
        items_data = json.loads(row[2])
        items = [OrderItem.from_legacy_dict(item) for item in items_data]
        return Order(
            id=row[0],
            customer_name=row[1],
            items=items,
            total=row[3],
            status=row[4],
            created_at=row[5],
            customer_type=row[6],
        )
