import logging
import pandas as pd
import streamlit as st

from kafkaing import publish, subscribe
import settings
from utils import publish_messages

logger = logging.getLogger(__name__)

@st.fragment
def update_monitoring_metrics():

    new_data = get_recent_data(
        stream=settings.STREAM,
        topic=settings.TOPIC,
    )

    if new_data is None:
        return

    st.session_state.topic_stats = pd.concat(
        [st.session_state.topic_stats, new_data],
        ignore_index=True,
    )
    st.session_state.topic_stats = st.session_state.topic_stats[
        -100:
    ]  # Limit to the last 100 entries


def get_recent_data(stream: str, topic: str):
    logger.debug(f"Streaming from {stream}:{topic}")

    for metric in subscribe():
        data = {
            "Timestamp": [metric["timestamp"]], # pyright: ignore
            "Published": [
                metric["data"][0]["maxoffset"] + 1 # pyright: ignore
            ],  # Assuming maxoffset is the last offset + 1
            "Consumed": [metric["data"][0]["minoffsetacrossconsumers"]], # pyright: ignore
        }

        logger.debug(f"Got topic metric: {data}")

        df = pd.DataFrame(data, columns=["Timestamp", "Published", "Consumed"])
        df["Timestamp"] = pd.to_datetime(df["Timestamp"], unit="ms")
        df.set_index("Timestamp", inplace=True)
        return df


def stream_metric():
    pass
