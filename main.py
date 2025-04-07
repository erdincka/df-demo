import asyncio
import logging
import streamlit as st
from streamlit.logger import get_logger

import mock
from streams import produce, stream_metrics

class StreamlitLogHandler(logging.Handler):
    def __init__(self, widget_update_func):
        super().__init__()
        self.widget_update_func = widget_update_func

    def emit(self, record):
        msg = self.format(record)
        self.widget_update_func(msg)

st.set_page_config(page_title="Device monitoring", layout="wide")
STREAM = "iot/device_metrics"
TOPIC = "devices"
st.session_state.setdefault("logs", "")

logger = get_logger(__name__)
logger.setLevel(logging.DEBUG)
logger.debug("Starting device monitoring app")
logger.debug("Stream path: %s", STREAM)
logger.debug("Topic: %s", TOPIC)


def handle_stream_sampling():
    for data in mock.get_samples():
        logger.info(f"Sending data: {data}")
        if produce(STREAM, TOPIC, str(data)):
            logger.info("Data sent successfully")
        else:
            logger.warning("Failed to send data")

# Write logs to session
def add_to_logs(msg):
    st.session_state["logs"] += str(msg)
    

async def main():
    st.title("Device Metrics Real-time Visualization")
    st.write(f"Publishing data to: {STREAM}:{TOPIC}")
    st.button("Sample Data", on_click=handle_stream_sampling)

    async for metric in stream_metrics(STREAM, TOPIC):
        add_to_logs(metric)

    # streamlit_log_handler = StreamlitLogHandler(st.empty().code)
    streamlit_log_handler = StreamlitLogHandler(add_to_logs)
    streamlit_log_handler.setLevel(logging.INFO)
    logger.addHandler(streamlit_log_handler)
    st.code(st.session_state.get("logs", ""), language="text", height=300)


if __name__ == "__main__":
    asyncio.run(main())
