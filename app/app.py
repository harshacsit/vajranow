import sys
from pathlib import Path

# ============================================================
# VAJRANOW
# AI-BASED THUNDERSTORM & LIGHTNING NOWCASTING
# ============================================================

# ------------------------------------------------------------
# PROJECT PATH
# ------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# ------------------------------------------------------------
# IMPORTS
# ------------------------------------------------------------

import numpy as np
import pandas as pd
import streamlit as st
import folium

from streamlit_folium import folium_static

from src.ai_model import (
    load_model,
    predict_risk
)


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="VajraNow | Thunderstorm Nowcasting",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# GLOBAL UI STYLE
# ============================================================

st.markdown(
    """
    <style>

    /* ========================================================
       GLOBAL
       ======================================================== */

    [data-testid="stAppViewContainer"] {
        background: #f5f7fb;
    }

    [data-testid="stHeader"] {
        background: transparent;
    }

    .block-container {
        max-width: 1500px;
        padding-top: 1.2rem;
        padding-bottom: 3rem;
    }

    /* ========================================================
       MAIN TITLE
       ======================================================== */

    h1 {
        color: #101828;
        font-weight: 900 !important;
        letter-spacing: -1.5px;
    }

    h2, h3 {
        color: #172033;
        font-weight: 800 !important;
    }

    /* ========================================================
       METRICS
       ======================================================== */

    [data-testid="stMetric"] {
        background: #ffffff;
        border: 1px solid #e4e7ec;
        border-radius: 14px;
        padding: 14px 16px;
        box-shadow: 0 2px 8px rgba(16, 24, 40, 0.04);
    }

    [data-testid="stMetricLabel"] {
        color: #667085 !important;
        font-weight: 700 !important;
    }

    [data-testid="stMetricValue"] {
        color: #101828 !important;
        font-weight: 850 !important;
    }

    /* ========================================================
       CONTAINERS
       ======================================================== */

    [data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 15px !important;
        border-color: #e4e7ec !important;
        background: #ffffff;
    }

    /* ========================================================
       BUTTONS
       ======================================================== */

    .stButton > button {
        border-radius: 10px;
        min-height: 42px;
        font-weight: 700;
    }

    /* ========================================================
       SLIDER
       ======================================================== */

    [data-testid="stSlider"] {
        padding-top: 4px;
    }

    /* ========================================================
       TABLE
       ======================================================== */

    [data-testid="stDataFrame"] {
        border-radius: 12px;
        overflow: hidden;
    }

    /* ========================================================
       MAP
       ======================================================== */

    iframe {
        border-radius: 14px;
    }

    /* ========================================================
       FOOTER
       ======================================================== */

    .footer-note {
        text-align: center;
        color: #98a2b3;
        font-size: 12px;
        line-height: 1.6;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# MODEL LOADING
# ============================================================

MODEL_PATH = (
    PROJECT_ROOT
    / "models"
    / "vajranow_rf.pkl"
)


@st.cache_resource
def get_model():

    return load_model(
        MODEL_PATH
    )


try:

    ai_model = get_model()

    model_loaded = True

except Exception as error:

    ai_model = None

    model_loaded = False

    st.error(
        f"Unable to load VajraNow AI model: {error}"
    )


# ============================================================
# DEMO SCENARIOS
# ============================================================

SCENARIOS = {

    "🌤️ Low Activity": {
        "radar_reflectivity": 22,
        "lightning_activity": 2,
        "cloud_development": 35,
        "atmospheric_instability": 38
    },

    "🌩️ Developing Storm": {
        "radar_reflectivity": 38,
        "lightning_activity": 6,
        "cloud_development": 55,
        "atmospheric_instability": 72
    },

    "⛈️ Active Thunderstorm": {
        "radar_reflectivity": 48,
        "lightning_activity": 17,
        "cloud_development": 72,
        "atmospheric_instability": 81
    },

    "🔴 Severe Storm": {
        "radar_reflectivity": 62,
        "lightning_activity": 28,
        "cloud_development": 91,
        "atmospheric_instability": 94
    },

    "🌧️ Decaying Storm": {
        "radar_reflectivity": 28,
        "lightning_activity": 3,
        "cloud_development": 41,
        "atmospheric_instability": 48
    }
}


DEMO_STAGES = list(
    SCENARIOS.keys()
)


# ============================================================
# SESSION STATE
# ============================================================

if "demo_mode" not in st.session_state:

    st.session_state.demo_mode = False


if "demo_index" not in st.session_state:

    st.session_state.demo_index = 1


# ============================================================
# ALERT ENGINE
# ============================================================

def get_alert_level(
    thunderstorm_probability,
    lightning_probability
):

    combined_risk = (
        thunderstorm_probability * 0.7
        +
        lightning_probability * 0.3
    )

    if combined_risk >= 75:

        return {
            "level": "SEVERE",
            "icon": "🔴",
            "action":
                "Immediate preparedness recommended",
            "type": "error"
        }

    elif combined_risk >= 50:

        return {
            "level": "WARNING",
            "icon": "🟠",
            "action":
                "Prepare for possible severe weather",
            "type": "warning"
        }

    elif combined_risk >= 30:

        return {
            "level": "WATCH",
            "icon": "🟡",
            "action":
                "Monitor developing conditions",
            "type": "warning"
        }

    else:

        return {
            "level": "LOW",
            "icon": "🟢",
            "action":
                "No significant risk detected",
            "type": "success"
        }


# ============================================================
# FORECAST INPUT
# ============================================================

def get_forecast_input(
    weather,
    minutes
):

    time_factor = max(
        0.55,
        1.0 -
        (
            (minutes - 30)
            / 400
        )
    )

    return {

        "radar_reflectivity":
            weather["radar_reflectivity"]
            * time_factor,

        "lightning_activity":
            weather["lightning_activity"]
            * time_factor,

        "cloud_development":
            weather["cloud_development"]
            * time_factor,

        "atmospheric_instability":
            weather["atmospheric_instability"]
            * time_factor
    }


# ============================================================
# AI PREDICTION
# ============================================================

def get_ai_risk(
    weather,
    minutes
):

    if not model_loaded:

        return 0.0

    values = get_forecast_input(
        weather,
        minutes
    )

    probability = predict_risk(
        ai_model,
        values
    )

    probability = float(
        probability
    )

    # Handle either 0-1 or 0-100 output.
    if probability > 1:

        probability /= 100

    return float(
        np.clip(
            probability * 100,
            0,
            100
        )
    )


# ============================================================
# HEADER
# ============================================================

header_left, header_right = st.columns(
    [7, 2]
)


with header_left:

    st.title(
        "⚡ VajraNow"
    )

    st.caption(
        "Real-Time AI-Based Thunderstorm & Lightning Nowcasting"
    )


with header_right:

    if model_loaded:

        st.success(
            "● AI ENGINE ONLINE"
        )

    else:

        st.error(
            "AI ENGINE OFFLINE"
        )


st.divider()


# ============================================================
# FORECAST CONTROL
# ============================================================

st.subheader(
    "🎛️ Forecast Control"
)


with st.container(
    border=True
):

    control1, control2, control3 = st.columns(
        [2.2, 3.2, 2]
    )


    # --------------------------------------------------------
    # SCENARIO
    # --------------------------------------------------------

    with control1:

        if st.session_state.demo_mode:

            scenario_name = DEMO_STAGES[
                st.session_state.demo_index
            ]

            st.selectbox(
                "Storm Scenario",
                DEMO_STAGES,
                index=st.session_state.demo_index,
                disabled=True
            )

        else:

            scenario_name = st.selectbox(
                "Storm Scenario",
                DEMO_STAGES,
                index=2
            )


    # --------------------------------------------------------
    # FORECAST HORIZON
    # --------------------------------------------------------

    with control2:

        lead_time = st.select_slider(
            "Forecast Horizon",
            options=[
                30,
                60,
                90,
                120,
                150,
                180
            ],
            value=60,
            format_func=lambda x:
                f"+{x} min"
        )


    # --------------------------------------------------------
    # DEMO CONTROL
    # --------------------------------------------------------

    with control3:

        if not st.session_state.demo_mode:

            if st.button(
                "▶ Start Demo Mode",
                use_container_width=True
            ):

                st.session_state.demo_mode = True

                st.session_state.demo_index = 1

                st.rerun()

        else:

            if st.button(
                "⏭ Next Storm Stage",
                use_container_width=True
            ):

                st.session_state.demo_index += 1

                if (
                    st.session_state.demo_index
                    >= len(DEMO_STAGES)
                ):

                    st.session_state.demo_index = 0

                st.rerun()

            if st.button(
                "⏹ Exit Demo",
                use_container_width=True
            ):

                st.session_state.demo_mode = False

                st.rerun()


# ============================================================
# ACTIVE WEATHER
# ============================================================

weather = SCENARIOS[
    scenario_name
]


# ============================================================
# CURRENT RISK
# ============================================================

risk_percent = get_ai_risk(
    weather,
    lead_time
)


lightning_risk = min(
    95,
    weather["lightning_activity"] * 4
)


alert = get_alert_level(
    risk_percent,
    lightning_risk
)


# ============================================================
# ATMOSPHERIC OBSERVATIONS
# ============================================================

st.subheader(
    "📡 Current Atmospheric Situation"
)


k1, k2, k3, k4 = st.columns(4)


with k1:

    st.metric(
        "📡 Radar Reflectivity",
        f"{weather['radar_reflectivity']} dBZ"
    )


with k2:

    st.metric(
        "⚡ Lightning Activity",
        f"{weather['lightning_activity']} / min"
    )


with k3:

    st.metric(
        "☁️ Cloud Development",
        f"{weather['cloud_development']}%"
    )


with k4:

    st.metric(
        "🌡️ Atmospheric Instability",
        f"{weather['atmospheric_instability']}%"
    )


# ============================================================
# ALERT
# ============================================================

alert_message = (
    f"{alert['icon']} **{alert['level']}**  |  "
    f"{alert['action']}  |  "
    f"Forecast **+{lead_time} min**"
)


if alert["type"] == "error":

    st.error(
        alert_message
    )

elif alert["type"] == "warning":

    st.warning(
        alert_message
    )

else:

    st.success(
        alert_message
    )


# ============================================================
# NOWCAST SECTION
# ============================================================

st.subheader(
    "🌩️ Thunderstorm Nowcast"
)


st.caption(
    f"Simulated storm field for "
    f"{scenario_name} at +{lead_time} minutes."
)


map_column, risk_column = st.columns(
    [2.2, 1]
)


# ============================================================
# MAP
# ============================================================

with map_column:

    # --------------------------------------------------------
    # MAP CENTER
    # --------------------------------------------------------

    center_lat = 17.0
    center_lon = 80.5


    weather_map = folium.Map(
        location=[
            center_lat,
            center_lon
        ],
        zoom_start=7,
        tiles="OpenStreetMap",
        control_scale=True
    )


    # --------------------------------------------------------
    # STORM MOVEMENT
    # --------------------------------------------------------

    storm_shift = (
        lead_time - 30
    ) * 0.002


    scenario_multiplier = (
        weather["radar_reflectivity"]
        / 48
    )


    storm_centers = [

        (
            17.20 + storm_shift,
            80.30 + storm_shift * 2,
            0.95 * scenario_multiplier
        ),

        (
            16.70 + storm_shift * 0.6,
            81.00 + storm_shift,
            0.70 * scenario_multiplier
        ),

        (
            17.60 + storm_shift * 0.7,
            80.80 + storm_shift * 1.5,
            0.55 * scenario_multiplier
        )
    ]


    # --------------------------------------------------------
    # RISK GRID
    # --------------------------------------------------------

    latitudes = np.linspace(
        16.0,
        18.2,
        24
    )


    longitudes = np.linspace(
        79.5,
        81.7,
        24
    )


    for lat in latitudes:

        for lon in longitudes:

            local_risk = 0.015


            for (
                storm_lat,
                storm_lon,
                intensity
            ) in storm_centers:

                distance = (
                    (lat - storm_lat) ** 2
                    +
                    (lon - storm_lon) ** 2
                )


                local_risk += (
                    intensity
                    *
                    np.exp(
                        -distance / 0.065
                    )
                )


            ai_factor = (
                risk_percent
                / 100
            )


            local_risk *= (
                0.45
                +
                0.95 * ai_factor
            )


            local_risk = min(
                1.0,
                local_risk
            )


            if local_risk >= 0.70:

                color = "#ef4444"

            elif local_risk >= 0.50:

                color = "#f97316"

            elif local_risk >= 0.30:

                color = "#eab308"

            else:

                color = "#22c55e"


            folium.CircleMarker(
                location=[
                    lat,
                    lon
                ],
                radius=7,
                color=color,
                fill=True,
                fill_color=color,
                fill_opacity=0.48,
                weight=0,
                popup=(
                    f"Thunderstorm Risk: "
                    f"{local_risk * 100:.1f}%"
                )
            ).add_to(
                weather_map
            )


    # --------------------------------------------------------
    # STORM CELLS
    # --------------------------------------------------------

    for index, (
        lat,
        lon,
        intensity
    ) in enumerate(
        storm_centers,
        start=1
    ):

        folium.Circle(
            location=[
                lat,
                lon
            ],
            radius=18000 * max(
                intensity,
                0.5
            ),
            color="#dc2626",
            fill=False,
            weight=2,
            popup=(
                f"Storm Cell {index}"
            )
        ).add_to(
            weather_map
        )


        folium.Marker(
            location=[
                lat,
                lon
            ],
            tooltip=(
                f"⛈️ Storm Cell {index}"
            ),
            popup=(
                f"Storm Cell {index}<br>"
                f"Forecast: +{lead_time} min<br>"
                f"Intensity: {intensity:.2f}"
            )
        ).add_to(
            weather_map
        )


    # --------------------------------------------------------
    # MAP LEGEND
    # --------------------------------------------------------

    legend = folium.Element(
        """
        <div style="
            position: fixed;
            bottom: 25px;
            left: 25px;
            z-index: 9999;
            background: white;
            padding: 10px 14px;
            border-radius: 10px;
            box-shadow: 0 2px 8px rgba(0,0,0,.22);
            font-family: Arial;
            font-size: 12px;
            color: #344054;
        ">

        <b>Thunderstorm Risk</b><br><br>

        🟢 Low<br>
        🟡 Watch<br>
        🟠 Warning<br>
        🔴 Severe

        </div>
        """
    )


    weather_map.get_root().html.add_child(
        legend
    )


    # --------------------------------------------------------
    # MAP DISPLAY
    # --------------------------------------------------------

    folium_static(
        weather_map,
        width=900,
        height=500
    )


# ============================================================
# RISK PANEL
# ============================================================

with risk_column:

    with st.container(
        border=True
    ):

        st.markdown(
            "### 🎯 Risk Assessment"
        )


        st.metric(
            "Thunderstorm Probability",
            f"{risk_percent:.1f}%"
        )


        if alert["type"] == "error":

            st.error(
                f"{alert['icon']} {alert['level']}"
            )

        elif alert["type"] == "warning":

            st.warning(
                f"{alert['icon']} {alert['level']}"
            )

        else:

            st.success(
                f"{alert['icon']} {alert['level']}"
            )


        st.progress(
            min(
                risk_percent / 100,
                1.0
            )
        )


        st.metric(
            "⚡ Lightning Risk",
            f"{lightning_risk:.0f}%"
        )


        st.metric(
            "⏱ Forecast Lead",
            f"+{lead_time} min"
        )


        st.info(
            f"🚨 {alert['action']}"
        )


        st.caption(
            "Prototype probability using demonstration inputs."
        )


# ============================================================
# WHY THIS ALERT?
# ============================================================

st.subheader(
    "🔎 Why is VajraNow Alerting?"
)


st.caption(
    "Multiple atmospheric signals are combined before "
    "the prototype generates its risk estimate."
)


e1, e2, e3, e4 = st.columns(4)


with e1:

    with st.container(
        border=True
    ):

        st.markdown(
            "### 📡 Radar"
        )

        st.metric(
            "Reflectivity",
            f"{weather['radar_reflectivity']} dBZ"
        )

        st.caption(
            "Storm precipitation intensity signal."
        )


with e2:

    with st.container(
        border=True
    ):

        st.markdown(
            "### ⚡ Lightning"
        )

        st.metric(
            "Activity",
            f"{weather['lightning_activity']}/min"
        )

        st.caption(
            "Electrical activity around storm cells."
        )


with e3:

    with st.container(
        border=True
    ):

        st.markdown(
            "### ☁️ Cloud Growth"
        )

        st.metric(
            "Development",
            f"{weather['cloud_development']}%"
        )

        st.caption(
            "Prototype cloud-development indicator."
        )


with e4:

    with st.container(
        border=True
    ):

        st.markdown(
            "### 🌡️ Instability"
        )

        st.metric(
            "Index",
            f"{weather['atmospheric_instability']}%"
        )

        st.caption(
            "Prototype atmospheric instability indicator."
        )


# ============================================================
# FORECAST EVOLUTION
# ============================================================

st.subheader(
    "⏱️ Storm Risk Evolution"
)


st.caption(
    "Predicted thunderstorm probability across "
    "the next three hours."
)


forecast_times = [
    30,
    60,
    90,
    120,
    150,
    180
]


forecast_risks = [
    round(
        get_ai_risk(
            weather,
            time
        ),
        1
    )
    for time in forecast_times
]


timeline_columns = st.columns(
    6
)


for column, time, risk in zip(
    timeline_columns,
    forecast_times,
    forecast_risks
):

    with column:

        if risk >= 70:

            icon = "🔴"

        elif risk >= 50:

            icon = "🟠"

        elif risk >= 30:

            icon = "🟡"

        else:

            icon = "🟢"


        with st.container(
            border=True
        ):

            st.markdown(
                f"### {icon}"
            )

            st.markdown(
                f"**+{time} min**"
            )

            st.metric(
                "Risk",
                f"{risk:.0f}%"
            )


# ============================================================
# FORECAST CURVE
# ============================================================

st.subheader(
    "📈 Forecast Probability Curve"
)


forecast_df = pd.DataFrame(
    {
        "Lead Time (min)": forecast_times,
        "Thunderstorm Risk (%)":
            forecast_risks
    }
)


st.line_chart(
    forecast_df.set_index(
        "Lead Time (min)"
    ),
    height=280
)


# ============================================================
# FORECAST METHOD COMPARISON
# ============================================================

st.subheader(
    "🧠 Forecast Method Comparison"
)


comparison = pd.DataFrame(
    {
        "Method": [
            "Persistence",
            "Optical Flow",
            "VajraNow AI Fusion"
        ],

        "Role": [
            "Baseline",
            "Storm-motion baseline",
            "Multi-feature ML prototype"
        ],

        "MAE": [
            "0.2222*",
            "0.0000*",
            "Pending real-data evaluation"
        ],

        "CSI": [
            "0.0000*",
            "1.0000*",
            "Pending real-data evaluation"
        ]
    }
)


st.dataframe(
    comparison,
    use_container_width=True,
    hide_index=True
)


st.caption(
    "* Persistence and Optical Flow values are from "
    "the controlled synthetic demonstration."
)


# ============================================================
# HOW VAJRANOW WORKS
# ============================================================

st.subheader(
    "🛰️ How VajraNow Works"
)


st.caption(
    "Multi-sensor observations are transformed into "
    "a thunderstorm risk estimate and decision-support alert."
)


with st.container(
    border=True
):

    p1, p2, p3, p4, p5 = st.columns(5)


    with p1:

        st.markdown(
            "## 📡"
        )

        st.markdown(
            "**RADAR**"
        )

        st.caption(
            "Storm intensity"
        )


    with p2:

        st.markdown(
            "## 🛰️"
        )

        st.markdown(
            "**SATELLITE**"
        )

        st.caption(
            "Cloud evolution"
        )


    with p3:

        st.markdown(
            "## ⚡"
        )

        st.markdown(
            "**LIGHTNING**"
        )

        st.caption(
            "Electrical activity"
        )


    with p4:

        st.markdown(
            "## 🌡️"
        )

        st.markdown(
            "**ATMOSPHERE**"
        )

        st.caption(
            "Instability"
        )


    with p5:

        st.markdown(
            "## 🧠"
        )

        st.markdown(
            "**AI FUSION**"
        )

        st.caption(
            "Risk prediction"
        )


# ============================================================
# DEMO MODE STATUS
# ============================================================

if st.session_state.demo_mode:

    stage_number = (
        st.session_state.demo_index
        + 1
    )

    total_stages = len(
        DEMO_STAGES
    )


    st.success(
        f"""
        🎬 **Demo Mode: Stage {stage_number}/{total_stages}**

        Current storm state:
        **{scenario_name}**

        Click **Next Storm Stage** to demonstrate
        storm development → intensification → decay.
        """
    )


# ============================================================
# FINAL PROTOTYPE STATUS
# ============================================================

st.divider()


st.subheader(
    "⚡ VajraNow Prototype"
)


status_columns = st.columns(5)


with status_columns[0]:

    st.success(
        "✓ AI Model"
    )


with status_columns[1]:

    st.success(
        "✓ Risk Map"
    )


with status_columns[2]:

    st.success(
        "✓ Forecast"
    )


with status_columns[3]:

    st.success(
        "✓ Explainability"
    )


with status_columns[4]:

    st.success(
        "✓ Demo Mode"
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()


st.markdown(
    "### ⚡ VajraNow"
)


st.caption(
    "Observe → Fuse → Predict → Explain → Alert"
)


st.caption(
    "Prototype demonstration uses synthetic atmospheric "
    "observations, storm fields and training data."
)


st.caption(
    "Operational deployment requires validation using "
    "historical radar, satellite, lightning and "
    "atmospheric datasets."
)


st.caption(
    "This prototype is a regional proof-of-concept and "
    "is not an operational weather-warning system."
)