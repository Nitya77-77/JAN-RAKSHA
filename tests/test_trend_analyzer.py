
from core.trend_analyzer import TrendAnalyzer


def test_initial_monitoring():

    analyzer = TrendAnalyzer()

    trend, change, warning = analyzer.analyze(
        zone=0,
        current_risk=20
    )

    assert trend == "MONITORING"
    assert warning is False


def test_rising_risk():

    analyzer = TrendAnalyzer()

    risks = [
        15, 18, 20, 25,
        35, 45, 55, 65
    ]

    result = None

    for risk in risks:
        result = analyzer.analyze(
            zone=0,
            current_risk=risk
        )

    trend, change, warning = result

    assert trend in [
        "RISING",
        "RISING FAST"
    ]

    assert change > 0


def test_early_warning():

    analyzer = TrendAnalyzer()

    risks = [
        10, 15, 20, 25,
        40, 50, 65, 80
    ]

    result = None

    for risk in risks:
        result = analyzer.analyze(
            zone=0,
            current_risk=risk
        )

    trend, change, warning = result

    assert warning is True


def test_falling_risk():

    analyzer = TrendAnalyzer()

    risks = [
        80, 75, 70, 65,
        45, 35, 25, 15
    ]

    result = None

    for risk in risks:
        result = analyzer.analyze(
            zone=0,
            current_risk=risk
        )

    trend, change, warning = result

    assert trend == "FALLING"
    assert change < 0


def test_reset():

    analyzer = TrendAnalyzer()

    for risk in [10, 20, 30, 40]:
        analyzer.analyze(
            zone=0,
            current_risk=risk
        )

    analyzer.reset()

    trend, change, warning = analyzer.analyze(
        zone=0,
        current_risk=50
    )

    assert trend == "MONITORING"
