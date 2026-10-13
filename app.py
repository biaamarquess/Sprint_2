from pathlib import Path
import sys
import pandas as pd
import streamlit as st
import plotly.express as px

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))

from ev_chargeops.data import load_sessions, validate_sessions
from ev_chargeops.rateio import calculate_allocation
from ev_chargeops.ai import detect_anomalies, generate_recommendations

st.set_page_config(page_title="EV ChargeOps", page_icon="⚡", layout="wide")
st.title("⚡ EV ChargeOps")
st.caption("Gestão inteligente de recargas compartilhadas • Protótipo acadêmico FIAP + GoodWe")

with st.sidebar:
    st.header("Configuração")
    uploaded = st.file_uploader("Importar sessões (CSV)", type=["csv"])
    price_kwh = st.number_input("Preço da energia (R$/kWh)", min_value=0.0, value=0.92, step=0.05, format="%.2f")
    common_cost = st.number_input("Custos comuns do período (R$)", min_value=0.0, value=35.0, step=5.0, format="%.2f")
    idle_tolerance = st.number_input("Tolerância de ociosidade após recarga (min)", min_value=0, value=20, step=5)
    idle_fee = st.number_input("Penalidade por minuto excedente (R$)", min_value=0.0, value=0.10, step=0.05, format="%.2f")
    st.caption("Valores editáveis para simulação. Ajuste-os às regras aprovadas pelo grupo.")

default_path = ROOT / "data" / "sessoes_recarga.csv"
try:
    if uploaded:
        sessions = pd.read_csv(uploaded)
    else:
        sessions = load_sessions(default_path)
except Exception as exc:
    st.error(f"Não foi possível ler os dados: {exc}")
    st.stop()

sessions, issues = validate_sessions(sessions)
if issues:
    st.warning("Foram encontrados problemas nos dados. Revise o CSV antes de usar os resultados.")
    for issue in issues:
        st.write(f"- {issue}")
if sessions.empty:
    st.error("Nenhuma sessão válida foi encontrada.")
    st.stop()

allocated = calculate_allocation(
    sessions,
    price_per_kwh=price_kwh,
    common_cost=common_cost,
    idle_tolerance_minutes=idle_tolerance,
    idle_fee_per_minute=idle_fee,
)
ai_results = detect_anomalies(sessions)
recommendations = generate_recommendations(sessions, ai_results)

total_kwh = float(allocated["consumo_kwh"].sum())
total_cost = float(allocated["total_pagar"].sum())
n_users = int(allocated["usuario"].nunique())
n_sessions = len(allocated)
anomaly_count = int(ai_results["anomalia"].sum()) if "anomalia" in ai_results else 0

c1, c2, c3, c4 = st.columns(4)
c1.metric("Energia consumida", f"{total_kwh:,.1f} kWh".replace(",", "X").replace(".", ",").replace("X", "."))
c2.metric("Custo total rateado", f"R$ {total_cost:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
c3.metric("Usuários", n_users)
c4.metric("Sessões atípicas", anomaly_count)

tab1, tab2, tab3, tab4 = st.tabs(["Visão geral", "Sessões e rateio", "Inteligência artificial", "Dados e exportação"])

with tab1:
    left, right = st.columns(2)
    with left:
        by_user = allocated.groupby("usuario", as_index=False)["consumo_kwh"].sum().sort_values("consumo_kwh", ascending=False)
        st.subheader("Consumo por usuário")
        st.plotly_chart(px.bar(by_user, x="usuario", y="consumo_kwh", labels={"usuario":"Usuário","consumo_kwh":"Consumo (kWh)"}), use_container_width=True)
    with right:
        by_day = allocated.copy()
        by_day["data"] = pd.to_datetime(by_day["inicio"]).dt.date
        by_day = by_day.groupby("data", as_index=False)["consumo_kwh"].sum()
        st.subheader("Consumo por dia")
        st.plotly_chart(px.line(by_day, x="data", y="consumo_kwh", markers=True, labels={"data":"Data","consumo_kwh":"Consumo (kWh)"}), use_container_width=True)
    st.subheader("Como o rateio é calculado")
    st.markdown(
        "- **Energia:** consumo individual (kWh) × preço configurado por kWh.\n"
        "- **Custos comuns:** distribuídos proporcionalmente ao consumo de energia de cada usuário.\n"
        "- **Ociosidade:** penalidade simulada quando o tempo conectado após o fim da recarga supera a tolerância.\n"
        "- **Total individual:** energia + parcela dos custos comuns + penalidade."
    )

with tab2:
    st.subheader("Sessões calculadas")
    display_cols = ["sessao_id", "usuario", "inicio", "fim", "consumo_kwh", "duracao_min", "ociosidade_min", "custo_energia", "custo_comum", "penalidade_ociosidade", "total_pagar"]
    st.dataframe(allocated[display_cols].round(2), use_container_width=True, hide_index=True)
    st.download_button("Baixar rateio em CSV", allocated.to_csv(index=False).encode("utf-8-sig"), "rateio_ev_chargeops.csv", "text/csv")

with tab3:
    st.subheader("Detecção de sessões atípicas")
    st.write("O módulo utiliza IsolationForest quando há dados suficientes e uma análise estatística de fallback para conjuntos pequenos. Os alertas são sinais para revisão humana, não uma acusação de uso indevido.")
    ai_table = allocated.merge(ai_results[["sessao_id", "anomalia", "motivo_anomalia"]], on="sessao_id", how="left")
    st.dataframe(ai_table[["sessao_id", "usuario", "consumo_kwh", "duracao_min", "ociosidade_min", "anomalia", "motivo_anomalia"]], use_container_width=True, hide_index=True)
    st.subheader("Recomendações")
    for rec in recommendations:
        st.info(rec)
    st.download_button("Baixar análise de IA em CSV", ai_table.to_csv(index=False).encode("utf-8-sig"), "analise_ia_ev_chargeops.csv", "text/csv")

with tab4:
    st.subheader("Dados carregados")
    st.write(f"{len(sessions)} sessões válidas carregadas.")
    st.dataframe(sessions, use_container_width=True, hide_index=True)
    st.download_button("Baixar dados válidos em CSV", sessions.to_csv(index=False).encode("utf-8-sig"), "sessoes_validas.csv", "text/csv")
    st.caption("O protótipo usa dados de demonstração e não se conecta diretamente ao carregador GoodWe ou à plataforma SEMS.")

st.divider()
st.caption("EV ChargeOps • Protótipo acadêmico. Os valores são demonstrativos e devem ser validados antes de qualquer uso financeiro real.")
