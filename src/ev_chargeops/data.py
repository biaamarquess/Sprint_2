from pathlib import Path
import pandas as pd

REQUIRED_COLUMNS = ["sessao_id", "usuario", "inicio", "fim", "consumo_kwh", "ociosidade_min"]

def load_sessions(path):
    """Carrega sessões a partir de um CSV."""
    return pd.read_csv(Path(path))

def validate_sessions(df):
    """Valida e normaliza os campos essenciais; devolve (dados_validos, avisos)."""
    data = df.copy()
    issues = []
    missing = [c for c in REQUIRED_COLUMNS if c not in data.columns]
    if missing:
        return pd.DataFrame(columns=REQUIRED_COLUMNS), [f"Colunas obrigatórias ausentes: {', '.join(missing)}"]
    data["sessao_id"] = data["sessao_id"].astype(str)
    data["usuario"] = data["usuario"].astype(str).str.strip()
    data["inicio"] = pd.to_datetime(data["inicio"], errors="coerce")
    data["fim"] = pd.to_datetime(data["fim"], errors="coerce")
    for col in ["consumo_kwh", "ociosidade_min"]:
        data[col] = pd.to_numeric(data[col], errors="coerce")
    invalid = (
        data["usuario"].eq("") |
        data["inicio"].isna() |
        data["fim"].isna() |
        data["consumo_kwh"].isna() |
        data["ociosidade_min"].isna() |
        data["consumo_kwh"].lt(0) |
        data["ociosidade_min"].lt(0) |
        data["fim"].lt(data["inicio"])
    )
    if invalid.any():
        issues.append(f"{int(invalid.sum())} linha(s) inválida(s) foram descartadas.")
        data = data.loc[~invalid].copy()
    if data["sessao_id"].duplicated().any():
        duplicated = int(data["sessao_id"].duplicated(keep=False).sum())
        issues.append(f"Foram encontrados {duplicated} registros com identificador de sessão duplicado; foi mantida a primeira ocorrência.")
        data = data.drop_duplicates("sessao_id", keep="first")
    data["duracao_min"] = ((data["fim"] - data["inicio"]).dt.total_seconds() / 60).round(2)
    data = data.loc[data["duracao_min"] >= 0].reset_index(drop=True)
    return data, issues
