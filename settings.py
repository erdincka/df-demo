import logging
import streamlit as st

isDebugging = True  # Set this to False in production
isStreams = False
isMonitoring = False

STREAM = "iot"
TOPIC = "devices"
KWPS_STREAM = f"/var/mapr/mapr.kwps.root/topics/{TOPIC}/stream"
BRONZE_DATA_PATH = "demo_bronze_data"
SILVER_DATA_PATH = "demo_silver_data"
GOLD_DATA_PATH = "demo_gold_data"


class StreamlitLogHandler(logging.Handler):
    def __init__(self, widget_update_func):
        super().__init__()
        self.widget_update_func = widget_update_func
        self.level = logging.INFO  # Default log level

    def emit(self, record):
        msg = self.format(record)
        self.widget_update_func(msg)


# logging.basicConfig(level=logging.DEBUG if isDebugging else logging.INFO)
logger = logging.getLogger(__name__)
# logger = get_logger(__name__)
logger.setLevel(level=logging.DEBUG if isDebugging else logging.INFO)


# Write logs to session
def add_to_logs(msg):
    st.session_state.logs += str(msg) + "\n"


# logger.addHandler(StreamlitLogHandler(add_to_logs))
# streamlit_log_handler = StreamlitLogHandler(st.empty().code)
streamlit_log_handler = StreamlitLogHandler(add_to_logs)
streamlit_log_handler.setLevel(logging.INFO)
logger.addHandler(streamlit_log_handler)


# FIX: Ask user for credentials
def get_credentials():
    return "mapr", "mapr"
