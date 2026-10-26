
from core.risk_engine import calculate_risk, get_status


def test_safe_crowd():

    risk = calculate_risk(
        person_count=3,
        avg_speed=60,
        counterflow=False
    )

    assert risk < 25
    assert get_status(risk) == "SAFE"


def test_high_risk_crowd():

    risk = calculate_risk(
        person_count=12,
        avg_speed=15,
        counterflow=False
    )

    assert risk >= 50
    assert get_status(risk) == "HIGH"


def test_critical_counterflow():

    risk = calculate_risk(
        person_count=14,
        avg_speed=8,
        counterflow=True
    )

    assert risk >= 75
    assert get_status(risk) == "CRITICAL"


def test_risk_never_exceeds_100():

    risk = calculate_risk(
        person_count=100,
        avg_speed=0,
        counterflow=True
    )

    assert risk <= 100
