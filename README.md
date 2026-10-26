
JAN RAKSHA is a computer vision based crowd safety prototype designed to
identify emerging risk patterns in large public gatherings such as the
Kumbh Mela,festivals,religious gatherings,transport hubs and public events.

Instead of only counting people, JAN RAKSHA analyses crowd concentration,
movement speed,movement direction,counter flow and temporal risk trends
to provide an interpretable zone wise Crowd Risk Index and early warnings.

> JAN RAKSHA does not identify individuals.It analyses crowd movement,
> not personal identity.

Traditional CCTV systems primarily provide visual surveillance.

During very large gatherings, operators may need to simultaneously monitor
multiple crowd zones and identify conditions such as:

- increasing crowd concentration
- reduced crowd movement
- opposing pedestrian flows
- congestion
- rapidly increasing risk indicators

JAN RAKSHA acts as an AI assisted decision support layer over crowd footage.

- Person detection using YOLO
- Multi object tracking using ByteTrack
- Zone based crowd monitoring
- Crowd concentration analysis
- Movement speed estimation
- Movement direction analysis
- Counter flow detection
- Explainable Crowd Risk Index (0-100)
- Temporal risk trend analysis
- Early warning generation
- Full video analytics
- Interactive Streamlit command center dashboard
- Automated tests

Crowd Video
     |
YOLO Person Detection
     |
ByteTrack Tracking
     |
Zone Based Crowd Analysis
     |
     |── Crowd Concentration
     |── Movement Speed
     |── Movement Direction
     |── Counter Flow
     |
JAN RAKSHA Risk Engine
     |
Temporal Trend Analysis
     |
Early Warning
     |
Streamlit Command Center

Detailed architecture documentation is available in:

`docs/TECHNICAL_DESIGN.md`

JAN RAKSHA V1 uses an explainable heuristic risk index.

| Signal | Maximum Contribution |
|---|---:|
| Crowd concentration | 40 |
| Counter-flow | 35 |
| Movement congestion | 25 |
| **Total** | **100** |

Risk categories:

| Score | Status |
|---|---|
| 0-24 | SAFE |
| 25-49 | CAUTION |
| 50-74 | HIGH |
| 75-100 | CRITICAL |

These values are prototype parameters and are not validated operational
crowd safety thresholds.

- Python
- Ultralytics YOLO
- ByteTrack
- OpenCV
- Streamlit
- Pandas
- NumPy
- Pytest

jan_raksha/
│
├── app.py
├── README.md
├── LICENSE
├── requirements.txt
├── requirements-dev.txt
├── .env.example
├── .gitignore
│
├── core/
│   ├── crowd_analyzer.py
│   ├── risk_engine.py
│   └── trend_analyzer.py
│
├── sample_data/
│   ├── README.md
│   └── sample_scenarios.csv
│
├── tests/
│   ├── test_risk_engine.py
│   ├── test_trend_analyzer.py
│   └── test_sample_scenarios.py
│
└── docs/
    └── TECHNICAL_DESIGN.md

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt

Streamlit will provide a local address, normally:

http://localhost:8501

Open it in your browser.

Then:

1. Upload crowd footage.
2. Adjust detection confidence if required.
3. Click Analyze Crowd Risk.
4. Wait for the video analysis to complete.
5. Review the processed video, zone risk levels, timeline and warnings.

Supported upload formats include:

- MP4
- MOV
- AVI


Install development dependencies:

pip install -r requirements-dev.txt

Run:

python -m pytest tests/ -v


The repository contains tests covering:

- safe crowd conditions
- high risk conditions
- critical counter-flow conditions
- risk score limits
- temporal monitoring
- rising risk
- falling risk
- early warnings
- analyzer reset behaviour
- synthetic sample scenarios


`sample_data/sample_scenarios.csv` contains synthetic crowd scenarios for
testing the risk engine.

Third party crowd footage is intentionally not redistributed with the
repository unless redistribution rights are confirmed.

Users may analyse their own appropriately licensed crowd footage through
the dashboard.

JAN RAKSHA does not require facial recognition.

The prototype tracks anonymous detection IDs only for short-term movement
analysis within a video.

The objective is to understand **crowd behaviour rather than citizen identity**.

# Limitations

JAN RAKSHA V1 is a hackathon prototype.

Current limitations include:

- Image space speed is measured in pixels/second rather than metres/second.
- Physical crowd density requires camera calibration and real world area mapping.
- Detection accuracy may decrease under heavy occlusion.
- Performance depends on camera angle, lighting and video quality.
- Risk weights and thresholds require validation against real crowd safety data.
- The risk index is not a probability that a stampede will occur.
- The system is not a replacement for trained crowd-safety professionals.

# Future Development

Potential extensions include:

- perspective aware crowd density estimation
- camera calibration and real world speed estimation
- GIS based multi camera risk maps
- live CCTV/RTSP stream ingestion
- cross camera crowd flow analysis
- validated temporal forecasting models
- authority notification systems
- recommended crowd diversion routes
- edge deployment for event surveillance systems

# Social Impact

JAN RAKSHA is designed around the principle:

> Detect emerging crowd danger before visible panic becomes an emergency.

The system is intended to support safer management of large public gatherings
while avoiding unnecessary identity based surveillance.

# License

This project is released under the MIT License.

See `LICENSE` for details.


## Disclaimer

JAN RAKSHA is an experimental decision support prototype developed for
hackathon and educational purposes. It must not be treated as a certified
public safety system or used as the sole basis for operational crowd management
decisions.
