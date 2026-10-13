# Limitações e próximos passos

## Limitações atuais
- Dados simulados, sem integração com o carregador GoodWe HCA G2, SEMS ou Sense Plus.
- Sem login, gestão de permissões ou persistência em banco de dados.
- Sem conexão a tarifas horárias reais ou previsão de preço de energia.
- Detecção de anomalias limitada pela quantidade e qualidade da amostra.
- A regra de ociosidade depende da qualidade do dado fornecido no CSV.
- O custo comum é rateado proporcionalmente a kWh; o grupo deve confirmar que essa é a regra aprovada.

## Próximas evoluções
1. Validar o modelo de rateio com os requisitos originais da Sprint 01 e com o responsável pelo espaço de recarga.
2. Substituir os dados de demonstração por uma fonte autorizada e documentada.
3. Adicionar persistência, autenticação e trilha de auditoria.
4. Medir qualidade do modelo de anomalias com histórico real rotulado.
5. Criar testes de integração e pipeline de validação automática.
6. Adicionar exportação de relatório financeiro mensal e mecanismo de aprovação do gestor.
7. Avaliar privacidade, retenção e acesso aos dados antes de disponibilizar o sistema.
