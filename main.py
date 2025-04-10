import json
import logging
import os
import pandas as pd
import streamlit as st
from streamlit.logger import get_logger

import mock
from monitoring import get_recent_data
from streams import produce


class StreamlitLogHandler(logging.Handler):
    def __init__(self, widget_update_func):
        super().__init__()
        self.widget_update_func = widget_update_func

    def emit(self, record):
        msg = self.format(record)
        self.widget_update_func(msg)


st.set_page_config(page_title="IoT Devices", layout="wide")
STREAM = "iot/device_metrics"
TOPIC = "devices"
st.session_state.setdefault("logs", "")
# st.session_state.setdefault("monitor", False)
run_every = st.session_state.run_every if 'monitor' in st.session_state and st.session_state.monitor else None


logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)
logger = get_logger(__name__)
logger.debug("Using topic at: %s:%s", STREAM, TOPIC)


# Write logs to session
def add_to_logs(msg):
    st.session_state["logs"] += str(msg) + "\n"


@st.fragment(run_every=run_every)
def show_latest_data(STREAM: str, TOPIC: str):

    st.session_state.data = pd.concat(
        [st.session_state.data, get_recent_data(STREAM, TOPIC)]
    )
    st.session_state.data = st.session_state.data[-100:] # Limit to the last 100 entries
    st.line_chart(st.session_state.data)


def build_sidebar():
    st.sidebar.link_button("Management UI", f"https://{os.environ['USER']}@localhost:8443/app/dfui", type='tertiary')
    st.sidebar.title("Monitoring")
    st.sidebar.slider(
        "Check for updates every: (seconds)", 0.5, 5.0, value=2.0, key="run_every", step=0.5, help="How often to check for new data"
    )
    st.sidebar.toggle("Monitor topic stat", key="monitor", value=False)


def handle_stream_sampling():
    messages = mock.get_samples()
    for msg in messages:
        logger.debug(f"Sending data: {msg}")
        if produce(stream=STREAM, topic=TOPIC, message=json.dumps(msg)):
            logger.info(f"Published: {msg}")
        else:
            logger.warning(f"Failed publish {msg}")


def main():

    build_sidebar()
        
    st.button("Data ingestion", on_click=handle_stream_sampling, help=f"Publishing to Kafka topic: {STREAM}:{TOPIC}")

    if "data" not in st.session_state:
        st.session_state.data = get_recent_data(STREAM, TOPIC)

    with st.sidebar:
        show_latest_data(STREAM, TOPIC)

    # streamlit_log_handler = StreamlitLogHandler(st.empty().code)
    streamlit_log_handler = StreamlitLogHandler(add_to_logs)
    streamlit_log_handler.setLevel(logging.INFO)
    logger.addHandler(streamlit_log_handler)
    st.code(st.session_state.get("logs", ""), language="text", height=300)
    

if __name__ == "__main__":
    main()
