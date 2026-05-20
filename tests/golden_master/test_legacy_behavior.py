"""
Golden Master Tests — Testes de caracterização do sistema legado.

Capturam o comportamento exato das classes Sis e PedEspecial para garantir
que a refatoração não introduza regressões.
"""
import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from legacy import Sis, PedEspecial


# ============================================================
# Fixtures
# ============================================================

@pytest.fixture
def sis(tmp_path, monkeypatch):
    """Isola o banco em diretório temporário por teste."""
    monkeypatch.chdir(tmp_path)
    s = Sis()
    yield s
    s.close()


@pytest.fixture
def ped_especial(tmp_path, monkeypatch):
    """Isola o banco em diretório temporário para PedEspecial."""
    monkeypatch.chdir(tmp_path)
    s = PedEspecial()
    yield s
    s.close()


# ============================================================
# Task 2.1 — Criação de pedidos e cálculo de total
# Requirements: 1.2, 1.3, 1.4, 1.11, 14.2, 14.3
# ============================================================

class TestOrderCreationAndTotal:
    """Golden Master: criação de pedidos e cálculo de totais."""

    def test_pedido_normal_calcula_total_corretamente(self, sis):
        """Itens normal + desc10: 100*2 + 50*1*0.9 = 245.0"""
        itens = [
            {'nome': 'produto1', 'p': 100, 'q': 2, 'tipo': 'normal'},
            {'nome': 'produto2', 'p': 50, 'q': 1, 'tipo': 'desc10'},
        ]
        id_ped = sis.add_ped('Joao Silva', itens, 'normal')
        pedido = sis.get_ped(id_ped)
        assert pedido['tot'] == pytest.approx(245.0)
        assert pedido['st'] == 'pendente'

    def test_pedido_com_todos_tipos_desconto(self, sis):
        """normal + desc10 + desc20 + frete_gratis."""
        itens = [
            {'nome': 'produto1', 'p': 100, 'q': 1, 'tipo': 'normal'},       # 100
            {'nome': 'produto2', 'p': 100, 'q': 1, 'tipo': 'desc10'},       # 90
            {'nome': 'produto3', 'p': 100, 'q': 1, 'tipo': 'desc20'},       # 80
            {'nome': 'produto1', 'p': 100, 'q': 1, 'tipo': 'frete_gratis'}, # 100
        ]
        id_ped = sis.add_ped('Cliente', itens, 'normal')
        pedido = sis.get_ped(id_ped)
        # 100 + 90 + 80 + 100 = 370
        assert pedido['tot'] == pytest.approx(370.0)

    def test_pedido_vip_aplica_desconto_5_porcento(self, sis):
        """VIP: total * 0.95"""
        itens = [{'nome': 'produto1', 'p': 100, 'q': 1, 'tipo': 'normal'}]
        id_ped = sis.add_ped('Maria', itens, 'vip')
        pedido = sis.get_ped(id_ped)
        assert pedido['tot'] == pytest.approx(95.0)

    def test_pedido_vip_com_desconto_item(self, sis):
        """VIP com desc10: 100*2*0.9 = 180, depois *0.95 = 171.0"""
        itens = [{'nome': 'produto1', 'p': 100, 'q': 2, 'tipo': 'desc10'}]
        id_ped = sis.add_ped('Maria VIP', itens, 'vip')
        pedido = sis.get_ped(id_ped)
        assert pedido['tot'] == pytest.approx(171.0)

    def test_pedido_corporativo_aplica_desconto_10_porcento(self, sis):
        """Corporativo: total * 0.90"""
        itens = [{'nome': 'produto1', 'p': 100, 'q': 1, 'tipo': 'normal'}]
        id_ped = sis.add_ped('Empresa', itens, 'corporativo')
        pedido = sis.get_ped(id_ped)
        assert pedido['tot'] == pytest.approx(90.0)

    def test_pedido_corporativo_com_desconto_item(self, sis):
        """Corporativo com desc20: 200*1*0.8 = 160, depois *0.90 = 144.0"""
        itens = [{'nome': 'produto3', 'p': 200, 'q': 1, 'tipo': 'desc20'}]
        id_ped = sis.add_ped('Corp XYZ', itens, 'corporativo')
        pedido = sis.get_ped(id_ped)
        assert pedido['tot'] == pytest.approx(144.0)

    def test_pedido_especial_calcula_com_sobretaxa_15(self, ped_especial):
        """PedEspecial: soma itens (ignora frete_gratis) * 1.15"""
        itens = [
            {'nome': 'produto1', 'p': 100, 'q': 2, 'tipo': 'normal'},       # 200
            {'nome': 'produto2', 'p': 50, 'q': 1, 'tipo': 'desc10'},        # 45
            {'nome': 'produto3', 'p': 30, 'q': 1, 'tipo': 'frete_gratis'},  # ignorado
        ]
        id_ped = ped_especial.add_ped('Especial', itens, 'normal')
        pedido = ped_especial.get_ped(id_ped)
        # (200 + 45) * 1.15 = 281.75
        assert pedido['tot'] == pytest.approx(281.75)

    def test_pedido_especial_ignora_desconto_cliente(self, ped_especial):
        """PedEspecial ignora desconto de tipo de cliente."""
        itens = [{'nome': 'produto1', 'p': 100, 'q': 1, 'tipo': 'normal'}]
        id_ped = ped_especial.add_ped('VIP Especial', itens, 'vip')
        pedido = ped_especial.get_ped(id_ped)
        # 100 * 1.15 = 115.0 (sem desconto VIP)
        assert pedido['tot'] == pytest.approx(115.0)

    def test_pedido_status_inicial_pendente(self, sis):
        """Todo pedido inicia com status 'pendente'."""
        itens = [{'nome': 'produto1', 'p': 50, 'q': 1, 'tipo': 'normal'}]
        id_ped = sis.add_ped('Teste', itens, 'normal')
        pedido = sis.get_ped(id_ped)
        assert pedido['st'] == 'pendente'

    def test_pedido_armazena_dados_cliente(self, sis):
        """Verifica que nome do cliente e tipo são armazenados."""
        itens = [{'nome': 'produto1', 'p': 10, 'q': 1, 'tipo': 'normal'}]
        id_ped = sis.add_ped('Carlos', itens, 'vip')
        pedido = sis.get_ped(id_ped)
        assert pedido['cli'] == 'Carlos'
        assert pedido['tp'] == 'vip'


# ============================================================
# Task 2.2 — Processamento de pagamento
# Requirements: 1.5, 1.6, 1.12, 14.7
# ============================================================

class TestPaymentProcessing:
    """Golden Master: processamento de pagamentos."""

    def test_cartao_aprova_pedido(self, sis):
        """Cartão com valor suficiente → True, status 'aprovado'."""
        itens = [{'nome': 'produto1', 'p': 100, 'q': 1, 'tipo': 'normal'}]
        id_ped = sis.add_ped('Joao', itens, 'normal')
        result = sis.proc_pag(id_ped, 'cartao', 100)
        assert result is True
        assert sis.get_ped(id_ped)['st'] == 'aprovado'

    def test_cartao_valor_maior_que_total(self, sis):
        """Cartão com valor acima do total → True, status 'aprovado'."""
        itens = [{'nome': 'produto1', 'p': 100, 'q': 1, 'tipo': 'normal'}]
        id_ped = sis.add_ped('Joao', itens, 'normal')
        result = sis.proc_pag(id_ped, 'cartao', 200)
        assert result is True
        assert sis.get_ped(id_ped)['st'] == 'aprovado'

    def test_pix_aprova_pedido(self, sis):
        """PIX com valor suficiente → True, status 'aprovado'."""
        itens = [{'nome': 'produto1', 'p': 100, 'q': 1, 'tipo': 'normal'}]
        id_ped = sis.add_ped('Joao', itens, 'normal')
        result = sis.proc_pag(id_ped, 'pix', 100)
        assert result is True
        assert sis.get_ped(id_ped)['st'] == 'aprovado'

    def test_boleto_nao_aprova_pedido(self, sis):
        """Boleto com valor suficiente → True, status permanece 'pendente'."""
        itens = [{'nome': 'produto1', 'p': 100, 'q': 1, 'tipo': 'normal'}]
        id_ped = sis.add_ped('Joao', itens, 'normal')
        result = sis.proc_pag(id_ped, 'boleto', 100)
        assert result is True
        assert sis.get_ped(id_ped)['st'] == 'pendente'

    def test_pagamento_insuficiente_falha(self, sis):
        """Valor insuficiente → False, status inalterado."""
        itens = [{'nome': 'produto1', 'p': 100, 'q': 1, 'tipo': 'normal'}]
        id_ped = sis.add_ped('Joao', itens, 'normal')
        result = sis.proc_pag(id_ped, 'cartao', 50)
        assert result is False
        assert sis.get_ped(id_ped)['st'] == 'pendente'

    def test_metodo_pagamento_invalido(self, sis):
        """Método inválido → False, status inalterado."""
        itens = [{'nome': 'produto1', 'p': 100, 'q': 1, 'tipo': 'normal'}]
        id_ped = sis.add_ped('Joao', itens, 'normal')
        result = sis.proc_pag(id_ped, 'cheque', 100)
        assert result is False
        assert sis.get_ped(id_ped)['st'] == 'pendente'

    def test_pagamento_pedido_inexistente(self, sis):
        """Pedido inexistente → False."""
        result = sis.proc_pag(999, 'cartao', 100)
        assert result is False


# ============================================================
# Task 2.3 — Status, fidelidade, cancelamento, estoque
# Requirements: 1.7, 1.8, 1.9, 14.4, 14.6
# ============================================================

class TestStatusLoyaltyCancellationStock:
    """Golden Master: atualização de status, pontos, cancelamento, estoque."""

    def test_entrega_pontos_cliente_normal(self, sis, capsys):
        """Entrega normal: pontos = int(total * 1)."""
        itens = [{'nome': 'produto1', 'p': 100, 'q': 1, 'tipo': 'normal'}]
        id_ped = sis.add_ped('Joao', itens, 'normal')
        sis.proc_pag(id_ped, 'cartao', 100)
        sis.upd_st(id_ped, 'enviado')
        sis.upd_st(id_ped, 'entregue')
        pedido = sis.get_ped(id_ped)
        assert pedido['st'] == 'entregue'
        captured = capsys.readouterr()
        assert 'Cliente ganhou 100 pontos!' in captured.out

    def test_entrega_pontos_cliente_vip(self, sis, capsys):
        """Entrega VIP: pontos = int(total * 2)."""
        itens = [{'nome': 'produto1', 'p': 100, 'q': 1, 'tipo': 'normal'}]
        id_ped = sis.add_ped('Maria', itens, 'vip')
        # total = 100 * 0.95 = 95.0
        sis.proc_pag(id_ped, 'cartao', 95)
        sis.upd_st(id_ped, 'enviado')
        sis.upd_st(id_ped, 'entregue')
        pedido = sis.get_ped(id_ped)
        assert pedido['st'] == 'entregue'
        captured = capsys.readouterr()
        # int(95 * 2) = 190
        assert 'Cliente VIP ganhou 190 pontos!' in captured.out

    def test_entrega_pontos_cliente_corporativo(self, sis, capsys):
        """Entrega corporativo: pontos = int(total * 1.5)."""
        itens = [{'nome': 'produto1', 'p': 100, 'q': 1, 'tipo': 'normal'}]
        id_ped = sis.add_ped('Empresa', itens, 'corporativo')
        # total = 100 * 0.90 = 90.0
        sis.proc_pag(id_ped, 'cartao', 90)
        sis.upd_st(id_ped, 'enviado')
        sis.upd_st(id_ped, 'entregue')
        pedido = sis.get_ped(id_ped)
        assert pedido['st'] == 'entregue'
        captured = capsys.readouterr()
        # int(90 * 1.5) = 135
        assert 'Cliente corporativo ganhou 135 pontos!' in captured.out

    def test_cancelar_pedido_pendente(self, sis):
        """Cancelar pedido pendente → status 'cancelado'."""
        itens = [{'nome': 'produto1', 'p': 100, 'q': 1, 'tipo': 'normal'}]
        id_ped = sis.add_ped('Joao', itens, 'normal')
        sis.cancelar_pedido(id_ped)
        pedido = sis.get_ped(id_ped)
        assert pedido['st'] == 'cancelado'

    def test_cancelar_pedido_aprovado(self, sis):
        """Cancelar pedido aprovado → status 'cancelado'."""
        itens = [{'nome': 'produto1', 'p': 100, 'q': 1, 'tipo': 'normal'}]
        id_ped = sis.add_ped('Joao', itens, 'normal')
        sis.proc_pag(id_ped, 'cartao', 100)
        sis.cancelar_pedido(id_ped)
        pedido = sis.get_ped(id_ped)
        assert pedido['st'] == 'cancelado'

    def test_cancelar_pedido_enviado(self, sis):
        """Cancelar pedido enviado → status 'cancelado'."""
        itens = [{'nome': 'produto1', 'p': 100, 'q': 1, 'tipo': 'normal'}]
        id_ped = sis.add_ped('Joao', itens, 'normal')
        sis.proc_pag(id_ped, 'cartao', 100)
        sis.upd_st(id_ped, 'enviado')
        sis.cancelar_pedido(id_ped)
        pedido = sis.get_ped(id_ped)
        assert pedido['st'] == 'cancelado'

    def test_validar_estoque_produto_existente_suficiente(self, sis):
        """Estoque suficiente → True."""
        itens = [{'nome': 'produto1', 'q': 10}]
        assert sis.validar_estoque(itens) is True

    def test_validar_estoque_produto_inexistente(self, sis):
        """Produto não existe no catálogo → False."""
        itens = [{'nome': 'produto_inexistente', 'q': 1}]
        assert sis.validar_estoque(itens) is False

    def test_validar_estoque_quantidade_insuficiente(self, sis):
        """Quantidade excede estoque → False."""
        itens = [{'nome': 'produto2', 'q': 999}]
        assert sis.validar_estoque(itens) is False

    def test_validar_estoque_multiplos_itens(self, sis):
        """Múltiplos itens válidos → True."""
        itens = [
            {'nome': 'produto1', 'q': 5},
            {'nome': 'produto2', 'q': 10},
            {'nome': 'produto3', 'q': 20},
        ]
        assert sis.validar_estoque(itens) is True

    def test_upd_st_para_aprovado(self, sis):
        """Atualizar status para aprovado."""
        itens = [{'nome': 'produto1', 'p': 100, 'q': 1, 'tipo': 'normal'}]
        id_ped = sis.add_ped('Joao', itens, 'normal')
        sis.upd_st(id_ped, 'aprovado')
        assert sis.get_ped(id_ped)['st'] == 'aprovado'

    def test_upd_st_para_enviado(self, sis):
        """Atualizar status para enviado."""
        itens = [{'nome': 'produto1', 'p': 100, 'q': 1, 'tipo': 'normal'}]
        id_ped = sis.add_ped('Joao', itens, 'normal')
        sis.upd_st(id_ped, 'enviado')
        assert sis.get_ped(id_ped)['st'] == 'enviado'

    def test_ped_especial_upd_st_pula_estados(self, ped_especial):
        """PedEspecial permite pular direto para qualquer estado."""
        itens = [{'nome': 'produto1', 'p': 100, 'q': 1, 'tipo': 'normal'}]
        id_ped = ped_especial.add_ped('Especial', itens, 'normal')
        ped_especial.upd_st(id_ped, 'entregue')
        assert ped_especial.get_ped(id_ped)['st'] == 'entregue'


# ============================================================
# Task 2.4 — Geração de relatórios
# Requirements: 1.10, 14.5
# ============================================================

class TestReportGeneration:
    """Golden Master: geração de relatórios."""

    def test_relatorio_vendas_cria_arquivo(self, sis):
        """Relatório de vendas cria rel_vendas.txt com conteúdo."""
        itens = [{'nome': 'produto1', 'p': 100, 'q': 2, 'tipo': 'normal'}]
        sis.add_ped('Joao', itens, 'normal')
        sis.gerar_rel('vendas')
        assert os.path.exists('rel_vendas.txt')
        with open('rel_vendas.txt', 'r') as f:
            content = f.read()
        assert len(content) > 0
        assert 'Total de vendas:' in content

    def test_relatorio_clientes_cria_arquivo(self, sis):
        """Relatório de clientes cria rel_clientes.txt com conteúdo."""
        itens = [{'nome': 'produto1', 'p': 100, 'q': 1, 'tipo': 'normal'}]
        sis.add_ped('Joao', itens, 'normal')
        sis.add_ped('Maria', itens, 'vip')
        sis.gerar_rel('clientes')
        assert os.path.exists('rel_clientes.txt')
        with open('rel_clientes.txt', 'r') as f:
            content = f.read()
        assert len(content) > 0
        assert 'Joao' in content
        assert 'Maria' in content

    def test_relatorio_vendas_conteudo_correto(self, sis):
        """Relatório de vendas contém total correto."""
        itens = [{'nome': 'produto1', 'p': 50, 'q': 2, 'tipo': 'normal'}]
        sis.add_ped('Joao', itens, 'normal')
        sis.gerar_rel('vendas')
        with open('rel_vendas.txt', 'r') as f:
            content = f.read()
        # Total = 50*2 = 100.0
        assert '100' in content

    def test_relatorio_clientes_formato(self, sis):
        """Relatório de clientes tem formato CSV: nome,tipo."""
        itens = [{'nome': 'produto1', 'p': 100, 'q': 1, 'tipo': 'normal'}]
        sis.add_ped('Carlos', itens, 'corporativo')
        sis.gerar_rel('clientes')
        with open('rel_clientes.txt', 'r') as f:
            content = f.read()
        assert 'Carlos,corporativo' in content

    def test_calc_tot_cli(self, sis):
        """calc_tot_cli retorna soma dos totais do cliente."""
        itens = [{'nome': 'produto1', 'p': 100, 'q': 1, 'tipo': 'normal'}]
        sis.add_ped('Joao', itens, 'normal')
        sis.add_ped('Joao', itens, 'normal')
        total = sis.calc_tot_cli('Joao')
        assert total == pytest.approx(200.0)

    def test_get_ped_inexistente(self, sis):
        """get_ped com ID inexistente retorna None."""
        assert sis.get_ped(999) is None
