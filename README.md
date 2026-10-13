# EV ChargeOps — Sprint 02

**Protótipo funcional acadêmico para gestão de recargas compartilhadas de veículos elétricos.**

O EV ChargeOps transforma registros de sessões de recarga em indicadores de consumo, rateio de custos e alertas operacionais. Este protótipo utiliza dados CSV demonstrativos e não possui conexão direta com o carregador GoodWe HCA G2 ou com a plataforma SEMS/Sense Plus.

## Objetivos implementados

- Importação de sessões por CSV e validação dos campos.
- Cálculo de consumo e custo individual por sessão.
- Rateio proporcional dos custos comuns de acordo com o consumo em kWh.
- Penalidade configurável por ociosidade além da tolerância.
- Dashboard com indicadores, consumo por usuário e consumo por dia.
- Detecção de sessões atípicas com IsolationForest, com alternativa robusta para amostras pequenas.
- Recomendações interpretáveis de operação e economia.
- Exportação dos resultados para CSV.
- Testes automatizados para regras centrais.

## Tecnologias

- Python 3.10 ou superior
- Streamlit para a interface
- Pandas e NumPy para tratamento de dados
- Plotly para gráficos
- Scikit-learn para o modelo IsolationForest
- Pytest para testes automatizados

## Estrutura do projeto

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
├── src/ev_chargeops/
│   ├── __init__.py
│   ├── ai.py
│   ├── data.py
│   └── rateio.py
└── tests/
    ├── test_data_ai.py
    └── test_rateio.py
```

## Como executar no Windows

Abra a pasta do projeto no VS Code e execute no terminal PowerShell:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e . -r requirements-dev.txt
streamlit run app.py
```

Se o comando `py -3.12` não existir, use `python -m venv .venv` com uma versão suportada do Python. Se o PowerShell bloquear a ativação, consulte as políticas do seu ambiente ou execute os comandos em um terminal autorizado pela instituição.

O Streamlit normalmente abrirá `http://localhost:8501`.

## Como executar no macOS ou Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e . -r requirements-dev.txt
streamlit run app.py
```

## Como executar os testes

Com o ambiente virtual ativado:

```bash
python -m pytest -v
```

Os testes cobrem o cálculo de energia, rateio de custos comuns, penalidade de ociosidade, validação de dados e retorno do módulo de IA.

## Formato do CSV

Colunas obrigatórias:

| Coluna | Descrição |
|---|---|
| `sessao_id` | Identificador único da sessão |
| `usuario` | Identificador do usuário |
| `inicio` | Data e hora de início |
| `fim` | Data e hora de término da sessão |
| `consumo_kwh` | Energia consumida na sessão |
| `ociosidade_min` | Minutos de ociosidade registrados após a recarga |

Use ponto como separador decimal nos arquivos CSV. Datas e horários devem ser reconhecíveis pelo Pandas.

## Regras de rateio implementadas

1. **Custo de energia:** `consumo_kwh × preço por kWh`.
2. **Custos comuns:** distribuídos proporcionalmente ao consumo total do período.
3. **Ociosidade excedente:** `máximo(ociosidade_min − tolerância, 0) × tarifa_por_minuto`.
4. **Total por sessão:** custo de energia + custo comum alocado + penalidade por ociosidade.

Os valores de preço, custos comuns, tolerância e tarifa de ociosidade são parâmetros demonstrativos configuráveis no painel. Antes de uso real, a equipe gestora deve validar a política de cobrança, as regras legais e a forma de medir a ociosidade.

## Papel da inteligência artificial

O módulo `ai.py` utiliza IsolationForest para sinalizar combinações de consumo, duração e ociosidade que pareçam atípicas quando há dados suficientes. Para conjuntos pequenos ou sem variação, usa limites robustos como alternativa. O sistema também gera recomendações interpretáveis a partir dos horários e dos registros de ociosidade.

A IA é parte do fluxo: os resultados aparecem no painel, são associados às sessões e podem ser exportados. Os alertas não alteram automaticamente o valor cobrado. Toda sinalização deve ser revisada por uma pessoa antes de qualquer decisão financeira.

## Evidências

Consulte `docs/evidencias/DEMO_RESULTADOS.md` e os arquivos CSV de saída. Eles registram resultados reproduzíveis calculados a partir do conjunto demonstrativo. Para a apresentação final, executem o painel localmente e acrescentem capturas de tela reais das abas Visão geral, Sessões e rateio e Inteligência artificial, ou gravem uma demonstração curta em vídeo.

## Decisões e desvios

As decisões técnicas, premissas, limitações e possíveis desvios da Sprint 01 estão descritos em `docs/DECISOES_TECNICAS.md` e `docs/LIMITACOES_E_PROXIMOS_PASSOS.md`. Confirmem com o documento original da Sprint 01 se os parâmetros e o comportamento aqui implementados correspondem exatamente às regras aprovadas pela equipe.

## Segurança, privacidade e limitações

- O CSV de exemplo contém dados fictícios.
- O protótipo não autentica usuários nem aplica controle de acesso.
- Não há integração com hardware nem consulta à API GoodWe.
- Não se deve usar o resultado como cobrança real sem validação de dados e aprovação das regras.
- Evite enviar dados pessoais reais para repositórios públicos.


