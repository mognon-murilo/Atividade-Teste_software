# Regra 9: tabela de caixa-preta

Montada só com o enunciado da regra 9 e as regras 4 e 5 de `docs/regras_de_negocio.md`,
sem abrir o código.

**Título de referência:** 1.000,00 com vencimento em **10/11/2026 (terça-feira)**.
Para os casos de fim de semana: vencimento em **14/11/2026 (sábado)**, prorrogado para
**16/11/2026 (segunda-feira)**.

**Antecedência** = vencimento **original** − data do pagamento, em dias.
**Encargos (regra 4)** = multa de 2% + juros de 0,033% ao dia de atraso, arredondados para duas
casas (meio centavo para cima): 1 dia de atraso → 20,33; 30 dias de atraso → 29,90.

| # | Classe de equivalência (data do pagamento) | Valor representativo | Valores limite | Resultado esperado |
|---|---|---|---|---|
| C1 | Antecedência de **10 dias ou mais** (pagamento até 31/10/2026): 5% de desconto | 01/10/2026 (40 dias antes) → **950,00** | 31/10/2026 (10 dias antes) → 950,00<br>01/11/2026 (9 dias antes, já na C2) → 1.000,00 | 1.000,00 − 50,00 = **950,00** |
| C2 | De **9 dias antes até o vencimento**, inclusive (01/11 a 10/11/2026): valor cheio | 05/11/2026 (5 dias antes) → **1.000,00** | 01/11/2026 (9 dias antes) → 1.000,00<br>10/11/2026 (no vencimento) → 1.000,00<br>31/10/2026 (vizinho na C1) → 950,00<br>11/11/2026 (vizinho na C3) → 1.020,33 | **1.000,00** |
| C3 | **Depois do vencimento**: valor + encargos da regra 4 | 10/12/2026 (30 dias de atraso) → **1.029,90** | 11/11/2026 (1 dia de atraso) → 1.020,33<br>10/11/2026 (vizinho na C2) → 1.000,00 | 1.000,00 + encargos |
| C4 | Vencimento no **fim de semana**, pagamento depois da data original e até a segunda-feira (regra 5): sem encargos | venc. 14/11 (sáb.), pago em 15/11 (dom.) → **1.000,00** | 16/11/2026 (segunda, data prorrogada) → 1.000,00<br>17/11/2026 (vizinho na C5) → 1.020,33 | **1.000,00** |
| C5 | Vencimento no **fim de semana**, pagamento depois da segunda-feira: atraso contado a partir da data prorrogada | venc. 14/11 (sáb.), pago em 17/11 (ter.) → **1.020,33** (1 dia de atraso, não 3) | 17/11/2026 (1 dia após a segunda) → 1.020,33<br>16/11/2026 (vizinho na C4) → 1.000,00 | 1.000,00 + encargos de 1 dia = **1.020,33** |
| C6 | Vencimento no **fim de semana**, antecedência contada sobre a **data original** (sábado), não sobre a prorrogada | venc. 14/11 (sáb.), pago em 04/11 (10 dias antes do sábado) → **950,00** | 04/11/2026 (10 dias antes do sábado) → 950,00<br>05/11/2026 (9 dias antes do sábado e 11 antes da segunda) → **1.000,00** | 950,00 em 04/11; 1.000,00 em 05/11 |
| C7 | Desconto que termina em **meio centavo**: arredonda para cima | título de **100,10** com vencimento em 10/11, pago em 31/10: desconto 5,005 → **5,01** | 5,005 → 5,01 (o arredondamento bancário daria 5,00 e o resultado 95,10) | 100,10 − 5,01 = **95,09** |

Observação: com 1.000,00 o desconto é exato (50,00), por isso a classe C7 usa outro valor.

## Fila de testes (TDD)

Cada linha da tabela vira um teste em `tests/unit/test_desconto.py`, nesta ordem:

1. C2, no vencimento (10/11) → 1.000,00
2. C1, 10 dias antes (31/10) → 950,00
3. C2, 9 dias antes (01/11) → 1.000,00
4. C3, 1 dia depois (11/11) → 1.020,33
5. C3, 30 dias depois (10/12) → 1.029,90
6. C4, vencimento no sábado e pagamento na segunda (16/11) → 1.000,00
7. C5, vencimento no sábado e pagamento na terça (17/11) → 1.020,33
8. C6, vencimento no sábado e pagamento 10 dias antes do sábado (04/11) → 950,00
9. C6, vencimento no sábado e pagamento 9 dias antes do sábado (05/11) → 1.000,00
10. C7, desconto com meio centavo (100,10 em 31/10) → 95,09
