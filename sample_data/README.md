
This directory contains sample inputs for testing the JAN RAKSHA prototype.

The CSV contains synthetic crowd scenarios that can be used to test the
JAN RAKSHA risk engine.

| Field | Description |
|---|---|
| scenario | Name of the synthetic crowd situation |
| person_count | Number of detected people in a monitored zone |
| average_speed | Average image-space movement speed in pixels/second |
| counterflow | Whether opposing crowd movement is detected |
| expected_status | Expected JAN-RAKSHA risk category |

The scenarios are synthetic and are provided for software testing and
demonstration.They are not validated crowd safety thresholds.

JAN RAKSHA accepts MP4,MOV and AVI crowd footage through the Streamlit
dashboard.

A video file is intentionally not bundled in this repository so that
third party footage is not redistributed without appropriate permission.

Users can test the application using their own crowd footage for which
they have appropriate rights.

JAN RAKSHA V1 is a hackathon prototype.The included sample scenarios and
risk thresholds must not be interpreted as operational crowd safety
standards.
