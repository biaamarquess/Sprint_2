import pandas as pd
import pytest
from ev_chargeops.rateio import calculate_allocation

def sample():
    return pd.DataFrame({
        "sessao_id": ["A", "B"],
        "usuario": ["ana", "bruno"],
        "inicio": pd.to_datetime(["2026-01-01 08:00", "2026-01-01 09:00"]),
        "fim": pd.to_datetime(["2026-01-01 09:00", "2026-01-01 10:00"]),
        "consumo_kwh": [10.0, 30.0],
        "ociosidade_min": [10, 40],
        "duracao_min": [60.0, 60.0],
    })

def test_rateio_energia_e_custo_comum():
    result = calculate_allocation(sample(), price_per_kwh=1.0, common_cost=40.0, idle_tolerance_minutes=20, idle_fee_per_minute=0.5)
    assert result.loc[0, "custo_energia"] == pytest.approx(10)
    assert result.loc[1, "custo_energia"] == pytest.approx(30)
    assert result.loc[0, "custo_comum"] == pytest.approx(10)
    assert result.loc[1, "custo_comum"] == pytest.approx(30)

def test_penalidade_apenas_acima_da_tolerancia():
    result = calculate_allocation(sample(), idle_tolerance_minutes=20, idle_fee_per_minute=0.5)
    assert result.loc[0, "penalidade_ociosidade"] == pytest.approx(0)
    assert result.loc[1, "penalidade_ociosidade"] == pytest.approx(10)

def test_parametros_negativos_sao_rejeitados():
    with pytest.raises(ValueError):
        calculate_allocation(sample(), price_per_kwh=-1)

def test_soma_do_custo_comum_preserva_total():
    result = calculate_allocation(sample(), common_cost=52.0)
    assert result["custo_comum"].sum() == pytest.approx(52.0)
