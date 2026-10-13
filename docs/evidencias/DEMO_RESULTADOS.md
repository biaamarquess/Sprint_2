# Evidências de demonstração — EV ChargeOps

Este diretório contém saídas de referência calculadas a partir de `data/sessoes_recarga.csv` usando os parâmetros demonstrativos abaixo:

- Preço da energia: R$ 0,92/kWh
- Custos comuns do período: R$ 35,00
- Tolerância de ociosidade: 20 minutos
- Tarifa por minuto excedente: R$ 0,10

Arquivos:
- `rateio_demo.csv`: sessões com os valores calculados.
- `analise_ia_demo.csv`: sessões com o sinal de anomalia e motivo retornado pelo módulo de IA.

Esses arquivos são evidências de saída do processamento, não capturas de tela do dashboard. Para completar a apresentação, executem `streamlit run app.py` e salvem capturas reais do painel. Recomenda-se capturar:
1. A aba Visão geral com os indicadores e gráficos.
2. A aba Sessões e rateio com a tabela de custos.
3. A aba Inteligência artificial com alertas e recomendações.
4. O terminal mostrando a execução dos testes com sucesso.

Não afirmem que houve integração com hardware real: a demonstração usa dados simulados.


Resumo calculado para referência:
- Sessões válidas: 16
- Usuários distintos: 5
- Consumo total: 349.40 kWh
- Total rateado: R$ 393.85
- Sessões sinalizadas pela IA: 3
