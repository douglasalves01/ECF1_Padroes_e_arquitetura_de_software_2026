import pytest
from src.strategies.volume_discount_strategy import (
    VOLUME_DISCOUNT_RATE,
    VOLUME_THRESHOLD,
    VolumeDiscountStrategy,
    calculate_subtotal_with_volume_discount,
)


class TestVolumeDiscountStrategy:

    @pytest.mark.parametrize("quantity", [1, 2])
    def test_abaixo_do_limiar_sem_desconto_volume(self, quantity: int) -> None:
        """Menos de 3 unidades não recebe desconto de volume."""
        strategy = VolumeDiscountStrategy("normal")
        result = strategy.calculate(100.0, quantity)
        assert result == pytest.approx(100.0 * quantity)

    @pytest.mark.parametrize("quantity", [3, 4, 5, 10])
    def test_acima_do_limiar_com_desconto_15(self, quantity: int) -> None:
        """3 ou mais unidades recebem 15% de desconto adicional."""
        strategy = VolumeDiscountStrategy("normal")
        expected = 100.0 * quantity * (1.0 - VOLUME_DISCOUNT_RATE)
        result = strategy.calculate(100.0, quantity)
        assert result == pytest.approx(expected)

    def test_limiar_exato_tres_unidades(self) -> None:
        """Exatamente 3 unidades já aplica o desconto."""
        strategy = VolumeDiscountStrategy("normal")
        result = strategy.calculate(100.0, VOLUME_THRESHOLD)
        assert result == pytest.approx(100.0 * VOLUME_THRESHOLD * 0.85)

    def test_compoe_com_desconto_de_item_desc10(self) -> None:
        """Volume se aplica sobre o resultado do desconto de item (desc10)."""
        strategy = VolumeDiscountStrategy("desc10")
        result = strategy.calculate(100.0, 3)
        assert result == pytest.approx(229.5)

    def test_compoe_com_desconto_de_item_desc20(self) -> None:
        """Volume se aplica sobre o resultado do desconto de item (desc20)."""
        strategy = VolumeDiscountStrategy("desc20")
        result = strategy.calculate(100.0, 3)
        assert result == pytest.approx(204.0)

    def test_compoe_com_frete_gratis(self) -> None:
        """frete_gratis sem desconto de item, mas com desconto de volume."""
        strategy = VolumeDiscountStrategy("frete_gratis")
        result = strategy.calculate(100.0, 3)
        assert result == pytest.approx(255.0)

    def test_dois_itens_um_com_volume_outro_sem(self) -> None:
        """Função utilitária aplica volume apenas onde quantidade >= 3."""
        items = [
            {"p": 100, "q": 2, "tipo": "normal"},
            {"p": 100, "q": 3, "tipo": "normal"},
        ]
        result = calculate_subtotal_with_volume_discount(items)
        assert result == pytest.approx(455.0)

    def test_subtotal_multiplos_itens_com_volume(self) -> None:
        """Subtotal correto com vários itens e descontos mistos."""
        items = [
            {"p": 50,  "q": 3, "tipo": "desc10"},
            {"p": 200, "q": 1, "tipo": "desc20"},
            {"p": 100, "q": 5, "tipo": "normal"},
        ]
        result = calculate_subtotal_with_volume_discount(items)
        assert result == pytest.approx(114.75 + 160.0 + 425.0)

    def test_integracao_com_item_discount_resolver(self) -> None:
        """VolumeDiscountStrategy não modifica resolve_item_discount existente."""
        from src.strategies.item_discount_resolver import resolve_item_discount

        # resolve_item_discount original continua funcionando sem volume
        original = resolve_item_discount("normal")
        assert original.calculate(100.0, 3) == pytest.approx(300.0)

        # VolumeDiscountStrategy compõe em cima, sem alterar o original
        volume = VolumeDiscountStrategy("normal")
        assert volume.calculate(100.0, 3) == pytest.approx(255.0)

    def test_nao_modifica_classes_existentes(self) -> None:
        """Garante que classes existentes de desconto não foram alteradas."""
        from src.strategies.discount_implementations import (
            Discount10Strategy,
            Discount20Strategy,
            NoDiscountStrategy,
        )

        assert NoDiscountStrategy().calculate(100.0, 3) == pytest.approx(300.0)
        assert Discount10Strategy().calculate(100.0, 3) == pytest.approx(270.0)
        assert Discount20Strategy().calculate(100.0, 3) == pytest.approx(240.0)
