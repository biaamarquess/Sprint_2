# Decisões técnicas — EV ChargeOps Sprint 02

## Objetivo
Implementar uma prova de conceito que transforme sessões de recarga em consumo individual, rateio de custos e sinais operacionais para gestores.

## Arquitetura
- `app.py`: interface Streamlit e fluxo de apresentação dos resultados.
- `data.py`: leitura, normalização e validação dos CSVs.
- `rateio.py`: regras determinísticas de cálculo financeiro.
- `ai.py`: detecção de anomalias e recomendações interpretáveis.
- `tests/`: testes automatizados para funções centrais.

A separação permite testar as regras de negócio sem iniciar a interface e facilita evoluções futuras.

## Modelo de rateio
O protótipo soma três componentes por sessão:
1. Energia consumida multiplicada pelo preço unitário.
2. Parcela proporcional dos custos comuns, ponderada pelo consumo de energia de cada sessão.
3. Penalidade demonstrativa por minutos de ociosidade acima de uma tolerância configurável.

A penalidade foi mantida separada e visível para facilitar auditoria. Ela não é ativada como regra oficial até que o grupo confirme os parâmetros e a definição operacional de ociosidade.

## Papel estrutural da IA
O `IsolationForest` analisa consumo, duração e ociosidade e marca registros fora do padrão. A análise aparece junto à sessão correspondente no dashboard e pode ser exportada. O módulo gera recomendações operacionais relacionadas a horários de início e ociosidade.

A IA não altera automaticamente o rateio, porque anomalia estatística não comprova fraude nem erro. Decisões com impacto financeiro precisam de revisão humana.

## Dados
Para o protótipo, a entrada é um CSV com identificador de sessão, usuário, início, fim, consumo e ociosidade. A validação descarta linhas com dados essenciais ausentes, datas inválidas ou valores negativos e relata duplicidades.

## Desvios e premissas que a equipe deve confirmar
- O protótipo utiliza dados simulados porque não há conexão direta com o carregador nesta implementação.
- Os custos, preço por kWh, tolerância e penalidade são parâmetros de demonstração; devem ser substituídos pelas regras acordadas na Sprint 01, se forem diferentes.
- A recomendação de horários usa a distribuição observada na amostra e não constitui uma previsão avançada de demanda.
- O modelo de anomalias precisa ser recalibrado com dados reais e suficientes antes de uso operacional.

## Reprodutibilidade
A execução é local, com dependências registradas nos arquivos `requirements.txt` e `requirements-dev.txt`. Os testes podem ser executados com `python -m pytest -v`.
