import os
from pwd import getpwuid
import pandas as pd
import streamlit as st

import settings

st.set_page_config(page_title="Data Fabric Pipeline", layout="wide", initial_sidebar_state="collapsed")

st.session_state.setdefault("username", getpwuid(os.getuid()).pw_name)
st.session_state.setdefault("password", None)
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

# Import these after setting the session state
from pages import (
    bronze_page,
    info_page,
    gold_page,
    ingestion_page,
    silver_page,
)
from utils import handle_sample_data, read_from_topic, handle_file_upload

import monitoring


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
        st.sidebar.write(
            f"Kafka Topic: {settings.STREAM if settings.isStreams else settings.KWPS_STREAM}:{settings.TOPIC}"
        )
        st.sidebar.write("Session State:")
        st.sidebar.json(st.session_state)


@st.fragment()
def log_viewer():
    st.code(st.session_state.logs, language="text", height=200)


def select_file():
    return st.file_uploader(
        label="Upload CSV",
        type=["csv"],
        on_change=handle_file_upload,
        help="Upload a CSV file to ingest data into the system.",
    )


def main():
    build_sidebar()
    # Add monitoring chart to sidebar (TODO: move to details tab)
    if st.session_state.isMonitoring:
        monitoring.update_monitoring_metrics()
        with st.sidebar:
            st.line_chart(st.session_state.topic_stats)

    info_page()

    with st.container(border=True):
        st.write("Data ingestion")
        cols = st.columns([20, 80], border=True, gap='medium', vertical_alignment='center')
        cols[0].button(
            "To Kafka Topic",
            on_click=handle_sample_data,
            help=f"Generate sample data and publish to Kafka topic: {settings.STREAM if settings.isStreams else settings.KWPS_STREAM}:{settings.TOPIC}",
            use_container_width=True,
        )
        cols[0].button(
            "Upload File",
            on_click=handle_file_upload,
            help=f"Upload a CSV file and publish to Kafka topic: {settings.STREAM if settings.isStreams else settings.KWPS_STREAM}:{settings.TOPIC}",
            use_container_width=True,
        )
            
        with cols[1]:
            ingestion_page()


    if st.session_state.topic_data.empty:
        st.error("No data available. Please upload a file or generate sample data.")
    else:
        with st.container(border=True):
            st.write("Data Transformation")
            bronze_page()

    # silver_page()

    # gold_page()

    log_viewer()
    # Start streaming from topic at app start
    # read_from_topic() 

if __name__ == "__main__":
    main()
