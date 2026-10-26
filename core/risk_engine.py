
def calculate_risk(person_count, avg_speed, counterflow):

    density_ratio = min(person_count / 15, 1.0)
    density_score = density_ratio * 40

    counterflow_score = 35 if counterflow else 0

    if person_count < 2:
        congestion_score = 0

    elif avg_speed < 10:
        congestion_score = 25

    elif avg_speed < 25:
        congestion_score = 18

    elif avg_speed < 40:
        congestion_score = 10

    else:
        congestion_score = 0

    risk = (
        density_score
        + counterflow_score
        + congestion_score
    )

    return min(round(risk), 100)


def get_status(risk):
  

    if risk < 25:
        return "SAFE"

    elif risk < 50:
        return "CAUTION"

    elif risk < 75:
        return "HIGH"

    else:
        return "CRITICAL"
