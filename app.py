import os
import tempfile
import pandas as pd
import streamlit as st

from core.crowd_analyzer import CrowdAnalyzer

st.set_page_config(
    page_title="JAN-RAKSHA",
    page_icon="🛡️",
    layout="wide"
)

st.markdown(
    
    unsafe_allow_html=True
)

st.markdown(
    '<p class="main-title">🛡️ JAN-RAKSHA</p>',
    unsafe_allow_html=True
)

st.markdown(
    
    unsafe_allow_html=True
)

st.divider()

with st.sidebar:

    st.header("Control Center")

    st.write(
        "Upload crowd footage for AI-assisted "
        "crowd safety analysis."
    )

    confidence = st.slider(
        "Detection Confidence",
        min_value=0.20,
        max_value=0.80,
        value=0.35,
        step=0.05
    )

    st.divider()

    st.markdown("### Analysis Features")

    st.write("✓ Person detection")
    st.write("✓ Person tracking")
    st.write("✓ Zone monitoring")
    st.write("✓ Crowd concentration")
    st.write("✓ Movement analysis")
    st.write("✓ Counter-flow detection")
    st.write("✓ Crowd risk scoring")
    st.write("✓ Temporal risk analysis")
    st.write("✓ Early warning")

    st.divider()

    st.caption(
        "JAN-RAKSHA Prototype V1"
    )

st.subheader("Crowd Footage")

uploaded_video = st.file_uploader(
    "Upload CCTV or crowd footage",
    type=["mp4", "mov", "avi"]
)


if uploaded_video is None:

    st.info(
        "Upload a crowd video to begin "
        "JAN-RAKSHA analysis."
    )

    st.stop()

suffix = os.path.splitext(
    uploaded_video.name
)[1]


with tempfile.NamedTemporaryFile(
    delete=False,
    suffix=suffix
) as temp_file:

    temp_file.write(
        uploaded_video.getbuffer()
    )

    input_path = temp_file.name

st.markdown("### Original Footage")

st.video(uploaded_video)


if st.button(
    "🔍 Analyze Crowd Risk",
    type="primary",
    use_container_width=True
):

    output_path = (
        tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".mp4"
        ).name
    )

    with st.spinner(
        "JAN-RAKSHA is analysing crowd behaviour..."
    ):

        try:

            analyzer = CrowdAnalyzer(
                confidence=confidence
            )

            summary = analyzer.analyze_video(
                video_path=input_path,
                output_path=output_path
            )

        except Exception as error:

            st.error(
                f"Analysis failed: {error}"
            )

            st.stop()


    st.success(
        "✓ Crowd analysis completed successfully."
    )

    st.divider()

    st.header("Command Center Overview")


    metric1, metric2, metric3, metric4 = (
        st.columns(4)
    )


    metric1.metric(
        "Peak Risk",
        f"{summary['maximum_risk']}/100"
    )


    metric2.metric(
        "Frames Analysed",
        summary["frames_processed"]
    )


    metric3.metric(
        "Alert Frames",
        summary["alert_frames"]
    )

    peak_crowd = max(
        zone["peak_people"]
        for zone in summary["analytics"]
    )


    metric4.metric(
        "Peak Zone Crowd",
        peak_crowd
    )


    st.divider()


    st.header("AI Crowd Analysis")


    if os.path.exists(
        summary["output_video"]
    ):

        with open(
            summary["output_video"],
            "rb"
        ) as video_file:

            video_bytes = (
                video_file.read()
            )


        st.video(video_bytes)


    st.caption(
        "Bounding boxes represent detected and tracked "
        "individuals. Zone borders change according to "
        "the calculated crowd-risk level."
    )


    st.divider()


    st.header("Zone Status")

    st.caption(
        "The values below represent the final analysed "
        "frame of the uploaded footage."
    )


    zones = summary["zones"]

    zone_columns = st.columns(
        len(zones)
    )


    for column, zone in zip(
        zone_columns,
        zones
    ):

        with column:

            st.markdown(
                f"### Zone {zone['zone']}"
            )


            st.metric(
                "Current Risk",
                f"{zone['risk']}/100"
            )


            status = zone["status"]


            if status == "SAFE":

                st.success(
                    f"🟢 {status}"
                )

            elif status == "CAUTION":

                st.warning(
                    f"🟡 {status}"
                )

            elif status == "HIGH":

                st.warning(
                    f"🟠 {status}"
                )

            else:

                st.error(
                    f"🔴 {status}"
                )


            st.write(
                f"**People:** "
                f"{zone['people']}"
            )


            st.write(
                f"**Average Speed:** "
                f"{zone['average_speed']} px/s"
            )


            flow = (
                "⚠ Counter-flow detected"
                if zone["counterflow"]
                else "✓ Normal flow"
            )


            st.write(
                f"**Flow:** {flow}"
            )


            st.write(
                f"**Trend:** "
                f"{zone['trend']}"
            )


            if zone["early_warning"]:

                st.error(
                    "⚠️ EARLY WARNING"
                )


    st.divider()


    st.header("Risk Timeline")

    st.write(
        "This chart shows how the JAN-RAKSHA "
        "risk index changed throughout the video."
    )


    chart_data = {}


    for zone in summary["analytics"]:

        chart_data[
            f"Zone {zone['zone']}"
        ] = zone["risk_history"]


    risk_dataframe = pd.DataFrame(
        chart_data
    )


    st.line_chart(
        risk_dataframe,
        height=350
    )


    st.caption(
        "A sustained upward trend may indicate "
        "developing crowd-risk conditions."
    )


    st.divider()

    st.header("Full Video Analytics")

    st.write(
        "Unlike the current zone status, these metrics "
        "summarise conditions across the entire video."
    )


    analytics_columns = st.columns(
        len(summary["analytics"])
    )


    for column, zone in zip(
        analytics_columns,
        summary["analytics"]
    ):

        with column:

            st.markdown(
                f"### Zone {zone['zone']}"
            )


            st.metric(
                "Peak Risk",
                f"{zone['peak_risk']}/100"
            )


            st.metric(
                "Average Risk",
                f"{zone['average_risk']}/100"
            )


            st.metric(
                "Peak Crowd",
                zone["peak_people"]
            )


            st.write(
                f"**Average Movement:** "
                f"{zone['average_speed']} px/s"
            )


            st.write(
                f"**Warning Frames:** "
                f"{zone['warning_frames']}"
            )


            st.write(
                f"**Counter-flow Frames:** "
                f"{zone['counterflow_frames']}"
            )


    st.divider()


    st.header("⚠ Early Warning Center")

    current_warning_zones = [
        zone
        for zone in zones
        if zone["early_warning"]
    ]

    historical_warning_zones = [
        zone
        for zone in summary["analytics"]
        if zone["warning_frames"] > 0
    ]


    if current_warning_zones:

        for zone in current_warning_zones:

            st.error(
                f"⚠ Zone {zone['zone']}: "
                f"Risk indicators are currently rising. "
                f"Current risk is "
                f"{zone['risk']}/100."
            )

    else:

        st.success(
            "No active early warning in the "
            "final analysed frame."
        )


    if historical_warning_zones:

        st.markdown(
            "### Warnings Detected During Video"
        )


        for zone in historical_warning_zones:

            st.warning(
                f"Zone {zone['zone']} generated "
                f"{zone['warning_frames']} "
                f"warning frame(s) during analysis."
            )


    st.divider()


    st.header("System Interpretation")


    highest_zone = max(
        summary["analytics"],
        key=lambda zone: zone["peak_risk"]
    )


    st.write(
        f"The highest observed risk occurred in "
        f"**Zone {highest_zone['zone']}**, reaching "
        f"**{highest_zone['peak_risk']}/100**."
    )


    if highest_zone["counterflow_frames"] > 0:

        st.write(
            f"Counter-flow behaviour was detected "
            f"in Zone {highest_zone['zone']} during "
            f"{highest_zone['counterflow_frames']} "
            f"frame(s)."
        )


    if highest_zone["warning_frames"] > 0:

        st.warning(
            f"Zone {highest_zone['zone']} showed "
            f"a rising risk pattern during the footage."
        )


    st.divider()


    with st.expander(
        "How does JAN-RAKSHA calculate risk?"
    ):

        st.markdown(
            
        )



    with st.expander(
        "Prototype limitations"
    ):

        st.markdown(
            
        )


    st.divider()


    st.caption(
        "JAN-RAKSHA • AI-Powered Crowd Risk Monitoring "
        "& Early Warning System • Prototype V1"
    )