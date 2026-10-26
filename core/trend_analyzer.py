
from collections import defaultdict, deque


class TrendAnalyzer:
   
    def __init__(self, history_size=20):
        self.history_size = history_size

        self.risk_history = defaultdict(
            lambda: deque(maxlen=self.history_size)
        )


    def analyze(self, zone, current_risk):
   

        self.risk_history[zone].append(current_risk)

        history = list(self.risk_history[zone])

        if len(history) < 8:
            return "MONITORING", 0.0, False


        midpoint = len(history) // 2

        old_average = (
            sum(history[:midpoint])
            / midpoint
        )

        recent_average = (
            sum(history[midpoint:])
            / (len(history) - midpoint)
        )

        change = recent_average - old_average

        if change >= 15:
            trend = "RISING FAST"

        elif change >= 7:
            trend = "RISING"

        elif change <= -7:
            trend = "FALLING"

        else:
            trend = "STABLE"

        early_warning = (
            trend in ["RISING", "RISING FAST"]
            and current_risk >= 40
        )


        return trend, round(change, 2), early_warning


    def reset(self):
   
        self.risk_history.clear()
