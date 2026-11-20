"""Regra 9: valor a pagar conforme a data do pagamento.

Os casos seguem a tabela de caixa-preta em docs/tabela_caixa_preta_regra9.md.
"""
from datetime import date
from decimal import Decimal

from app.regras import calcular_valor_pagamento

VENCIMENTO = date(2026, 11, 10)   # terça-feira


def test_pagamento_no_vencimento_e_valor_cheio():
    valor = calcular_valor_pagamento(Decimal("1000.00"), VENCIMENTO, VENCIMENTO)

    assert valor == Decimal("1000.00")


def test_pagamento_com_dez_dias_de_antecedencia_tem_cinco_por_cento_de_desconto():
    valor = calcular_valor_pagamento(Decimal("1000.00"), VENCIMENTO, date(2026, 10, 31))

    assert valor == Decimal("950.00")


def test_pagamento_com_nove_dias_de_antecedencia_e_valor_cheio():
    valor = calcular_valor_pagamento(Decimal("1000.00"), VENCIMENTO, date(2026, 11, 1))

    assert valor == Decimal("1000.00")
