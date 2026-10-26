
import cv2
import math
from collections import defaultdict, deque, Counter
from ultralytics import YOLO

from core.risk_engine import calculate_risk, get_status
from core.trend_analyzer import TrendAnalyzer


class CrowdAnalyzer:

    def __init__(
        self,
        model_path="yolo11n.pt",
        confidence=0.35,
        number_of_zones=3
    ):
        self.model = YOLO(model_path)
        self.confidence = confidence
        self.number_of_zones = number_of_zones

        self.track_history = defaultdict(
            lambda: deque(maxlen=10)
        )

        self.trend_analyzer = TrendAnalyzer()


    def reset(self):

        self.track_history.clear()
        self.trend_analyzer.reset()


    def analyze_video(
        self,
        video_path,
        output_path="janraksha_output.mp4"
    ):

        self.reset()

        cap = cv2.VideoCapture(video_path)

        if not cap.isOpened():
            raise ValueError(
                f"Could not open video: {video_path}"
            )

        width = int(
            cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        )

        height = int(
            cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        )

        fps = cap.get(cv2.CAP_PROP_FPS)

        if fps <= 0:
            fps = 30.0

        cap.release()

        zone_width = width // self.number_of_zones

        writer = cv2.VideoWriter(
            output_path,
            cv2.VideoWriter_fourcc(*"mp4v"),
            fps,
            (width, height)
        )

        if not writer.isOpened():
            raise ValueError(
                "Could not create output video."
            )

        zone_analytics = {}

        for zone in range(self.number_of_zones):

            zone_analytics[zone] = {
                "risk_history": [],
                "people_history": [],
                "speed_history": [],
                "warning_frames": 0,
                "counterflow_frames": 0,
                "peak_risk": 0,
                "peak_people": 0
            }


        maximum_risk = 0
        total_alert_frames = 0
        frame_count = 0



        results = self.model.track(
            source=video_path,
            classes=[0],
            conf=self.confidence,
            tracker="bytetrack.yaml",
            persist=True,
            stream=True,
            verbose=False
        )


        final_zones = {}


        for result in results:

            frame_count += 1

            frame = result.orig_img.copy()

            zone_counts = [
                0
            ] * self.number_of_zones

            zone_speeds = {
                z: []
                for z in range(
                    self.number_of_zones
                )
            }

            zone_directions = {
                z: []
                for z in range(
                    self.number_of_zones
                )
            }


            if (
                result.boxes is not None
                and result.boxes.id is not None
            ):

                boxes = (
                    result.boxes.xyxy
                    .cpu()
                    .numpy()
                )

                track_ids = (
                    result.boxes.id
                    .int()
                    .cpu()
                    .tolist()
                )


                for box, track_id in zip(
                    boxes,
                    track_ids
                ):

                    x1, y1, x2, y2 = map(
                        int,
                        box[:4]
                    )

                    current_x = int(
                        (x1 + x2) / 2
                    )

                    current_y = int(y2)



                    zone = min(
                        current_x // zone_width,
                        self.number_of_zones - 1
                    )

                    zone_counts[zone] += 1


                    history = (
                        self.track_history[track_id]
                    )

                    previous = (
                        history[-1]
                        if history
                        else None
                    )

                    history.append(
                        (current_x, current_y)
                    )


                    speed = 0
                    direction = "STILL"


                    if previous:

                        old_x, old_y = previous

                        dx = current_x - old_x
                        dy = current_y - old_y

                        distance = math.sqrt(
                            dx ** 2 + dy ** 2
                        )

                        speed = distance * fps

                        zone_speeds[
                            zone
                        ].append(speed)



                    if len(history) >= 5:

                        old_x, old_y = history[0]

                        dx = current_x - old_x
                        dy = current_y - old_y

                        movement = math.sqrt(
                            dx ** 2 + dy ** 2
                        )

                        if movement > 10:

                            if abs(dx) > abs(dy):

                                direction = (
                                    "RIGHT"
                                    if dx > 0
                                    else "LEFT"
                                )

                            else:

                                direction = (
                                    "DOWN"
                                    if dy > 0
                                    else "UP"
                                )


                    if direction != "STILL":

                        zone_directions[
                            zone
                        ].append(direction)


                    cv2.rectangle(
                        frame,
                        (x1, y1),
                        (x2, y2),
                        (255, 255, 255),
                        1
                    )

                    cv2.putText(
                        frame,
                        f"ID {track_id}",
                        (
                            x1,
                            max(y1 - 5, 15)
                        ),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.35,
                        (255, 255, 255),
                        1
                    )


            frame_has_alert = False


            for zone in range(
                self.number_of_zones
            ):

                speeds = zone_speeds[zone]

                avg_speed = (
                    sum(speeds) / len(speeds)
                    if speeds
                    else 0
                )


                directions = Counter(
                    zone_directions[zone]
                )

                left = directions["LEFT"]
                right = directions["RIGHT"]
                up = directions["UP"]
                down = directions["DOWN"]


                counterflow = (
                    (left >= 2 and right >= 2)
                    or
                    (up >= 2 and down >= 2)
                )


                risk = calculate_risk(
                    zone_counts[zone],
                    avg_speed,
                    counterflow
                )

                status = get_status(risk)

                trend, change, warning = (
                    self.trend_analyzer.analyze(
                        zone,
                        risk
                    )
                )


                analytics = zone_analytics[zone]

                analytics[
                    "risk_history"
                ].append(risk)

                analytics[
                    "people_history"
                ].append(
                    zone_counts[zone]
                )

                analytics[
                    "speed_history"
                ].append(
                    round(avg_speed, 2)
                )

                analytics["peak_risk"] = max(
                    analytics["peak_risk"],
                    risk
                )

                analytics["peak_people"] = max(
                    analytics["peak_people"],
                    zone_counts[zone]
                )

                if warning:

                    analytics[
                        "warning_frames"
                    ] += 1

                    frame_has_alert = True


                if counterflow:

                    analytics[
                        "counterflow_frames"
                    ] += 1


                maximum_risk = max(
                    maximum_risk,
                    risk
                )


                final_zones[zone] = {
                    "zone": chr(65 + zone),
                    "people": zone_counts[zone],
                    "average_speed": round(
                        avg_speed,
                        2
                    ),
                    "counterflow": counterflow,
                    "risk": risk,
                    "status": status,
                    "trend": trend,
                    "risk_change": change,
                    "early_warning": warning
                }


                if status == "SAFE":
                    color = (0, 255, 0)

                elif status == "CAUTION":
                    color = (0, 255, 255)

                elif status == "HIGH":
                    color = (0, 165, 255)

                else:
                    color = (0, 0, 255)


                x_start = (
                    zone * zone_width
                )

                if (
                    zone
                    == self.number_of_zones - 1
                ):

                    x_end = width

                else:

                    x_end = (
                        (zone + 1)
                        * zone_width
                    )


                cv2.rectangle(
                    frame,
                    (x_start, 0),
                    (x_end - 1, height - 1),
                    color,
                    3
                )


                text_x = x_start + 8

                information = [
                    f"ZONE {chr(65 + zone)}",
                    f"People: {zone_counts[zone]}",
                    f"Speed: {avg_speed:.0f}px/s",
                    (
                        "Flow: COUNTER"
                        if counterflow
                        else "Flow: NORMAL"
                    ),
                    f"Risk: {risk}/100",
                    f"Status: {status}",
                    f"Trend: {trend}"
                ]


                y = 22

                for line in information:

                    cv2.putText(
                        frame,
                        line,
                        (text_x, y),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.38,
                        color,
                        1
                    )

                    y += 19


                if warning:

                    cv2.putText(
                        frame,
                        "EARLY WARNING!",
                        (text_x, y + 8),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.45,
                        (0, 0, 255),
                        2
                    )


            if frame_has_alert:

                total_alert_frames += 1


            writer.write(frame)


        writer.release()


        analytics_summary = []


        for zone in range(
            self.number_of_zones
        ):

            data = zone_analytics[zone]

            risk_history = (
                data["risk_history"]
            )

            speed_history = (
                data["speed_history"]
            )


            average_risk = (
                sum(risk_history)
                / len(risk_history)
                if risk_history
                else 0
            )

            average_speed = (
                sum(speed_history)
                / len(speed_history)
                if speed_history
                else 0
            )


            analytics_summary.append(
                {
                    "zone": chr(65 + zone),

                    "peak_risk":
                        data["peak_risk"],

                    "average_risk":
                        round(
                            average_risk,
                            2
                        ),

                    "peak_people":
                        data["peak_people"],

                    "average_speed":
                        round(
                            average_speed,
                            2
                        ),

                    "warning_frames":
                        data[
                            "warning_frames"
                        ],

                    "counterflow_frames":
                        data[
                            "counterflow_frames"
                        ],

                    "risk_history":
                        data[
                            "risk_history"
                        ],

                    "people_history":
                        data[
                            "people_history"
                        ]
                }
            )

        return {
            "frames_processed": frame_count,
            "maximum_risk": maximum_risk,
            "alert_frames": total_alert_frames,
            "zones": list(
                final_zones.values()
            ),
            "analytics": analytics_summary,
            "output_video": output_path,
            "fps": fps
        }
