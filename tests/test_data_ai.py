from pathlib import Path
import pandas as pd
from ev_chargeops.data import load_sessions, validate_sessions
from ev_chargeops.ai import detect_anomalies, generate_recommendations

ROOT = Path(__file__).resolve().parents[1]

def test_csv_de_exemplo_carrega_e_valida():
    raw = load_sessions(ROOT / "data" / "sessoes_recarga.csv")
    valid, issues = validate_sessions(raw)
    assert len(valid) == 16
    assert valid["consumo_kwh"].sum() > 0
    assert isinstance(issues, list)

def test_validacao_descarta_consumo_negativo():
    raw = pd.DataFrame({
        "sessao_id": ["X"], "usuario": ["ana"], "inicio": ["2026-01-01 08:00"],
        "fim": ["2026-01-01 09:00"], "consumo_kwh": [-2], "ociosidade_min": [0]
    })
    valid, issues = validate_sessions(raw)
    assert valid.empty
    assert issues

def test_ia_retorna_colunas_esperadas():
    raw = load_sessions(ROOT / "data" / "sessoes_recarga.csv")
    valid, _ = validate_sessions(raw)
    result = detect_anomalies(valid)
    assert {"sessao_id", "anomalia", "motivo_anomalia", "metodo_ia"}.issubset(result.columns)
    assert len(result) == len(valid)

def test_recomendacoes_nao_vazias():
    raw = load_sessions(ROOT / "data" / "sessoes_recarga.csv")
    valid, _ = validate_sessions(raw)
    result = detect_anomalies(valid)
    assert len(generate_recommendations(valid, result)) >= 1
