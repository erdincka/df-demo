import os
import pandas as pd
from requests import session
import streamlit as st

# from streamlit.logger import get_logger

import monitoring
from pages import (
    bronze_page,
    info_page,
    gold_page,
    ingestion_page,
    silver_page,
)
import settings
from utils import handle_data_consumption, handle_data_ingestion_file


st.set_page_config(page_title="IoT Devices", layout="wide")

st.session_state.setdefault("logs", "")
st.session_state.setdefault("topic_stats", None)
st.session_state.setdefault("bronze_data", None)
st.session_state.setdefault("silver_data", None)
st.session_state.setdefault("gold_data", None)
st.session_state.setdefault("isMonitoring", settings.isMonitoring)
st.session_state.setdefault("isDebugging", settings.isDebugging)
st.session_state.setdefault("isStreams", settings.isStreams)
st.session_state.setdefault("topic_data", pd.DataFrame())
settings.isMonitoring = (
    "isMonitoring" in st.session_state and st.session_state.isMonitoring
)
settings.isDebugging = (
    "isDebugging" in st.session_state and st.session_state.isDebugging
)
settings.isStreams = "isStreams" in st.session_state and st.session_state.isStreams


def build_sidebar():
    cols = st.sidebar.columns(2)
    cols[0].link_button(
        "DFUI",
        f"https://{os.environ['USER']}@localhost:8443/app/dfui",
        type="tertiary",
        icon=":material/home:",
    )
    cols[1].link_button(
        "MCS",
        f"https://{os.environ['USER']}@localhost:8443/app/mcs",
        type="tertiary",
        icon=":material/settings:",
    )
    st.sidebar.toggle("Monitor Topic", key="isMonitoring", value=False)
    st.sidebar.toggle("Use DF Streams", key="isStreams", value=False)
    st.sidebar.toggle("Debug", key="isDebugging", value=False)

    if settings.isMonitoring:
        st.sidebar.title("Monitoring")
        st.sidebar.slider(
            "Check for updates every: (seconds)",
            0.5,
            5.0,
            value=2.0,
            key="run_every",
            step=0.5,
            help="Check every X seconds",
        )
    # Debug info
    if settings.isDebugging:
        st.sidebar.title("Debugging")
        st.sidebar.write(f"Monitoring: {settings.isMonitoring}")
        st.sidebar.write(f"DF Streams: {settings.isStreams}")
        st.sidebar.write(
            f"From: {settings.STREAM if settings.isStreams else settings.KWPS_STREAM}:{settings.TOPIC}"
        )
        st.sidebar.write(f"Data: {st.session_state.topic_stats}")


@st.fragment()
def log_viewer():
    st.code(st.session_state.logs, language="text", height=300)


@st.fragment(run_every=5)
def read_from_topic():
    # Subscribe to the stream
    handle_data_consumption()
    if st.session_state.topic_data.empty:
        st.write("No data received yet.")
    else:
        with open(settings.BRONZE_DATA_PATH, "w") as f:
            f.write(st.session_state.topic_data.to_csv(index=False))
        st.write("Data saved to bronze layer.")


def select_file():
    return st.file_uploader(
        label="Upload CSV",
        type=["csv"],
        on_change=handle_data_ingestion_file,
        help="Upload a CSV file to ingest data into the system.",
    )


def main():
    build_sidebar()
    # Add monitoring chart to sidebar (TODO: move to details tab)
    if st.session_state.isMonitoring:
        monitoring.update_monitoring_metrics()
        with st.sidebar:
            st.line_chart(st.session_state.topic_stats)

    # demo_info()
    # Ingestion Page
    ingestion_page()

    bronze_page()

    silver_page()

    gold_page()

    log_viewer()


if __name__ == "__main__":
    main()
