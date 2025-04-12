import logging
import pandas as pd
import streamlit as st

import settings
from streams import stream_metrics

run_every = st.session_state.run_every if st.session_state.isMonitoring else None


@st.fragment(run_every=run_every)
def update_monitoring_metrics():

    if not settings.isMonitoring:
        return

    new_data = get_recent_data(
        stream=settings.STREAM if settings.isStreams else settings.KWPS_STREAM,
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
    settings.logger.setLevel(
        level=logging.DEBUG if settings.isDebugging else logging.INFO
    )
    settings.logger.debug(f"Streaming from {stream}")

    for metric in stream_metrics(stream, topic):
        data = {
            "Timestamp": [metric["timestamp"]],
            "Published": [
                metric["data"][0]["maxoffset"] + 1
            ],  # Assuming maxoffset is the last offset + 1
            "Consumed": [metric["data"][0]["minoffsetacrossconsumers"]],
        }

        settings.logger.debug(f"Got topic metric: {data}")

        df = pd.DataFrame(data, columns=["Timestamp", "Published", "Consumed"])
        df["Timestamp"] = pd.to_datetime(df["Timestamp"], unit="ms")
        df.set_index("Timestamp", inplace=True)
        return df
