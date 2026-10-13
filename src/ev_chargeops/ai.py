import numpy as np
import pandas as pd

FEATURES = ["consumo_kwh", "duracao_min", "ociosidade_min"]

def detect_anomalies(sessions, contamination=0.15):
    """
    Detecta padrões incomuns com IsolationForest quando há pelo menos 8 linhas e variação.
    Para amostras menores, usa limites robustos por mediana/MAD. É apoio à revisão humana.
    """
    data = sessions.copy()
    if "duracao_min" not in data.columns:
        data["inicio"] = pd.to_datetime(data["inicio"])
        data["fim"] = pd.to_datetime(data["fim"])
        data["duracao_min"] = (data["fim"] - data["inicio"]).dt.total_seconds() / 60
    for col in FEATURES:
        data[col] = pd.to_numeric(data[col], errors="coerce").fillna(0)
    reasons = []
    flags = np.zeros(len(data), dtype=bool)
    method = "limites robustos"
    if len(data) >= 8 and data[FEATURES].nunique().sum() > len(FEATURES):
        try:
            from sklearn.ensemble import IsolationForest
            model = IsolationForest(contamination=contamination, random_state=42)
            pred = model.fit_predict(data[FEATURES])
            flags = pred == -1
            method = "IsolationForest"
        except Exception:
            pass
    if method == "limites robustos":
        for feature in FEATURES:
            values = data[feature].to_numpy(dtype=float)
            median = float(np.median(values)) if len(values) else 0
            mad = float(np.median(np.abs(values - median))) if len(values) else 0
            threshold = max(3.5 * 1.4826 * mad, abs(median) * 1.5, 1.0)
            flags |= np.abs(values - median) > threshold
    for idx, row in data.iterrows():
        row_reasons = []
        if row["consumo_kwh"] > 50:
            row_reasons.append("consumo acima de 50 kWh")
        if row["ociosidade_min"] > 120:
            row_reasons.append("ociosidade superior a 120 minutos")
        if flags[data.index.get_loc(idx)] and not row_reasons:
            row_reasons.append("combinação de consumo, duração ou ociosidade fora do padrão")
        reasons.append("; ".join(row_reasons) if row_reasons else ("padrão incomum (" + method + ")" if flags[data.index.get_loc(idx)] else "sem sinal relevante"))
    return pd.DataFrame({
        "sessao_id": data["sessao_id"].astype(str).values if "sessao_id" in data else data.index.astype(str),
        "anomalia": flags,
        "motivo_anomalia": reasons,
        "metodo_ia": method,
    })

def generate_recommendations(sessions, ai_results=None):
    """Gera recomendações interpretáveis a partir dos dados analisados."""
    data = sessions.copy()
    if data.empty:
        return ["Importe sessões válidas para receber recomendações."]
    if "inicio" in data:
        start = pd.to_datetime(data["inicio"], errors="coerce")
        hours = start.dt.hour.dropna()
        if not hours.empty:
            peak_hour = int(hours.value_counts().idxmax())
            recommendations = [f"O horário com mais inícios de recarga nesta amostra é por volta de {peak_hour:02d}h. Avalie incentivos para horários alternativos."]
        else:
            recommendations = []
    else:
        recommendations = []
    if "ociosidade_min" in data:
        idle = pd.to_numeric(data["ociosidade_min"], errors="coerce").fillna(0)
        if (idle > 20).any():
            recommendations.append(f"{int((idle > 20).sum())} sessão(ões) tiveram mais de 20 minutos de ociosidade registrada. Avalie notificações ao usuário e confirme a regra de tolerância.")
        else:
            recommendations.append("A amostra não mostra ociosidade acima de 20 minutos; mantenha o monitoramento.")
    if ai_results is not None and "anomalia" in ai_results and ai_results["anomalia"].any():
        recommendations.append(f"{int(ai_results['anomalia'].sum())} sessão(ões) foram sinalizadas para revisão humana. Confira os dados de origem antes de aplicar qualquer cobrança.")
    recommendations.append("Compare o consumo por usuário ao longo de períodos maiores antes de alterar tarifas ou regras de rateio.")
    return recommendations
