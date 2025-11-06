import math

from src.preprocess.preprocess_text import clean_description
from src.models.classify_family import predict_family
from src.models.search_material import search_material


def test_clean_description_basic():
    raw = "Valvula de Globo Acero 2 Pulgadas Clase 600!!!"
    cleaned = clean_description(raw)
    assert "valvula" in cleaned
    assert "globo" in cleaned
    assert "acero" in cleaned
    assert "2" in cleaned
    assert "pulg" in cleaned  # normaliza 'pulgadas' -> 'pulg'
    assert "clase 600" in cleaned
    assert "!" not in cleaned


def test_predict_family_valvula():
    text = "VALVULA GLOBO ACERO 2 PULG CLASE 600"
    fam = predict_family(text)
    assert fam == "valvula"


def test_search_material_returns_best_match():
    text = "VALVULA GLOBO ACERO 2 PULG CLASE 600"
    code, desc, score = search_material(text)
    assert isinstance(code, str) and isinstance(desc, str) and isinstance(score, float)
    assert code == "VAL-GLB-AC-2-CL600"
    assert math.isfinite(score) and 0.0 <= score <= 1.0
    assert len(desc) > 0
