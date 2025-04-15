import logging
import streamlit as st
from streamlit.logger import get_logger

isDebugging = False  # Set this to False in production
isStreams = False
isMonitoring = False

STREAM = "demo"
TOPIC = "metrics"
KWPS_STREAM = f"/var/mapr/mapr.kwps.root/topics/{TOPIC}/stream"
APP_VOLUME = "."
BRONZE_DATA_PATH = f"{APP_VOLUME}/demo_bronze_data"
SILVER_DATA_PATH = f"{APP_VOLUME}/demo_silver_data"
GOLD_DATA_PATH = f"{APP_VOLUME}/demo_gold_data"

logging.getLogger("watchdog").setLevel(logging.WARNING)

class StreamlitLogHandler(logging.Handler):
    def __init__(self, widget_update_func):
        super().__init__()
        self.widget_update_func = widget_update_func
        self.level = logging.INFO  # Default log level

    def emit(self, record):
        msg = self.format(record)
        self.widget_update_func(msg)

FORMAT = '%(asctime)s %(levelname)s %(filename)s:%(lineno)d (%(funcName)s) - %(message)s'
logging.basicConfig(format=FORMAT, level=logging.WARNING)

logger = get_logger(__name__)
logger.setLevel(level=logging.DEBUG if isDebugging else logging.INFO)

# Write logs to session
def add_to_logs(msg):
    st.session_state.logs += str(msg) + "\n"

# streamlit_log_handler = StreamlitLogHandler(st.empty().code)
streamlit_log_handler = StreamlitLogHandler(add_to_logs)
streamlit_log_handler.setLevel(logging.INFO)
logger.addHandler(streamlit_log_handler)


# TODO: Ask user for credentials
# @st.dialog("User Credentials")
def get_credentials():
    return 'mapr', 'mapr'
    if st.session_state.password is None:
        with st.form("credentials_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Submit")
            if submitted:
                st.session_state.username = username
                st.session_state.password = password
    return st.session_state.username, st.session_state.password
