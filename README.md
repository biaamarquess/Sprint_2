# Enterprise Challenge 2026 — GoodWe + FIAP
## Sprint 02 — Desenvolvimento e prototipação

O **EV ChargeOps** é um protótipo acadêmico para apoiar a gestão de recargas compartilhadas de veículos elétricos. A proposta é transformar registros de sessões de recarga em informações organizadas sobre consumo, distribuição de custos, possíveis anomalias e oportunidades de melhoria operacional.

Esta Sprint 02 evolui a proposta conceitual da Sprint 01 para um **MVP local e demonstrável**, com painel interativo em Streamlit, importação de arquivos CSV, motor de rateio, análise consultiva de anomalias e exportação de resultados.

> **Importante:** o projeto utiliza dados simulados. Não possui integração direta com o carregador GoodWe, com a plataforma SEMS/Sense Plus ou com sistemas de cobrança reais.

**Equipe**

<table>
  <thead>
    <tr>
      <th>Integrante</th>
      <th>RM</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Danilo Gustavo da Silva Fernandes</td>
      <td>RM570057</td>
    </tr>
    <tr>
      <td>Renan Mano Otero</td>
      <td>RM573615</td>
    </tr>
    <tr>
      <td>Beatriz Marques Souza</td>
      <td>RM571819</td>
    </tr>
    <tr>
      <td colspan="2" align="center"><strong>E-mail da equipe:</strong> rm570057@fiap.com.br</td>
    </tr>
  </tbody>
</table>

---

## Resumo da solução

O EV ChargeOps foi pensado para condomínios, empresas e campus universitários que compartilham pontos de recarga. Quando várias pessoas usam o mesmo carregador, é importante entender quem consumiu energia, como os custos foram distribuídos e quais registros precisam ser revisados.

A solução reúne, em um único painel:

- importação e validação de sessões de recarga;
- cálculo do custo energético por sessão;
- distribuição proporcional de custos comuns;
- simulação de cobrança por ociosidade excedente;
- identificação de registros potencialmente atípicos;
- recomendações operacionais baseadas nos dados disponíveis;
- visualização de indicadores, gráficos e tabelas;
- exportação de resultados para análise posterior.

## Problema

A recarga compartilhada envolve questões técnicas e administrativas: identificar o consumo, aplicar regras transparentes de rateio, tratar registros inconsistentes e evitar que situações atípicas resultem em cobranças indevidas.

Sem dados organizados e critérios claros, a gestão pode gerar divergências entre usuários, dificuldade de conferência e desperdício de energia. O EV ChargeOps propõe uma camada de organização e apoio à decisão para tornar esse processo mais compreensível.

## Objetivo do MVP

Demonstrar um fluxo funcional que receba dados de sessões, valide as informações disponíveis, calcule custos de acordo com parâmetros configuráveis e apresente alertas para revisão humana.

O protótipo não substitui uma solução de produção: autenticação, persistência em banco de dados, integração com hardware, conexão com APIs externas e cobrança real permanecem fora do escopo atual.

## Fluxo de funcionamento

```text
Arquivo CSV
    ↓
Importação e validação dos dados
    ↓
Cálculo do consumo e dos custos
    ↓
Rateio dos custos comuns
    ↓
Análise de possíveis anomalias
    ↓
Dashboard, recomendações e exportação
```

As regras determinísticas do sistema calculam os valores. A análise de IA é consultiva: sinaliza registros que merecem atenção, mas não decide automaticamente se uma sessão deve ser cobrada.

---

## Funcionalidades implementadas

### 1. Importação de dados

O painel permite importar um arquivo CSV de sessões de recarga. Os dados são lidos e validados antes dos cálculos. O repositório inclui um conjunto demonstrativo em `data/sessoes_recarga.csv`.

### 2. Cálculo e rateio de custos

O sistema calcula o custo variável de cada sessão usando o consumo em kWh e o preço configurado por kWh. Os custos comuns do período são distribuídos proporcionalmente ao consumo válido. Também existe um parâmetro de tolerância e uma tarifa para simular penalidade por ociosidade excedente quando esse dado estiver disponível.

### 3. Dashboard

O painel interativo apresenta indicadores e gráficos para facilitar a leitura dos dados importados, do consumo e dos custos calculados.

### 4. Análise de anomalias com IA

O módulo `src/ev_chargeops/ai.py` utiliza `IsolationForest` para auxiliar na identificação de combinações de dados potencialmente atípicas. Para amostras pequenas, o módulo conta com tratamento alternativo para evitar depender exclusivamente do modelo estatístico.

Os alertas devem ser interpretados como sinais para investigação. Uma anomalia não comprova fraude, erro ou responsabilidade de um usuário.

### 5. Recomendações e exportação

O protótipo gera recomendações a partir dos dados disponíveis e permite exportar resultados para arquivos CSV, facilitando a conferência e o uso das informações em documentação e apresentação.

---

## Regras de rateio

Os parâmetros do painel são editáveis para fins de simulação.

| Componente | Regra aplicada |
|---|---|
| Custo de energia | Consumo da sessão em kWh × preço configurado por kWh |
| Custo comum | Distribuição proporcional ao consumo válido de cada sessão |
| Ociosidade excedente | Minutos acima da tolerância × tarifa configurada por minuto |
| Total da sessão | Custo energético + parcela de custo comum + penalidade aplicável |

As regras devem ser confirmadas e aprovadas pela equipe antes de qualquer uso em cenário real. O conjunto de dados demonstrativo não representa usuários, unidades ou consumo reais.

## Papel da inteligência artificial

A IA auxilia a priorizar registros que podem precisar de revisão, com base nos atributos disponíveis. Ela não substitui a validação dos dados nem as regras de cálculo do rateio.

**Princípios adotados:**

- os valores são calculados por regras explícitas;
- os alertas de IA são consultivos;
- uma sinalização não determina, por si só, uma cobrança;
- decisões financeiras exigem conferência humana;
- a qualidade das análises depende da quantidade e da qualidade dos dados fornecidos.

Previsão temporal de consumo, agrupamento de perfis de usuários e integração com dados reais de geração solar são possibilidades futuras, mas não devem ser considerados recursos validados nesta versão.

---

## Tecnologias utilizadas

| Tecnologia | Aplicação |
|---|---|
| Python | Lógica e processamento do projeto |
| Streamlit | Interface web interativa |
| Pandas / NumPy | Tratamento e análise dos dados |
| Plotly | Visualização gráfica |
| Scikit-learn | Detecção consultiva de anomalias com `IsolationForest` |
| Pytest | Testes automatizados |

## Arquitetura do projeto

A aplicação é iniciada por `app.py`. As principais regras foram separadas em módulos dentro do pacote `ev_chargeops`, localizado em `src/`.

- `app.py`: interface Streamlit, parâmetros, indicadores e visualizações.
- `src/ev_chargeops/data.py`: leitura e validação de dados CSV.
- `src/ev_chargeops/rateio.py`: cálculos de consumo e rateio.
- `src/ev_chargeops/ai.py`: identificação consultiva de anomalias e recomendações.
- `data/sessoes_recarga.csv`: conjunto demonstrativo.
- `tests/`: testes automatizados.
- `docs/`: decisões técnicas, limitações e evidências de demonstração.

## Estrutura do repositório

```text
EV-ChargeOps-Sprint02/
├── app.py
├── data/
│   └── sessoes_recarga.csv
├── docs/
│   ├── DECISOES_TECNICAS.md
│   ├── LIMITACOES_E_PROXIMOS_PASSOS.md
│   └── evidencias/
│       ├── DEMO_RESULTADOS.md
│       ├── rateio_demo.csv
│       └── analise_ia_demo.csv
├── entrega-sprint-02.txt
├── pyproject.toml
├── requirements.txt
├── requirements-dev.txt
├── src/
│   └── ev_chargeops/
│       ├── __init__.py
│       ├── ai.py
│       ├── data.py
│       └── rateio.py
└── tests/
    ├── test_data_ai.py
    └── test_rateio.py
```

---

## Como executar localmente

### Pré-requisitos

- Git (caso vá clonar o repositório);
- Python instalado;
- VS Code ou outro editor de código.

### Windows — PowerShell

Na raiz da pasta do projeto, execute os comandos um de cada vez:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e . -r requirements-dev.txt
streamlit run app.py
```

Se o comando `py` não estiver disponível, tente `python -m venv .venv`. Se o PowerShell bloquear a ativação do ambiente virtual, é possível executar os comandos em outro terminal Python autorizado no computador.

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e . -r requirements-dev.txt
streamlit run app.py
```

O Streamlit exibirá o endereço local no terminal, normalmente `http://localhost:8501`. Mantenha o terminal aberto enquanto estiver usando o painel.

### Como carregar o CSV de exemplo

1. Abra o dashboard no navegador.
2. Na barra lateral, localize **Importar sessões (CSV)**.
3. Clique em **Upload**.
4. Selecione `data/sessoes_recarga.csv` na pasta do projeto.
5. Confira os indicadores, as tabelas e os resultados exibidos.

## Testes automatizados

Com o ambiente virtual ativado, execute:

```bash
python -m pytest -v
```

Os testes do projeto verificam regras de rateio e aspectos da validação de dados e análise de IA. Registre no relatório da equipe os resultados observados ao executar os testes no ambiente utilizado para a entrega.

---

## Limitações e próximos passos

Esta versão é um protótipo acadêmico. As principais limitações são:

- não há integração direta com o carregador GoodWe ou com a API SEMS/Sense Plus;
- não há autenticação, perfis de acesso ou banco de dados persistente;
- os dados incluídos são simulados e não representam uma instalação real;
- o sistema não realiza cobrança ou pagamento;
- os parâmetros de custo precisam ser validados pela equipe;
- alertas de IA exigem interpretação humana;
- recomendações energéticas dependem da disponibilidade e da qualidade dos dados.

Como evolução, o projeto pode receber persistência de dados, trilha de auditoria, autenticação, integração com relatórios reais autorizados, regras de conciliação de sessões e validação técnica das recomendações de eficiência energética.

## Decisões técnicas

As decisões, premissas e limitações da implementação estão registradas em:

- `docs/DECISOES_TECNICAS.md`
- `docs/LIMITACOES_E_PROXIMOS_PASSOS.md`
- `docs/evidencias/DEMO_RESULTADOS.md`

Esses documentos devem ser consultados junto com o código para explicar o que foi implementado e o que ficou como trabalho futuro.

## Evidências da demonstração

A pasta `docs/evidencias/` reúne resultados de demonstração e arquivos de saída. Para a apresentação, recomenda-se incluir capturas de tela reais do dashboard em execução, mostrando:

1. a visão geral após a importação do CSV;
2. a tabela ou visualização de rateio;
3. a área de alertas/análise de IA;
4. a exportação dos resultados.

As evidências finais devem corresponder à versão publicada no GitHub.

## Relação com a Sprint 01

A Sprint 01 definiu o contexto do problema, a proposta de governança energética, as regras conceituais de rateio e o papel da IA. A Sprint 02 materializa parte dessa proposta em um MVP local, priorizando importação CSV, cálculos, visualização e alertas consultivos.

Nem todas as integrações e análises previstas conceitualmente estão implementadas. A conexão com hardware e APIs, a persistência e as funcionalidades avançadas de previsão permanecem como evolução futura.

