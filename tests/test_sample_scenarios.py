
import csv
from pathlib import Path

from core.risk_engine import calculate_risk, get_status


def test_sample_scenarios():

    data_file = (
        Path(__file__).parent.parent
        / "sample_data"
        / "sample_scenarios.csv"
    )

    with open(data_file, newline="") as file:

        scenarios = csv.DictReader(file)

        for scenario in scenarios:

            risk = calculate_risk(
                person_count=int(
                    scenario["person_count"]
                ),
                avg_speed=float(
                    scenario["average_speed"]
                ),
                counterflow=(
                    scenario["counterflow"]
                    == "True"
                )
            )

            status = get_status(risk)

            assert status == scenario[
                "expected_status"
            ], (
                f"{scenario['scenario']} "
                f"expected "
                f"{scenario['expected_status']} "
                f"but received {status}"
            )
