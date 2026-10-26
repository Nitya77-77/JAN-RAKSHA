# JAN RAKSHA Technical Design Document

#1.Overview

JAN RAKSHA is an AI assisted crowd risk monitoring and early warning prototype
for large public gatherings.

The system processes crowd video, detects and tracks pedestrians,analyses
zone level crowd behaviour,calculates an explainable risk index,monitors
risk trends over time and presents the results through a Streamlit command
center.
The system is designed as a decision support prototype rather than an
autonomous public safety system.

#2.Objectives

JAN RAKSHA aims to:

1.Detect people in crowd footage.
2.Track anonymous pedestrian movement across frames.
3.Divide monitored footage into analysis zones.
4.Estimate crowd concentration within each zone.
5.Analyse movement speed and direction.
6.Detect opposing pedestrian flows.
7.Generate an interpretable Crowd Risk Index.
8.Monitor how risk changes over time.
9.Generate early warnings for rising risk conditions.
10.Present results through an interactive dashboard.

#3.High Level Architecture

flowchart TD

    A[CCTV / Uploaded Crowd Video]
    --> B[YOLO Person Detection]

    B --> C[ByteTrack Multi Object Tracking]

    C --> D[Zone Based Crowd Analyzer]

    D --> E1[Crowd Concentration]
    D --> E2[Movement Speed]
    D --> E3[Movement Direction]
    D --> E4[Counter Flow Detection]

    E1 --> F[JAN RAKSHA Risk Engine]
    E2 --> F
    E3 --> F
    E4 --> F

    F --> G[Temporal Trend Analyzer]

    G --> H[Early Warning Engine]

    H --> I[Analytics Summary]

    I --> J[Streamlit Command Center]

#4.Data Flow

Video
  |
Frame
  |
YOLO
  |
Person Bounding Boxes
  |
ByteTrack
  |
Anonymous Track IDs
  |
Ground Position Approximation
  |
  |-- Zone Assignment
  |-- Movement Distance
  |-- Direction
  |-- Speed
  |
Zone Behaviour Analysis
  |
  |-- Person Count
  |-- Average Movement Speed
  |-- Counter Flow
  |
Risk Engine
  |
Risk Score 0-100
  |
Temporal Trend Analysis
  |
Early Warning
  |
Dashboard

#5. Major Components

##5.1 Person Detection

JAN RAKSHA uses a pretrained Ultralytics YOLO model.

For the current prototype:

Model: YOLO11 Nano
Class analysed: Person
Default confidence: 0.35

##5.2 Multi Object Tracking

ByteTrack is used to associate detections between consecutive frames.

Instead of independently observing:

Frame 1: Person
Frame 2: Person
Frame 3: Person

Frame 1: Person ID 7
Frame 2: Person ID 7
Frame 3: Person ID 7

#6.Ground Position Approximation

For every person bounding box:

(x1, y1, x2, y2)

JAN RAKSHA uses approximately the bottom center point:

x = (x1 + x2) / 2
y = y2

This provides a simple approximation of the person's position on the
visible ground plane.

#7.Zone Analysis

The current prototype divides the image into three vertical monitoring zones:

+-------------+-------------+-------------+
|             |             |             |
|   ZONE A    |   ZONE B    |   ZONE C    |
|             |             |             |
+-------------+-------------+-------------+

Each tracked person's bottom center position determines their current zone.

The architecture can later support manually defined polygons or GIS linked
monitoring regions.

#8.Movement Speed

Movement is estimated by comparing a tracked person's position between frames.

For positions:

P1 = (x1, y1)
P2 = (x2, y2)

image space displacement is:

distance = sqrt((x2-x1)^2 + (y2-y1)^2)

Approximate image space speed:

speed = distance x FPS

The result is measured in:

pixels/second

This is useful for relative movement analysis but is not equivalent to
physical walking speed.

Real world speed estimation would require perspective correction and
camera calibration.

#9.Movement Direction

A short trajectory history is stored for every tracking ID.

The displacement is calculated as:

dx = current_x - previous_x
dy = current_y - previous_y


LEFT
RIGHT
UP
DOWN
STILL

Small movements are ignored to reduce detection jitter.


#10.Counter Flow Detection

Counter flow represents significant movement occurring in opposing directions
within the same monitored zone.

Horizontal conflict:

LEFT >= 2 AND RIGHT >= 2

Vertical conflict:

UP >= 2 AND DOWN >= 2

If either condition occurs,the zone receives a counter flow signal.

The thresholds are prototype parameters.

#11. Crowd Risk Engine

JAN RAKSHA V1 intentionally uses an explainable heuristic risk model.

The risk score consists of:

| Component | Maximum Score |
|---|---:|
| Crowd concentration | 40 |
| Counter-flow | 35 |
| Movement congestion | 25 |
| Total | 100 |

#11.1 Crowd Concentration

The current prototype normalizes zone occupancy using:

density_ratio = min(person_count / 15, 1)
density_score = density_ratio x 40

Therefore the concentration component contributes at most 40 points.

The value '15' is a prototype normalization constant rather than a
validated physical density threshold.


##11.2 Counter Flow

If counter flow is detected:

counterflow_score = 35

Otherwise:

counterflow_score = 0

#11.3 Movement Congestion

For zones containing at least two people:

Average Speed < 10 px/s    - 25 points
Average Speed < 25 px/s    - 18 points
Average Speed < 40 px/s    - 10 points
Average Speed >= 40 px/s   - 0 points


This allows slow movement to increase the prototype risk index.

#11.4 Final Risk Score

Risk =
    Crowd Concentration Score
    + Counter low Score
    + Congestion Score

The result is limited to:

0 <= Risk <= 100

Classification:

| Risk | Status |
|---|---|
| 0-24 | SAFE |
| 25-49 | CAUTION |
| 50-74 | HIGH |
| 75-100 | CRITICAL |

The score represents a prototype risk index.

It is not a probability of stampede occurrence.

#12.Temporal Risk Analysis

Analysing only the current frame may hide developing risk.

JAN RAKSHA therefore stores recent risk values separately for every zone.

Conceptually:

20 -> 24 -> 29 -> 37 -> 48 -> 61
                         |
                    rising risk


Recent risk values are compared against earlier values.

Trend states include:

MONITORING
STABLE
RISING
RISING FAST
FALLING

#13.Early Warning

An early warning is generated when:

Trend = RISING or RISING FAST

AND

Current Risk >= 40


This is intended to highlight zones where risk indicators are both elevated
and worsening.

#14.Full Video Analytics

JAN RAKSHA records analytics across the complete video.

For every zone,the system stores:

- risk history
- people count history
- speed history
- peak risk
- average risk
- peak detected crowd
- warning frames
- counter flow frames

This prevents the dashboard from relying only on the final video frame.


#15.Dashboard Architecture

The Streamlit dashboard provides:

Upload Crowd Video
        |
Analyze Crowd Risk
        |
CrowdAnalyzer
        |
Structured Analysis Summary
        |
        |-- Processed Video
        |-- Peak Risk
        |-- Zone Status
        |-- Risk Timeline
        |-- Full Video Analytics
        |-- Early Warnings

#16.Software Architecture

app.py
  |
core/crowd_analyzer.py
  |
  |----------> core/risk_engine.py
  |
  |----------> core/trend_analyzer.py
  |
Structured Results
  |
Streamlit Dashboard

Responsibilities are separated so that risk and temporal logic can be tested
separately.
#17.Testing Strategy

JAN RAKSHA uses Pytest.

Current automated tests cover:

- safe crowd conditions
- high risk conditions
- critical counter flow conditions
- risk score upper bounds
- temporal monitoring
- rising risk
- early warning activation
- falling risk
- trend analyzer reset
- synthetic sample scenarios

Tests can be executed with:

python -m pytest tests/ -v

#18.Privacy and Responsible Design

JAN RAKSHA does not require facial recognition.

The system analyses:

bounding boxes
temporary tracking IDs
positions
movement trajectories
zone level behaviour

It does not attempt to determine:

name
identity
demographic information
personal profile

This enables crowd behaviour analysis without requiring identity-based
surveillance.

#19.Security Considerations

The prototype processes user supplied video files locally within the running
application environment.

Production deployments should additionally implement:

- strict upload size limits
- file type validation
- authenticated dashboard access
- encrypted communication
- access logging
- secure video retention policies
- automatic deletion of temporary footage
- role based permissions

#20. Known Limitations

JAN RAKSHA V1 has several important limitations.

#Camera Perspective

People farther from the camera appear smaller and move fewer pixels.

#Physical Density

Person count per image zone is not equivalent to people per square metre.

#Occlusion

Extremely dense crowds may cause missed detections or unstable tracking.

#Speed

Movement is currently represented in pixels/second.

#Counter Flow

The current rule based counter flow detector is intentionally simple.

Risk weights and thresholds have not been validated against operational
crowd disaster datasets.

The prototype currently uses three equal vertical zones rather than
venue specific polygons.


#21.Future Architecture

A production oriented JAN RAKSHA system could evolve toward:

Multiple CCTV/Drone Streams
             |
      Edge AI Processing
             |
Perspective Calibration
             |
Real World Crowd Density
             |
Multi Camera Flow Fusion
             |
Temporal Forecasting Model
             |
GIS Crowd Risk Map
             |
Command & Control Center
             |
             |-- Alerts
             |-- Route Diversion
             |-- Emergency Response


#22.Future Improvements

Potential improvements include:

1. Perspective aware density estimation.
2. Real world speed estimation.
3. Polygon based custom zones.
4. Live CCTV/RTSP ingestion.
5. Multi camera tracking.
6. GIS integration.
7. Validated temporal forecasting.
8. Dynamic bottleneck detection.
9. Automated crowd diversion recommendations.
10. Edge device deployment.


#23.Deployment Considerations

Before operational use,JAN RAKSHA would require:

- validated crowd safety datasets
- venue specific calibration
- professional crow safety review
- extensive field testing
- false positive and false negative analysis
- privacy and data protection review
- resilience testing
- human in the loop operating procedures


#24.Conclusion

JAN RAKSHA demonstrates how computer vision and interpretable crowd analytics
can transform ordinary video footage into structured crowd risk information.

The prototype combines detection,tracking,crowd behaviour analysis,
explainable risk scoring and temporal monitoring while avoiding facial
recognition.

Its primary design principle is:

> Understand how the crowd is behaving, identify worsening conditions,
> and help human operators intervene earlier.
