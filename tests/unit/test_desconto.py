"""Regra 9: valor a pagar conforme a data do pagamento.

Os casos seguem a tabela de caixa-preta em docs/tabela_caixa_preta_regra9.md.
"""
from datetime import date
from decimal import Decimal

from app.regras import calcular_valor_pagamento

VENCIMENTO = date(2026, 11, 10)   # terça-feira
VENCIMENTO_SABADO = date(2026, 11, 14)   # prorrogado para segunda, 16/11 (regra 5)


def test_pagamento_no_vencimento_e_valor_cheio():
    valor = calcular_valor_pagamento(Decimal("1000.00"), VENCIMENTO, VENCIMENTO)

    assert valor == Decimal("1000.00")


def test_pagamento_com_dez_dias_de_antecedencia_tem_cinco_por_cento_de_desconto():
    valor = calcular_valor_pagamento(Decimal("1000.00"), VENCIMENTO, date(2026, 10, 31))

    assert valor == Decimal("950.00")


def test_pagamento_com_nove_dias_de_antecedencia_e_valor_cheio():
    valor = calcular_valor_pagamento(Decimal("1000.00"), VENCIMENTO, date(2026, 11, 1))

    assert valor == Decimal("1000.00")


def test_pagamento_um_dia_depois_do_vencimento_tem_encargos():
    valor = calcular_valor_pagamento(Decimal("1000.00"), VENCIMENTO, date(2026, 11, 11))

    assert valor == Decimal("1020.33")


def test_pagamento_trinta_dias_depois_do_vencimento_tem_encargos():
    valor = calcular_valor_pagamento(Decimal("1000.00"), VENCIMENTO, date(2026, 12, 10))

    assert valor == Decimal("1029.90")


def test_vencimento_no_sabado_pago_na_segunda_e_valor_cheio():
    valor = calcular_valor_pagamento(Decimal("1000.00"), VENCIMENTO_SABADO, date(2026, 11, 16))

    assert valor == Decimal("1000.00")


def test_vencimento_no_sabado_pago_na_terca_tem_um_dia_de_encargos():
    valor = calcular_valor_pagamento(Decimal("1000.00"), VENCIMENTO_SABADO, date(2026, 11, 17))

    assert valor == Decimal("1020.33")


def test_antecedencia_conta_sobre_o_vencimento_original_dez_dias_antes_do_sabado():
    valor = calcular_valor_pagamento(Decimal("1000.00"), VENCIMENTO_SABADO, date(2026, 11, 4))

    assert valor == Decimal("950.00")


def test_antecedencia_conta_sobre_o_vencimento_original_nove_dias_antes_do_sabado():
    # são 11 dias antes da segunda prorrogada, mas só 9 antes do vencimento original
    valor = calcular_valor_pagamento(Decimal("1000.00"), VENCIMENTO_SABADO, date(2026, 11, 5))

    assert valor == Decimal("1000.00")


def test_desconto_com_meio_centavo_e_arredondado_para_cima():
    # 5% de 100,10 = 5,005, que arredonda para 5,01
    valor = calcular_valor_pagamento(Decimal("100.10"), VENCIMENTO, date(2026, 10, 31))

    assert valor == Decimal("95.09")


def test_vencimento_no_sabado_pago_no_domingo_e_valor_cheio():
    # depois do vencimento original, mas antes da segunda prorrogada: ainda sem encargos
    valor = calcular_valor_pagamento(Decimal("1000.00"), VENCIMENTO_SABADO, date(2026, 11, 15))

    assert valor == Decimal("1000.00")
