import json
from typing import Any
import numpy as np
import streamlit as st
import pandas as pd

from kafkaing import publish, subscribe
import mock
import settings
from streams import consume, produce


def handle_file_upload(file):
    settings.logger.info(file)

    with open(file, "rb") as f:
        bytes = f.read()
        print(bytes)
        # TODO: Handle the data ingestion here
        pass


def handle_sample_data():
    messages = mock.get_samples()
    for message in messages:
        settings.logger.debug(f"Sending data: {message}")
        data_sent = produce(message=json.dumps(message)) if settings.isStreams else publish(message=json.dumps(message))
        if data_sent:
            settings.logger.info(f"Published: {message}")
            # TODO: Bypassing topic subscription, loading directly on session state for now
            new_metric = pd.DataFrame(message, columns=list(message.keys()), index=[0])
            st.session_state.topic_data = pd.concat(
                [st.session_state.topic_data, new_metric]
            )
        else:
            settings.logger.warning(f"Failed publish {message}")

def read_from_topic():
    settings.logger.debug(f"Streaming from {settings.STREAM if settings.isStreams else settings.KWPS_STREAM}")

    # Subscribe to the stream
    for message in consume() if settings.isStreams else subscribe():
        # settings.logger.debug(f"Received: {message}")
        st.session_state.topic_data = pd.concat(
            [st.session_state.topic_data, pd.DataFrame([json.loads(message)])]
        )
        st.rerun()

    settings.logger.debug("Done with streaming!")


def label_category(metric: Any):
    # Simulating AI inferencing for labeling
    # TODO: Replace this with actual AI model inference
    return type(metric).__name__


def set_topic_index():
    if st.session_state.topic_index is not None:
        print("FOUND INDEX! SETTING IT NOW!")
        st.session_state.topic_data.set_index(st.session_state.topic_index, inplace=True)
    if "topic_index" in st.session_state and st.session_state.topic_index == 'timestamp':
        print("FOUND TIMESTAMP! SETTING IT TO DATE!")
        st.session_state.topic_data['timestamp'] = pd.to_datetime(int(st.session_state.topic_data['timestamp']), unit="s")
        st.session_state.topic_data.set_index('timestamp', inplace=True)
