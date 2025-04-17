import os
from pwd import getpwuid
import pandas as pd
from requests import session
import streamlit as st

import settings

st.set_page_config(page_title="Data Fabric Pipeline", layout="wide", initial_sidebar_state="collapsed")

st.session_state.setdefault("username", getpwuid(os.getuid()).pw_name)
st.session_state.setdefault("password", None)
st.session_state.setdefault("logs", "")
st.session_state.setdefault("topic_stats", None)
st.session_state.setdefault("isMonitoring", settings.isMonitoring)
st.session_state.setdefault("isDebugging", settings.isDebugging)
st.session_state.setdefault("isStreams", settings.isStreams)
st.session_state.setdefault("topic_data", pd.DataFrame())
st.session_state.setdefault("bronze_data", pd.DataFrame())
st.session_state.setdefault("silver_data", pd.DataFrame())
st.session_state.setdefault("gold_data", pd.DataFrame())
# settings.isMonitoring = (
#     "isMonitoring" in st.session_state and st.session_state.isMonitoring
# )
# settings.isDebugging = (
#     "isDebugging" in st.session_state and st.session_state.isDebugging
# )
# settings.isStreams = "isStreams" in st.session_state and st.session_state.isStreams

# Import these after setting the session state
from pages import (
    bronze_page,
    info_page,
    gold_page,
    streaming_page,
    silver_page,
)

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


def log_viewer():
    st.code(st.session_state.logs, language="text", height=200, line_numbers=True)


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
        streaming_page()

    with st.container(border=True):
        st.write("Data Transformation")
        bronze_page()

    with st.container(border=True):
        st.write("Data Aggregation")
        silver_page()

    with st.container(border=True):
        st.write("Data Products")
        gold_page()

    log_viewer()
    # Start streaming from topic at app start
    # handle_topic_consume()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("DO WHATEVER HERE", e)  # 👈Modify this line 
        raise e
