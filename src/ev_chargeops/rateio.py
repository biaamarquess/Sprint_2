import pandas as pd

def calculate_allocation(sessions, price_per_kwh=0.92, common_cost=35.0,
                         idle_tolerance_minutes=20, idle_fee_per_minute=0.10):
    """
    Calcula rateio híbrido:
    energia individual + custos comuns proporcionais ao kWh + penalidade simulada por ociosidade.
    A ociosidade deve representar minutos após o término efetivo da recarga, conforme a fonte dos dados.
    """
    if price_per_kwh < 0 or common_cost < 0 or idle_tolerance_minutes < 0 or idle_fee_per_minute < 0:
        raise ValueError("Os parâmetros financeiros e de tolerância não podem ser negativos.")
    data = sessions.copy()
    if "duracao_min" not in data.columns:
        data["inicio"] = pd.to_datetime(data["inicio"])
        data["fim"] = pd.to_datetime(data["fim"])
        data["duracao_min"] = (data["fim"] - data["inicio"]).dt.total_seconds() / 60
    data["consumo_kwh"] = pd.to_numeric(data["consumo_kwh"], errors="raise")
    data["ociosidade_min"] = pd.to_numeric(data["ociosidade_min"], errors="raise")
    if (data["consumo_kwh"] < 0).any() or (data["ociosidade_min"] < 0).any():
        raise ValueError("Consumo e ociosidade não podem ser negativos.")
    total_kwh = float(data["consumo_kwh"].sum())
    data["custo_energia"] = data["consumo_kwh"] * price_per_kwh
    if total_kwh > 0:
        data["custo_comum"] = data["consumo_kwh"] / total_kwh * common_cost
    else:
        data["custo_comum"] = 0.0
    data["minutos_excedentes"] = (data["ociosidade_min"] - idle_tolerance_minutes).clip(lower=0)
    data["penalidade_ociosidade"] = data["minutos_excedentes"] * idle_fee_per_minute
    data["total_pagar"] = data["custo_energia"] + data["custo_comum"] + data["penalidade_ociosidade"]
    return data
